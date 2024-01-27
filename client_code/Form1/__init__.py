from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    resposta = anvil.server.call('testar_conexao')
    print(resposta)

  def file_loader_1_change(self, file, **event_args):
    self.loaded_file = file
    self.my_button.visible = True

  # No evento de clique do botão (para uso futuro)
  def my_button_click(self, **event_args):
    print("olá")
    if self.loaded_file:
      # Cria um objeto BlobMedia a partir do arquivo carregado
      blob = anvil.BlobMedia(content_type=self.loaded_file.content_type,
                              content=self.loaded_file.get_bytes(),
                              name=self.loaded_file.name)

      dados = anvil.server.call('processar_bibtex_e_criar_dataframe', blob)

      colunas = dados["colunas"]
      linhas = dados["linhas"]
  
      # Criar o Data Grid e definir colunas
      grid = DataGrid()
      grid.columns = [
        {"id": col, "title": col, "data_key": col, "cell_style": {"class": "truncate-text"}}
        for col in colunas
      ]
  
      # Preenchendo o Data Grid
      for linha in linhas:
          # Crie um dicionário mapeando nomes de colunas para valores de linha
          item = {col: valor for col, valor in zip(colunas, linha)}
          grid.add_component(DataRowPanel(item=item))

      
      # Adicionando o Data Grid ao formulário
      self.add_component(grid)
      
    else:
      print("Nenhum arquivo carregado")





      
      
    #   # Chama a função no servidor e passa o BlobMedia
    #   lista_autores = anvil.server.call('processar_bibtex', blob)
      
    #   # Cria um Data Grid
    #   grid = DataGrid()
    #   grid.columns = [
    #       {"id": "author_name", "title": "Nome do Autor", "data_key": "name"}
    #   ]

    #   # Cria um RepeatingPanel
    #   rp = RepeatingPanel(item_template=DataRowPanel)
    #   rp.items = [{"name": autor} for autor in lista_autores]

    #   # Adiciona o RepeatingPanel ao Data Grid
    #   grid.add_component(rp)

    #   # Adiciona o Data Grid ao formulário
    #   self.add_component(grid)
    # else:
    #   print("Nenhum arquivo carregado")
      

    



