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
    # Debug: Imprime as entradas brutos e seus fields_dict
    for entrada in bibtex_database.entries:
        # print(entrada)  # Imprime a entrada bruta
        print(entrada.fields_dict)  # Imprime o dicionário de campos
  
    # Formata e organiza as entradas BibTeX
    entradas_formatadas = formatar_entradas(bibtex_database.entries)
    return entradas_formatadas
    # return str(bibtex_database.entries)  # Retorna uma representação string das entradas

def formatar_entradas(entradas):
    entradas_organizadas = []
    for entrada in entradas:
        # Utiliza fields_dict para acessar os campos da entrada
        titulo = entrada.fields_dict.get('title', 'Sem Título')
        autor = entrada.fields_dict.get('author', 'Autor Desconhecido')
        entrada_formatada = f'Título: {titulo}, Autor(es): {autor}'
        entradas_organizadas.append(entrada_formatada)
    return entradas_organizadas
