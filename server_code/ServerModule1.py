import anvil.server
import bibtexparser
import pandas as pd
import io

@anvil.server.callable
def testar_conexao():
  return "Conexão bem-sucedida!"

@anvil.server.callable
def processar_bibtex_e_criar_dataframe(blob_media):
    # Lê o arquivo como uma string
    bibtex_str = blob_media.get_bytes().decode()
    # Usa bibtexparser.parse_string para processar a string BibTeX
    bibtex_database = bibtexparser.parse_string(bibtex_str)

    # Processando as entradas para garantir que todos os dados sejam serializáveis
    entradas_processadas = []
    for entrada in bibtex_database.entries:
        # Convertendo cada entrada para um dicionário, assegurando que todos os valores sejam strings
        entrada_dict = {chave: str(valor) for chave, valor in entrada.items()}
        entradas_processadas.append(entrada_dict)

    # Criando um DataFrame com os dados processados
    df = pd.DataFrame(entradas_processadas)

    # Convertendo as linhas e colunas para listas
    linhas = df.values.tolist()
    colunas = df.columns.astype(str).tolist()

    return {"colunas": colunas, "linhas": linhas}

  

