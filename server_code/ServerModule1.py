import anvil.server
import bibtexparser

@anvil.server.callable
def testar_conexao():
  return "Conexão bem-sucedida!"

@anvil.server.callable
def processar_bibtex(arquivo):
  print("Iniciando processamento do arquivo BibTeX...")
  with anvil.media.TempFile(arquivo) as filename:
    with open(filename, 'r') as file:
      conteudo = file.read()
      # Aqui você pode processar o conteúdo do arquivo BibTeX
      try:
        bib_database = bibtexparser.parse_string(conteudo)
        # Aqui, você pode extrair informações adicionais se necessário
        return f"Arquivo com {len(bib_database.entries)} entradas processado com sucesso!"
      except Exception as e:
        return f"Erro ao processar arquivo: {e}"
      return "Arquivo processado com sucesso!"

@anvil.server.callable
def obter_texto():
    return "Texto fornecido pelo backend."