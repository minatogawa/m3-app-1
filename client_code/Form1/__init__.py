from ._anvil_designer import Form1Template
from anvil import *
import anvil.server


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Configuração inicial do DataGrid
    self.configure_data_grid()

    # Any code you write here will run before the form opens.

  def configure_data_grid(self):
    # Adiciona uma coluna ao DataGrid
    self.data_grid_1.columns = [
       {'title': "Autores", 'data_key': "autores"}
    ]

  
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
      
      # Chama a função no servidor e passa o BlobMedia
      processed_data = anvil.server.call('processar_bibtex', blob)
      
      # Exibe os dados processados
      self.label_resultado.text = processed_data

      if processed_data:
        self.data_grid_1.items = [{'autores': autores} for autores in processed_data]
      else:
        print("Erro ao obter autores")
      
    else:
      print("Nenhum arquivo carregado")
    



