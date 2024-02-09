import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import bibtexparser
import io
from datetime import datetime
from collections import Counter

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

@anvil.server.callable
def buscar_dados_da_ultima_sessao():
    print("Iniciando a busca de dados da última sessão")
    usuario_atual = anvil.users.get_user()
    
    # Encontra a última sessão ordenando por 'upload_date' e pegando a primeira
    ultima_sessao = app_tables.sessions.search(
        tables.order_by("upload_date", ascending=False),
        user=usuario_atual
    )[0]
    
    # Busca entradas associadas à última sessão
    entradas_da_ultima_sessao = app_tables.bib_data.search(
        session=ultima_sessao
    )
    
    # Converte as entradas em dicionários para passar ao front end
    dados = [{
        'author': entrada['author'],
        'title': entrada['title'],
        'year': entrada['year'],
        'journal': entrada['journal'],
        'doi': entrada['doi'],
        'keywords': entrada['keywords'],
        'correspondence_address': entrada['correspondence_address'],
        'publisher': entrada['publisher']
    } for entrada in entradas_da_ultima_sessao]
    
    return dados


@anvil.server.callable
def dados_papers_ultima_sessao_por_ano():
    usuario_atual = anvil.users.get_user()
    ultima_sessao = app_tables.sessions.search(
        tables.order_by("upload_date", ascending=False),
        user=usuario_atual
    )[0]

    entradas = app_tables.bib_data.search(session=ultima_sessao)
    papers_por_ano = {}
    
    for entrada in entradas:
        ano = entrada['year']
        if ano in papers_por_ano:
            papers_por_ano[ano] += 1
        else:
            papers_por_ano[ano] = 1
    
    # Ordena o dicionário por ano (chave) e converte em uma lista de tuplas
    papers_ordenados_por_ano = sorted(papers_por_ano.items())
    
    return papers_ordenados_por_ano

@anvil.server.callable
def top_journals_ultima_sessao():
    usuario_atual = anvil.users.get_user()
    ultima_sessao = app_tables.sessions.search(
        tables.order_by("upload_date", ascending=False),
        user=usuario_atual
    )[0]
    
    entradas = app_tables.bib_data.search(session=ultima_sessao)
    contador_journals = {}
    
    for entrada in entradas:
        journal = entrada['journal']
        if journal:
            contador_journals[journal] = contador_journals.get(journal, 0) + 1
    
    # Ordena o dicionário por contagem e pega os top 10
    top_journals = sorted(contador_journals.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return top_journals


@anvil.server.callable
def dados_keywords_por_ano_agregados():
    entradas = app_tables.bib_data.search(tables.order_by("year", ascending=True))
    contador_keywords_por_ano = {}

    # Inicializa os contadores por ano para as top 10 palavras-chave
    for entrada in entradas:
        ano = entrada['year']
        if ano and entrada['keywords']:
            keywords = entrada['keywords'].split(';')
            if ano not in contador_keywords_por_ano:
                contador_keywords_por_ano[ano] = Counter()
            contador_keywords_por_ano[ano].update([keyword.strip() for keyword in keywords if keyword])

    # Preparando a lista das top 10 palavras-chave globais
    contador_global = Counter()
    for contador in contador_keywords_por_ano.values():
        contador_global.update(contador)
    top_keywords = [kw for kw, _ in contador_global.most_common(10)]

    # Preparando dados finais agregados
    dados_agregados = []
    for ano, contador in contador_keywords_por_ano.items():
        dados_ano = {'year': ano}
        for kw in top_keywords:
            dados_ano[kw] = contador[kw]
        dados_agregados.append(dados_ano)

    return dados_agregados