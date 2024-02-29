from ._anvil_designer import FormGraficoPublicacoesPorAnoTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class FormGraficoPublicacoesPorAno(FormGraficoPublicacoesPorAnoTemplate):

    def __init__(self, **properties):
        self.init_components(**properties)
        # Assume que 'dados_grafico' é passado como uma lista de tuplas (ano, contagem)
        self.dados_grafico = properties.get('dados_grafico', [])
        self.desenhar_grafico()

    def desenhar_grafico(self):
        if not self.dados_grafico:
            print("Nenhum dado para exibir.")
            return
        
        # Preparar os dados para o gráfico
        anos, contagens = zip(*self.dados_grafico)  # Desempacota os dados em duas listas
        
        # Criar o gráfico
        data = [go.Bar(x=anos, y=contagens)]
        layout = go.Layout(
            title='Publicações por Ano',
            xaxis=dict(title='Ano'),
            yaxis=dict(title='Número de Publicações')
        )
        
        # Configurar e exibir o gráfico
        fig = go.Figure(data=data, layout=layout)
        # Supondo que você tenha um componente Plot na sua interface chamado 'plot_area'
        self.plot_area.data = fig.data
        self.plot_area.layout = fig.layout

    def button_1_click(self, **event_args):
      open_form('Form1')