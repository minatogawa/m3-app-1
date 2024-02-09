from ._anvil_designer import GraphPageTemplate
from anvil import *
import plotly.graph_objects as go

class GraphPage(GraphPageTemplate):
  def __init__(self, dados_grafico, **properties):
    self.init_components(**properties)
    # Desenha o gráfico com os dados recebidos
    self.desenhar_grafico(dados_grafico)
  
  def desenhar_grafico(self, dados_grafico):
    anos = [ano for ano, _ in dados_grafico]
    contagem_papers = [contagem for _, contagem in dados_grafico]
    
    # Cria o gráfico
    fig = go.Figure(data=[go.Bar(x=anos, y=contagem_papers)])
    fig.update_layout(title='Papers Published per Year', xaxis_title='Year', yaxis_title='Number of Papers')
    
    # Exibe o gráfico no componente Plot da página
    self.plot_component.data = fig.data
    self.plot_component.layout = fig.layout
