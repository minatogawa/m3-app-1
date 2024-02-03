import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import bibtexparser
import io

@anvil.server.callable
def processar_bibtex_e_armazenar(blob_media):
    # Assumindo que o usuário está logado
    usuario_atual = anvil.users.get_user()

    # Lê o arquivo como uma string
    bibtex_str = blob_media.get_bytes().decode()
    # Usa bibtexparser.loads para processar a string BibTeX
    bibtex_database = bibtexparser.parse_string(bibtex_str)

    # Para cada entrada no arquivo BibTeX
    for entrada in bibtex_database.entries:
        # Convertendo cada entrada para um dicionário, assegurando que todos os valores sejam strings ou None
        entrada_dict = {chave: str(valor) if valor else None for chave, valor in entrada.items()}

        # Inserir entrada na tabela de dados
        app_tables.bib_data.add_row(
            user=usuario_atual,
            author=entrada_dict.get('author', None),
            title=entrada_dict.get('title', None),
            year=entrada_dict.get('year', None),
            journal=entrada_dict.get('journal', None),
            doi=entrada_dict.get('doi', None),
            keywords=entrada_dict.get('keywords', None),
            correspondence_address=entrada_dict.get('address', None),  # Assumindo que 'address' seja o campo correto
            publisher=entrada_dict.get('publisher', None)
            # Os campos devem corresponder exatamente aos nomes das colunas na sua tabela de dados
        )

    return "Dados processados e armazenados com sucesso."
  

