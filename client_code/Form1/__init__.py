from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import plotly.graph_objs as go

class Form1(Form1Template):

    def __init__(self, **properties):
        self.init_components(**properties)
        self.fill_data_grid()

    def button_logout_click(self, **event_args):
        anvil.users.logout()
        anvil.open_form('signin_signup')

    def file_loader_1_change(self, file, **event_args):
        self.loaded_file = file
        self.process_archive.visible = True

    def process_archive_click(self, **event_args):
        if self.loaded_file:
            result = anvil.server.call('process_and_store_bibtex', self.loaded_file)
            alert(result)
            self.fill_data_grid()
        else:
            alert("Please upload a .bib file to process.")
        self.draw_graph()
        self.draw_top_journals_graph()
        self.draw_keywords_streamgraph()

    def fill_data_grid(self):
        data = anvil.server.call('fetch_last_session_data')
        self.repeating_panel_1.items = data

    def draw_generic_graph(self, data, layout, plot_component):
        fig = go.Figure(data=data, layout=layout)
        plot_component.data = fig.data
        plot_component.layout = fig.layout

    def draw_graph(self):
        graph_data = anvil.server.call('fetch_papers_per_year')
        years, paper_counts = zip(*graph_data)
        data = [go.Bar(x=years, y=paper_counts)]
        layout = go.Layout(title='Papers Published per Year')
        self.draw_generic_graph(data, layout, self.plot_1)

    def draw_top_journals_graph(self):
        top_journals = anvil.server.call('fetch_top_journals')
        journals, counts = zip(*top_journals)
        data = [go.Bar(x=journals, y=counts)]
        layout = go.Layout(title='Top 10 Journals by Publications')
        self.draw_generic_graph(data, layout, self.plot_2)

    def draw_keywords_streamgraph(self):
        keywords_data = anvil.server.call('fetch_keywords_data')
        self.draw_generic_graph(keywords_data, self.plot_3)
