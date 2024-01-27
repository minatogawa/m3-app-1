from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    # Adicione seu CSS personalizado aqui ou no designer do Anvil sob Assets > Theme > Custom HTML
    self.add_component(Label(text="Carregue um arquivo BibTeX e clique em Processar."), 
                        slot="content_panel")

  def button_1_click(self, **event_args):
    resposta = anvil.server.call('testar_conexao')
    print(resposta)

  def file_loader_1_change(self, file, **event_args):
    self.loaded_file = file
    self.my_button.visible = True

  def my_button_click(self, **event_args):
    print("Processando arquivo...")
    if self.loaded_file:
        # Cria um objeto BlobMedia a partir do arquivo carregado
        blob = anvil.BlobMedia(content_type=self.loaded_file.content_type,
                                content=self.loaded_file.get_bytes(),
                                name=self.loaded_file.name)
        
        dados = anvil.server.call('processar_bibtex_e_criar_dataframe', blob)
        self.add_data_grid_with_wrapped_text(dados["colunas"], dados["linhas"])
    else:
        print("Nenhum arquivo carregado")

  def add_data_grid_with_wrapped_text(self, colunas, linhas):
    # Limpa o content_panel antes de adicionar um novo DataGrid
    self.content_panel.clear()
    
    # Criar o DataGrid e definir colunas com a classe CSS para quebra de texto
    grid = DataGrid()
    grid.columns = [
        {"id": col, "title": col, "data_key": col, "width": None, "role": "wrap-text"}
        for col in colunas
    ]
    
    # Preenchendo o DataGrid
    for linha in linhas:
        # Cria um DataRowPanel
        row_panel = DataRowPanel()
        for col, valor in zip(colunas, linha):
            # Converte o valor para string antes de verificar o comprimento
            valor_str = str(valor)
            # Usa um Button para que possamos adicionar um tooltip
            cell_button = Button(text=valor_str, role='cell')
            # Define o tooltip se o texto for muito longo
            if len(valor_str) > 50:
                cell_button.tooltip = valor_str
            # Adiciona o Button ao DataRowPanel com o papel específico
            row_panel.add_component(cell_button, col)
        # Adiciona o DataRowPanel ao DataGrid
        grid.add_component(row_panel)
    
    # Adicionando o DataGrid ao content_panel do formulário
    self.content_panel.add_component(grid)






    



