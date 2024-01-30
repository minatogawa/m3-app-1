from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  def file_loader_1_change(self, file, **event_args):
    self.loaded_file = file
    self.process_archive.visible = True

  # No evento de clique do botão (para uso futuro)
  def process_archive_click(self, **event_args):
    print("Processando Arquivo")
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
      grid.role = 'wide'
      grid.columns = [{"id": col, "title": col, "data_key": col, "width": "200"} for col in colunas]
      
      # Preenchendo o Data Grid
      for linha in linhas:
          # Crie um dicionário mapeando nomes de colunas para valores de linha
          item = {col: valor for col, valor in zip(colunas, linha)}
          grid.add_component(DataRowPanel(item=item))

      # Adicionando o Data Grid ao formulário
      self.add_component(grid)

    else:
      print("Nenhum arquivo carregado")

    # Cria o botão
    self.btn_hello = Button(text="Mostrar Olá")
    self.btn_hello.set_event_handler('click', self.on_hello_button_click)
    self.add_component(self.btn_hello)

  def on_hello_button_click(self, **event_args):
    # Cria a label
    label_hello = Label(text="Olá")
    # Adiciona a label ao formulário
    self.add_component(label_hello)
    # Chama a função do backend para gerar o gráfico
    if self.loaded_file:  # Certifica-se de que um arquivo foi carregado
        grafico = anvil.server.call('gerar_grafico_publicacoes_por_ano', self.loaded_file)
        # Exibir o gráfico
        self.add_component(Image(source=grafico))
    else:
        print("Nenhum arquivo carregado")


