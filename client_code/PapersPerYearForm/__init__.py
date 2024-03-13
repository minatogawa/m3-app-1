from ._anvil_designer import PapersPerYearFormTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class PapersPerYearForm(PapersPerYearFormTemplate):

    def __init__(self, graph_data=None, **properties):
        # Inicializa os componentes do form
        self.init_components(**properties)
        
        # Se dados do gráfico foram passados, desenhe o gráfico
        if graph_data:
            self.draw_papers_per_year(graph_data)
        else:
            # Se nenhum dado foi passado, você pode optar por buscar os dados diretamente
            # ou mostrar uma mensagem informando que não há dados disponíveis.
            pass

    def draw_papers_per_year(self, graph_data):
        # Extracts the list of years and counts from the passed data
        years = [year for year, _ in graph_data]
        paper_counts = [count for _, count in graph_data]
        
        # Cria os dados para o gráfico
        data = [go.Bar(x=years, y=paper_counts)]
        
        # Configura o layout do gráfico
        layout = go.Layout(
            title='Papers Published per Year',
            xaxis=dict(title='Year'),
            yaxis=dict(title='Number of Papers')
        )
        
        # Cria o gráfico usando os dados e o layout
        fig = go.Figure(data=data, layout=layout)
        
        # Exibe o gráfico no componente Plot
        self.plot_1.data = fig.data
        self.plot_1.layout = fig.layout

    def button_back_click(self, **event_args):
      # Retorna ao Form1.
      anvil.open_form('Form1')


