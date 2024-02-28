from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
      self.init_components(**properties)
      
      # Chama a função para preencher o Data Grid com dados da última sessão do usuário
      self.preencher_data_grid()

  def preencher_data_grid(self):
    dados = anvil.server.call('buscar_dados_da_ultima_sessao')
    if dados:  # Verifica se há dados para evitar erros
        self.repeating_panel_1.items = dados
    else:
        print("Nenhum dado encontrado para a última sessão.")
        

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
      self.button_publicacoes_por_ano.visible = True
      self.button_top_journals.visible = True
      self.streamgraph_keywords.visible = True
    else:
      alert("Nenhum arquivo foi carregado. Por favor, carregue um arquivo .bib para processar.")
    


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

#################################################################################################

  def button_publicacoes_por_ano_click(self, **event_args):
      dados_grafico = anvil.server.call('dados_papers_ultima_sessao_por_ano')
      anvil.open_form('FormGraficoPublicacoesPorAno', dados_grafico=dados_grafico)

  def button_top_journals_click(self, **event_args):
    dados_grafico = anvil.server.call('top_journals_ultima_sessao')
    anvil.open_form('FormGraficoTopJournals', dados_grafico=dados_grafico)

  def streamgraph_keywords_click(self, **event_args):
    dados_grafico = anvil.server.call('dados_keywords_por_ano')
    anvil.open_form('GraficoStreamKeywords', dados_grafico=dados_grafico)



  




