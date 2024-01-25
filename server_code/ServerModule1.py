import anvil.server
import bibtexparser
import io

@anvil.server.callable
def testar_conexao():
  return "Conexão bem-sucedida!"

@anvil.server.callable
def processar_bibtex(blob_media):
    # Lê o arquivo como uma string
    bibtex_str = blob_media.get_bytes().decode()
    # Usa bibtexparser.parse_string para processar a string BibTeX
    bibtex_database = bibtexparser.parse_string(bibtex_str)
    # Processamento adicional conforme necessário...
    # Por exemplo, extrair informações específicas do BibTeX
    return str(bibtex_database.entries)  # Retorna uma representação string das entradas
