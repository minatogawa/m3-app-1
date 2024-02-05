from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import plotly.graph_objs as go

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    # Preenche o Data Grid com dados
    self.preencher_data_grid()

  def button_logout_click(self, **event_args):
    # Encerra a sessão do usuário atual
    anvil.users.logout()
    
    # Redireciona o usuário de volta ao Form1 (tela de login)
    anvil.open_form('signin_signup')

  def file_loader_1_change(self, file, **event_args):
    # Salva o arquivo carregado em uma variável de instância para uso posterior
    self.loaded_file = file
    # Torna o botão de processamento visível
    self.process_archive.visible = True

  # No evento de clique do botão (para processar o arquivo .bib)
  def process_archive_click(self, **event_args):
    if self.loaded_file:
      # Chama a função do servidor para processar e armazenar os dados do arquivo .bib
      resultado = anvil.server.call('processar_bibtex_e_armazenar', self.loaded_file)
      # Exibe uma mensagem de confirmação
      alert(resultado)
      # Atualiza o repeating panel com os novos dados processados
      self.preencher_data_grid()  # Ou self.mostrar_dados(), dependendo da função que você está usando.
      # Torna o Data Grid visível
      self.data_grid.visible = True
    else:
      alert("Nenhum arquivo foi carregado. Por favor, carregue um arquivo .bib para processar.")
    self.desenhar_grafico()


  def mostrar_dados(self):
    dados = anvil.server.call('buscar_dados')
    self.data_grid.items = dados  # Atualiza o Data Grid com os dados recebidos

  def preencher_data_grid(self):
    try:
        # Chama a função do servidor para buscar os dados da última sessão
        dados = anvil.server.call('buscar_dados_da_ultima_sessao')
        # Atualiza os itens do Data Grid diretamente com os dados
        self.repeating_panel_1.items = dados
    except Exception as e:
        print(e)  # Isso imprimirá o erro no console de execução

  def desenhar_grafico(self):
        dados_grafico = anvil.server.call('dados_papers_ultima_sessao_por_ano')

        # Cria as coordenadas X e Y para o gráfico
        anos = [ano for ano, _ in dados_grafico]
        contagem_papers = [contagem for _, contagem in dados_grafico]
        
        # Cria o gráfico
        data = [go.Bar(x=anos, y=contagem_papers)]
        layout = go.Layout(title='Papers published per year')
        fig = go.Figure(data=data, layout=layout)

        # Exibe o gráfico no Plot component
        self.plot_1.data = fig.data
        self.plot_1.layout = fig.layout