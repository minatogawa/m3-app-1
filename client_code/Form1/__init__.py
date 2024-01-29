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

    def process_archive_click(self, **event_args):
        print("Processando Arquivo")
        if self.loaded_file:
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
                item = {col: valor for col, valor in zip(colunas, linha)}
                grid.add_component(DataRowPanel(item=item))

            # Criar um container para o DataGrid
            # container = FlowPanel()  # Ou ColumnPanel, se preferir
            container = FlowPanel(role='data-grid-container')
            container.add_component(grid)

            # Adicionando o Container ao formulário
            self.add_component(container)

        else:
            print("Nenhum arquivo carregado")


