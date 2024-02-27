from ._anvil_designer import FormGraficoTopJournalsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from anvil import *
import plotly.graph_objects as go

class FormGraficoTopJournals(FormGraficoTopJournalsTemplate):
    def __init__(self, **properties):
        # Inicializa os componentes do formulário, conforme definido no designer.
        self.init_components(**properties)

        self.dados_grafico = properties.get('dados_grafico', [])
        # Chama o método para desenhar o gráfico.
        self.desenhar_grafico()
        
    def desenhar_grafico(self):
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
  
      # Configurar e exibir o gráfico
      fig = go.Figure(data=data, layout=layout)
      # Supondo que você tenha um componente Plot na sua interface chamado 'plot_area'
      self.plot_area.data = fig.data
      self.plot_area.layout = fig.layout

