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
        # Chama a função do servidor para buscar os dados da última sessão
        dados = anvil.server.call('buscar_dados_da_ultima_sessao')
        # Atualiza os itens do Data Grid diretamente com os dados
        self.repeating_panel_1.items = dados
    except Exception as e:
        print(e)  # Isso imprimirá o erro no console de execução

  def desenhar_grafico_generico(self, dados, layout, plot_component):
    fig = go.Figure(data=dados, layout=layout)
    plot_component.data = fig.data
    plot_component.layout = fig.layout

  # Exemplo de como usar a função genérica
  def draw_papers_per_year(self):
    dados_grafico = anvil.server.call('dados_papers_ultima_sessao_por_ano')
    anos = [ano for ano, _ in dados_grafico]
    contagem_papers = [contagem for _, contagem in dados_grafico]
    data = [go.Bar(x=anos, y=contagem_papers)]
    layout = go.Layout(title='Papers published per year')
    self.desenhar_grafico_generico(data, layout, self.plot_1)

  def draw_top_journals_chart(self):
    top_journals = anvil.server.call('top_journals_ultima_sessao')

    cores_barras = ['rgba(255, 99, 132, 0.5)', 'rgba(54, 162, 235, 0.5)', 'rgba(255, 206, 86, 0.5)']
    cores_barras *= (len(top_journals) // len(cores_barras) + 1)

    nomes_journals = [journal.replace(' ', '<br>') for journal, _ in top_journals]
    contagem_papers = [contagem for _, contagem in top_journals]

    data = [go.Bar(x=nomes_journals, y=contagem_papers, marker=dict(color=cores_barras[:len(top_journals)]))]

    layout = go.Layout(
        title='Top 10 Journals com Mais Publicações',
        xaxis=dict(title='Journal', tickangle=0, tickmode='array', tickvals=list(range(len(nomes_journals))), ticktext=nomes_journals),
        yaxis=dict(title='Número de Publicações'),
        margin=dict(l=50, r=50, t=50, b=100)
    )

    self.desenhar_grafico_generico(data, layout, self.plot_2)


  def draw_keywords_streamgraph(self):
    dados_keywords = anvil.server.call('dados_keywords_por_ano')

    years = [dado['year'] for dado in dados_keywords]
    series = {keyword: [] for keyword in dados_keywords[0].keys() if keyword != 'year'}

    for dado in dados_keywords:
        for keyword, value in dado.items():
            if keyword != 'year':
                series[keyword].append(value)

    data = [go.Scatter(x=years, y=values, mode='lines', line=dict(shape='spline', smoothing=1.3), stackgroup='one', name=keyword) for keyword, values in series.items()]

    layout = go.Layout(
        title='Evolução das Palavras-Chave ao Longo dos Anos - Top 10',
        xaxis_title='Ano',
        yaxis_title='Frequência',
        showlegend=True
    )

    self.desenhar_grafico_generico(data, layout, self.plot_3)