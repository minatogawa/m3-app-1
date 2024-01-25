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
    if self.file_loader_1.file:
      arquivo = self.file_loader_1.file
      print("Arquivo selecionado, enviando para processamento...")
      anvil.server.call_async('processar_bibtex', arquivo, self.processar_resposta)
    else:
      anvil.alert("Por favor, selecione um arquivo .bib")

  def processar_resposta(self, resposta):
    print(f"Resposta recebida: {resposta}")
    self.label_resultado.text = resposta

  def button_2_click(self, **event_args):
    # Chamada para a função do backend
    texto_do_backend = anvil.server.call('obter_texto')
    self.label_1.text = texto_do_backend
