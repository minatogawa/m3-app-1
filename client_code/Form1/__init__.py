from ._anvil_designer import Form1Template
# Import Anvil's core functionalities for UI, server calls, and data handling.
from anvil import *
# Import Plotly's graph_objects for creating complex and interactive charts.
import plotly.graph_objects as go
# Import Anvil's table functionalities for database operations.
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# Import Anvil's user authentication module for handling user sessions.
import anvil.users
# Import Anvil's server module to enable server-side operations.
import anvil.server

# Define the class Form1, inheriting from Form1Template.
# This inheritance includes the UI design from the Anvil Designer.
class Form1(Form1Template):
  # Constructor method for the class.
  def __init__(self, **properties):
      # Initialize form components with properties. 
      # This includes setting up UI elements according to the Anvil Designer's specifications.
      self.init_components(**properties)
      
      # Code placed here runs before the form is shown to the user.
      # Call the method to fill the Data Grid with data.
      # This prepares the data presentation as soon as the form loads.
      self.fill_data_grid()

  def button_logout_click(self, **event_args):
    # Logs out the current user session.
    anvil.users.logout()
    # Redirects the user back to the signin/signup form.
    anvil.open_form('signin_signup')

  def file_loader_1_change(self, file, **event_args):
    # Saves the uploaded file in an instance variable for later use.
    self.loaded_file = file
    # Makes the processing button visible.
    self.process_archive.visible = True

  def process_archive_click(self, **event_args):
    # Check if a file has been loaded.
    if self.loaded_file:
        # Calls the server function to process and store the data from the .bib file.
        result = anvil.server.call('process_bibtex_and_store', self.loaded_file)
        # Displays a confirmation message with the result.
        alert(result)
        # Updates the repeating panel with the new processed data.
        self.fill_data_grid()
        # Makes the Data Grid visible to show the updated data.
        self.data_grid.visible = True
    else:
        # Alerts the user if no file has been uploaded.
        alert("No file has been loaded. Please upload a .bib file to process.")
    # Draw the charts
    self.draw_papers_per_year()
    self.draw_top_journals_chart()
    self.draw_keywords_streamgraph()

  def fill_data_grid(self):
    try:
        # Obtém o usuário atual
        current_user = anvil.users.get_user()
        # Caso não haja um usuário, pode-se decidir o que fazer, talvez redirecionar para um form de login
        if not current_user:
            anvil.open_form('LoginForm')
            return

        # Chama a função do servidor para buscar os dados da última sessão
        data = anvil.server.call('fetch_data_from_last_session', current_user)
        
        # Atualiza os itens do RepeatingPanel com os dados buscados
        self.repeating_panel_1.items = data
    except Exception as e:
        print(e)


###########################GRAPHS DRAWING##################################################3

  def plot_graph(self, data, layout, plot_component):
    # Creates a Figure object using Plotly, with the specified data and layout.
    # The 'data' parameter contains the data points and styling for the graph.
    # The 'layout' parameter defines the overall layout properties of the graph, such as titles, axis labels, etc.
    fig = go.Figure(data=data, layout=layout)
    
    # Assigns the data of the figure to the 'data' attribute of the plot component.
    # This line effectively updates the graph's data points and styling according to the 'fig' object.
    plot_component.data = fig.data
    
    # Assigns the layout of the figure to the 'layout' attribute of the plot component.
    # This line updates the layout properties (e.g., titles, axis labels) of the graph based on the 'fig' object.
    plot_component.layout = fig.layout


#######PAPERS PER YEAR###################################

  
  def draw_papers_per_year(self):
    # Calls a server function to retrieve data on papers published per year.
    graph_data = anvil.server.call('fetch_data_last_session_by_year')
    # Extracts the list of years from the data, which will be used as the X-axis of the graph.
    years = [year for year, _ in graph_data]
    # Extracts the paper count per year from the data, which will be used as the Y-axis of the graph.
    paper_counts = [count for _, count in graph_data]
    # Creates a bar graph data object with years on the X-axis and paper counts on the Y-axis.
    data = [go.Bar(x=years, y=paper_counts)]
    # Defines the layout of the graph, including the title.
    layout = go.Layout(title='Papers published per year')
    # Calls the generic graph plotting function with the data, layout, and specific plot component as arguments.
    self.plot_graph(data, layout, self.plot_1)

#######TOP JOURNALS###################################

  def draw_top_journals_chart(self):
    # Calls a server function to retrieve data on the top journals of the last session.
    top_journals = anvil.server.call('fetch_top_journals_last_session')

    # Defines a list of colors for the bars in the chart.
    bar_colors = ['rgba(255, 99, 132, 0.5)', 'rgba(54, 162, 235, 0.5)', 'rgba(255, 206, 86, 0.5)']
    # Repeats the color list to ensure there are enough colors for all journals.
    bar_colors *= (len(top_journals) // len(bar_colors) + 1)

    # Prepares the journal names for the X-axis, inserting line breaks for better readability.
    journal_names = [journal.replace(' ', '<br>') for journal, _ in top_journals]
    # Extracts the paper counts for each journal to be used as the Y-axis values.
    paper_counts = [count for _, count in top_journals]

    # Creates a bar chart data object, assigning colors to each bar from the color list.
    data = [go.Bar(x=journal_names, y=paper_counts, marker=dict(color=bar_colors[:len(top_journals)]))]

    # Sets up the layout of the chart, including the title and axis labels.
    layout = go.Layout(
        title='Top 10 Journals with Most Publications',
        xaxis=dict(title='Journal', tickangle=0, tickmode='array', tickvals=list(range(len(journal_names))), ticktext=journal_names),
        yaxis=dict(title='Number of Publications'),
        margin=dict(l=50, r=50, t=50, b=100)
    )

    # Calls the generic graph plotting function to display the chart with the prepared data and layout.
    self.plot_graph(data, layout, self.plot_2)
  
#######KEYWORDS EVOLUTION###################################
  
  def draw_keywords_streamgraph(self):
    # Calls a server function to fetch keyword data by year.
    keyword_data = anvil.server.call('fetch_keywords_by_year')

    # Extracts the years from the data to use as the X-axis.
    years = [data['year'] for data in keyword_data]
    # Initializes a dictionary to hold keyword series data, excluding 'year'.
    series = {keyword: [] for keyword in keyword_data[0].keys() if keyword != 'year'}

    # Populates the series dictionary with values for each keyword over the years.
    for data in keyword_data:
        for keyword, value in data.items():
            if keyword != 'year':
                series[keyword].append(value)

    # Prepares the data for a streamgraph, specifying the mode and appearance of lines.
    data = [go.Scatter(x=years, y=values, mode='lines', line=dict(shape='spline', smoothing=1.3), stackgroup='one', name=keyword) for keyword, values in series.items()]

    # Sets up the layout of the graph, including the title and axis titles.
    layout = go.Layout(
        title='Keyword Evolution Over the Years - Top 10',
        xaxis_title='Year',
        yaxis_title='Frequency',
        showlegend=True
    )

    # Calls the generic graph plotting function to display the streamgraph with the prepared data and layout.
    self.plot_graph(data, layout, self.plot_3)

  def button_view_papers_click(self, **event_args):
    data = anvil.server.call('fetch_data_last_session_by_year')
    anvil.open_form('PapersPerYearForm', data)
