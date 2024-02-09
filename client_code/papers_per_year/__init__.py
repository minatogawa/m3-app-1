from ._anvil_designer import papers_per_yearTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go

class papers_per_year(papers_per_yearTemplate):

    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

    def form_show(self, **event_args):
        # Chame o método para desenhar o gráfico quando a página é mostrada
        self.desenhar_grafico_papers_per_year()

    def desenhar_grafico_papers_per_year(self):
        dados_grafico = anvil.server.call('dados_papers_ultima_sessao_por_ano')
        anos = [ano for ano, _ in dados_grafico]
        contagem_papers = [contagem for _, contagem in dados_grafico]
        data = [go.Bar(x=anos, y=contagem_papers)]
        layout = go.Layout(title='Papers published per year')
        
        # Certifique-se de que você criou um componente plot com o nome `plot_papers_per_year` no designer
        self.plot_papers_per_year.figure = go.Figure(data=data, layout=layout)