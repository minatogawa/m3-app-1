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
    # Debug: Imprime as entradas brutos e seus fields_dict
    # for entrada in bibtex_database.entries:
    #     # print(entrada)  # Imprime a entrada bruta
    #     print(entrada.fields_dict)  # Imprime o dicionário de campos

    # dados_formatados = ""
    # for entrada in bibtex_database.entries:
    #     dados_formatados += str(entrada.fields_dict) + "\n"

    # return dados_formatados

    lista_autores = []
    for entrada in bibtex_database.entries:
        nome_autor = entrada.fields_dict.get('Author', 'Autor Desconhecido')
        if isinstance(nome_autor, bibtexparser.model.Field):
            nome_autor = nome_autor.value
        lista_autores.append(nome_autor)

    return lista_autores

  

