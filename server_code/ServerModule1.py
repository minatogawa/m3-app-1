import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import bibtexparser
import io
from datetime import datetime

@anvil.server.callable
def processar_bibtex_e_armazenar(blob_media):
    usuario_atual = anvil.users.get_user()

    # Cria uma nova sessão para este upload
    nova_sessao = app_tables.sessions.add_row(
        user=usuario_atual,
        upload_date=datetime.now()  # Obtém a data e hora atual
    )

    # Lê o arquivo como uma string
    bibtex_str = blob_media.get_bytes().decode()
    # Usa bibtexparser.loads para processar a string BibTeX
    bibtex_database = bibtexparser.parse_string(bibtex_str)

    # Processa e armazena cada entrada no arquivo BibTeX
    for entrada in bibtex_database.entries:
        entrada_dict = {chave: str(valor) if valor else None for chave, valor in entrada.items()}
        
        app_tables.bib_data.add_row(
            session=nova_sessao,
            author=entrada_dict.get('author', None),
            title=entrada_dict.get('title', None),
            year=entrada_dict.get('year', None),
            journal=entrada_dict.get('journal', None),
            doi=entrada_dict.get('doi', None),
            keywords=entrada_dict.get('keywords', None),
            correspondence_address=entrada_dict.get('address', None),  # Se 'address' for o campo correto
            publisher=entrada_dict.get('publisher', None)
            # Adicione quaisquer outros campos conforme necessário
        )

    # Retorna uma mensagem de confirmação
    return f"Dados processados e armazenados com sucesso para a sessão."
  

