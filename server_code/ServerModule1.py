import anvil.server
import bibtexparser
import pandas as pd
import io
import matplotlib.pyplot as plt


# Função para truncar o texto
def truncar_texto(texto, max_length=180):
    if len(texto) > max_length:
        return texto[:max_length] + '…'
    return texto

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

    # Aplicar a função de truncar em cada célula do DataFrame
    for coluna in df.columns:
      df[coluna] = df[coluna].apply(lambda x: truncar_texto(x) if isinstance(x, str) else x)

    # Convertendo as linhas e colunas para listas
    linhas = df.values.tolist()
    colunas = df.columns.astype(str).tolist()

    return {"colunas": colunas, "linhas": linhas}


@anvil.server.callable
def gerar_grafico_publicacoes_por_ano(blob_media):
    # Lê o arquivo como uma string
    bibtex_str = blob_media.get_bytes().decode()
    # Usa bibtexparser.parse_string para processar a string BibTeX
    bibtex_database = bibtexparser.parse_string(bibtex_str)

    # Extração dos anos das publicações
    anos = []
    for entrada in bibtex_database.entries:
        ano = entrada.get('year')
        if ano and ano.isdigit():  # Verifica se o ano é um dígito
            anos.append(ano)

    anos_contagem = {ano: anos.count(ano) for ano in set(anos)}

    # Criar o gráfico
    plt.bar(anos_contagem.keys(), anos_contagem.values())
    plt.xlabel('Ano')
    plt.ylabel('Quantidade de Publicações')
    plt.title('Publicações por Ano')

    # Salvar o gráfico como um BlobMedia
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    grafico = anvil.BlobMedia('image/png', buf, name='grafico.png')
    buf.close()

    return grafico

