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
        item = {col: (str(valor)[:100] + '...' if isinstance(valor, str) and len(valor) > 100 else str(valor)) for col, valor in zip(colunas, linha)}
        
        # Crie uma instância do seu CustomRowForm para cada linha
        custom_row_form = CustomRowForm(item=item)
        # Defina um evento 'x-click' que chama abrir_modal_com_conteudo_completo
        custom_row_form.set_event_handler('x-click', self.abrir_modal_com_conteudo_completo)
        grid.add_component(custom_row_form)

      
      # Adicionando o Data Grid ao formulário
      self.add_component(grid)
      
    else:
      print("Nenhum arquivo carregado")

  # A função de callback agora aceita 'item' como um argumento diretamente
  def abrir_modal_com_conteudo_completo(self, item):
    detalhes = "\n".join(f"{k}: {v}" for k, v in item.items())
    alert(detalhes)



    



