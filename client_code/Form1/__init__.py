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
      # Ajustando a largura das colunas e habilitando quebra de linha
      grid.columns = [{"id": col, "title": col, "data_key": col, "width": 200, "wrap": True} for col in colunas]
  
      # Preenchimento do DataGrid com os dados
      for linha in linhas:
        # Convertendo tudo para string e truncando se necessário
        item = {col: (str(valor)[:100] + '...' if isinstance(valor, str) and len(valor) > 100 else str(valor)) for col, valor in zip(colunas, linha)}
        
        # Adicionando cada linha ao DataGrid
        grid_row = DataRowPanel(item=item)
        # Adicione um evento de clique que chama abrir_modal_com_conteudo_completo com um argumento de item específico
        grid_row.set_event_handler('click', lambda event_args, item=item: self.abrir_modal_com_conteudo_completo(item))
        grid.add_component(grid_row)

      
      # Adicionando o Data Grid ao formulário
      self.add_component(grid)
      
    else:
      print("Nenhum arquivo carregado")

  # A função de callback agora aceita 'item' como um argumento diretamente
  def abrir_modal_com_conteudo_completo(self, item):
    detalhes = "\n".join(f"{k}: {v}" for k, v in item.items())
    alert(detalhes)




      
      
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
      

    



