import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
import bibtexparser
from datetime import datetime
from collections import Counter

@anvil.server.callable
def process_bibtex_and_store(blob_media):
    current_user = anvil.users.get_user()
    new_session = app_tables.sessions.add_row(
        user=current_user,
        upload_date=datetime.now()
    )

    bibtex_str = blob_media.get_bytes().decode()
    bibtex_database = bibtexparser.loads(bibtex_str)

    for entry in bibtex_database.entries:
        entry_dict = {key: str(value) if value else None for key, value in entry.items()}
        app_tables.bib_data.add_row(
            session=new_session,
            author=entry_dict.get('author'),
            title=entry_dict.get('title'),
            year=entry_dict.get('year'),
            journal=entry_dict.get('journal'),
            doi=entry_dict.get('doi'),
            keywords=entry_dict.get('keywords'),
            correspondence_address=entry_dict.get('address'),
            publisher=entry_dict.get('publisher')
        )

    return "Data processed and stored successfully for the session."

@anvil.server.callable
def fetch_last_session_data():
    current_user = anvil.users.get_user()
    last_session = app_tables.sessions.search(
        tables.order_by("upload_date", ascending=False),
        user=current_user
    )[0]
    
    session_entries = app_tables.bib_data.search(session=last_session)
    data = [{
        'author': entry['author'],
        'title': entry['title'],
        'year': entry['year'],
        'journal': entry['journal'],
        'doi': entry['doi'],
        'keywords': entry['keywords'],
        'correspondence_address': entry['correspondence_address'],
        'publisher': entry['publisher']
    } for entry in session_entries]
    
    return data

@anvil.server.callable
def fetch_papers_per_year():
    current_user = anvil.users.get_user()
    last_session = app_tables.sessions.search(
        tables.order_by("upload_date", ascending=False),
        user=current_user
    )[0]

    entries = app_tables.bib_data.search(session=last_session)
    papers_per_year = Counter([entry['year'] for entry in entries if entry['year']])

    sorted_papers_per_year = sorted(papers_per_year.items())
    return sorted_papers_per_year

@anvil.server.callable
def fetch_top_journals():
    current_user = anvil.users.get_user()
    last_session = app_tables.sessions.search(
        tables.order_by("upload_date", ascending=False),
        user=current_user
    )[0]
    
    entries = app_tables.bib_data.search(session=last_session)
    journal_counter = Counter([entry['journal'] for entry in entries if entry['journal']])
    
    top_journals = journal_counter.most_common(10)
    return top_journals

@anvil.server.callable
def fetch_keywords_data_by_year():
    entries = app_tables.bib_data.search(tables.order_by("year", ascending=True))
    keyword_counter = Counter()
    
    for entry in entries:
        if entry['keywords']:
            keywords = [keyword.strip() for keyword in entry['keywords'].split(';')]
            keyword_counter.update(keywords)
    
    top_keywords = [keyword for keyword, _ in keyword_counter.most_common(10)]
    data_by_year = {year: {kw: 0 for kw in top_keywords} for year in sorted(set(entry['year'] for entry in entries))}

    for entry in entries:
        year = entry['year']
        if year and entry['keywords']:
            entry_keywords = [keyword.strip() for keyword in entry['keywords'].split(';')]
            for keyword in entry_keywords:
                if keyword in top_keywords:
                    data_by_year[year][keyword] += 1

    stream_data = [{'year': year, **counts} for year, counts in data_by_year.items()]
    return stream_data
