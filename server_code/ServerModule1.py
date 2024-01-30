import anvil.server
import bibtexparser
from anvil.tables import app_tables
import pandas as pd

# Função para truncar texto
def truncar_texto(texto, max_length=180):
    if len(texto) > max_length:
        return texto[:max_length] + '…'
    return texto

@anvil.server.callable
def processar_bibtex_e_criar_dataframe(blob_media):
    # Lê o arquivo como uma string e processa usando bibtexparser
    bibtex_str = blob_media.get_bytes().decode()
    bibtex_database = bibtexparser.parse_string(bibtex_str)

    entradas_processadas = []
    for entrada in bibtex_database.entries:
        # Processamento da entrada
        processed_entry = {
            'author': entrada['fields_dict'].get('author', ''),
            'title': entrada['fields_dict'].get('title', ''),
            'journal': entrada['fields_dict'].get('journal', ''),
            'year': int(entrada['fields_dict'].get('year', 0)) if entrada['fields_dict'].get('year') else None,
            'volume': entrada['fields_dict'].get('volume', ''),
            'number': entrada['fields_dict'].get('number', ''),
            'month': entrada['fields_dict'].get('month', ''),
            'abstract': entrada['fields_dict'].get('abstract', '')
        }
        app_tables.bibtex_entries.add_row(**processed_entry)

        # Truncar texto e adicionar na lista para o DataFrame
        processed_entry_truncated = {k: truncar_texto(v) if isinstance(v, str) else v for k, v in processed_entry.items()}
        entradas_processadas.append(processed_entry_truncated)

    # Criação do DataFrame
    df = pd.DataFrame(entradas_processadas)

    # Conversão das linhas e colunas para listas
    linhas = df.values.tolist()
    colunas = df.columns.astype(str).tolist()

    return {"colunas": colunas, "linhas": linhas}

@anvil.server.callable
def recuperar_dados_bibtex():
    return app_tables.bibtex_entries.search()