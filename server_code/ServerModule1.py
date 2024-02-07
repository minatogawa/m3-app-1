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
    try:
        usuario_atual = anvil.users.get_user()
        ultima_sessao = app_tables.sessions.search(
            tables.order_by("upload_date", ascending=False),
            user=usuario_atual
        )[0]  # Pode lançar IndexError se não houver sessões

        entradas_da_ultima_sessao = app_tables.bib_data.search(session=ultima_sessao)
        dados = [{
            'author': entrada['author'],
            'title': entrada['title'],
            'year': entrada['year'],
            'journal': entrada['journal'],
            'doi': entrada['doi'],
            'keywords': entrada['keywords'],
            'correspondence_address': entrada.get('correspondence_address', None),  # Use .get() para campos opcionais
            'publisher': entrada['publisher']
            # Inclua outros campos conforme necessário
        } for entrada in entradas_da_ultima_sessao]
        return dados
    except IndexError:
        return []  # Retorna lista vazia se não houver sessões

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
def dados_keywords_por_ano():
    # Busca todas as entradas na tabela bib_data
    entradas = app_tables.bib_data.search(tables.order_by("year", ascending=True))

    # Inicializa um contador para todas as palavras-chave
    contador_keywords = Counter()

    # Conta a frequência de cada palavra-chave
    for entrada in entradas:
        if entrada['keywords']:
            keywords = entrada['keywords'].split(';')
            contador_keywords.update([keyword.strip() for keyword in keywords if keyword])

    # Seleciona as top 10 palavras-chave mais frequentes
    top_keywords = [keyword for keyword, count in contador_keywords.most_common(10)]

    # Inicializa o dicionário de dados para o streamgraph
    dados_stream = {ano: {kw: 0 for kw in top_keywords} for ano in sorted(set(entrada['year'] for entrada in entradas))}

    # Conta as palavras-chave apenas se estiverem no top 10
    for entrada in entradas:
        ano = entrada['year']
        if ano and entrada['keywords']:
            for keyword in entrada['keywords'].split(';'):
                keyword = keyword.strip()
                if keyword in top_keywords:
                    dados_stream[ano][keyword] += 1

    # Prepara os dados para o streamgraph
    stream_data = [{'year': ano, **counts} for ano, counts in dados_stream.items()]

    return stream_data