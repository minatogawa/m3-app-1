import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
import bibtexparser
from datetime import datetime
import anvil.users

@anvil.server.callable
def process_and_store_bibtex(blob_media):
    current_user = anvil.users.get_user()
    new_session = app_tables.sessions.add_row(user=current_user, upload_date=datetime.now())
    bibtex_str = blob_media.get_bytes().decode()
    bibtex_database = bibtexparser.loads(bibtex_str)

    for entry in bibtex_database.entries:
        app_tables.bib_data.add_row(session=new_session, **entry)

    return "Data processed and stored successfully."

@anvil.server.callable
def fetch_last_session_data():
    current_user = anvil.users.get_user()
    last_session = app_tables.sessions.search(tables.order_by("upload_date", descending=True), user=current_user)[0]
    entries = app_tables.bib_data.search(session=last_session)
    return [{"author": e["author"], "title": e["title"], "year": e["year"], "journal": e["journal"], "doi": e["doi"], "keywords": e["keywords"]} for e in entries]

@anvil.server.callable
def fetch_papers_per_year():
    current_user = anvil.users.get_user()
    last_session = app_tables.sessions.search(tables.order_by("upload_date", descending=True), user=current_user)[0]
    entries = app_tables.bib_data.search(session=last_session)
    papers_per_year = {}
    for entry in entries:
        year = entry["year"]
        papers_per_year[year] = papers_per_year.get(year, 0) + 1
    return sorted(papers_per_year.items())

@anvil.server.callable
def fetch_top_journals():
    current_user = anvil.users.get_user()
    last_session = app_tables.sessions.search(tables.order_by("upload_date", descending=True), user=current_user)[0]
    entries = app_tables.bib_data.search(session=last_session)
    journal_counts = {}
    for entry in entries:
        journal = entry["journal"]
        if journal:
            journal_counts[journal] = journal_counts.get(journal, 0) + 1
    top_journals = sorted(journal_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    return top_journals

@anvil.server.callable
def fetch_keywords_data():
    current_user = anvil.users.get_user()
    last_session = app_tables.sessions.search(tables.order_by("upload_date", descending=True), user=current_user)[0]
    entries = app_tables.bib_data.search(session=last_session)
    
    # Organiza as palavras-chave por ano
    keywords_by_year = {}
    for entry in entries:
        year = entry["year"]
        if year and entry["keywords"]:
            keywords_list = [kw.strip() for kw in entry["keywords"].split(";")]
            if year not in keywords_by_year:
                keywords_by_year[year] = {}
            for keyword in keywords_list:
                if keyword in keywords_by_year[year]:
                    keywords_by_year[year][keyword] += 1
                else:
                    keywords_by_year[year][keyword] = 1
    
    # Calcula as palavras-chave mais comuns ao longo de todos os anos
    all_keywords = {}
    for year, keywords in keywords_by_year.items():
        for keyword, count in keywords.items():
            if keyword in all_keywords:
                all_keywords[keyword] += count
            else:
                all_keywords[keyword] = count
    
    top_keywords = sorted(all_keywords, key=all_keywords.get, reverse=True)[:10]
    
    # Prepara os dados para o streamgraph
    stream_data = []
    for year in sorted(keywords_by_year.keys()):
        year_data = {"year": year}
        for keyword in top_keywords:
            year_data[keyword] = keywords_by_year[year].get(keyword, 0)
        stream_data.append(year_data)
    
    return stream_data