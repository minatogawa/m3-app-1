from ._anvil_designer import GraficoStreamKeywordsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class GraficoStreamKeywords(GraficoStreamKeywordsTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        # Assume que 'dados_grafico' é passado como uma lista de tuplas (ano, contagem)
        self.dados_grafico = properties.get('dados_grafico', [])
        self.desenhar_grafico()

    def desenhar_grafico(self):
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
  
      # Configurar e exibir o gráfico
      fig = go.Figure(data=data, layout=layout)
      # Supondo que você tenha um componente Plot na sua interface chamado 'plot_area'
      self.plot_1.data = fig.data
      self.plot_1.layout = fig.layout
