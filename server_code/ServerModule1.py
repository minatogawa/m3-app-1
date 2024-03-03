import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import bibtexparser
import io
from datetime import datetime
from collections import Counter

################################################################################################

@anvil.server.callable
def process_bibtex_and_store(blob_media):
    # Retrieves the current user.
    current_user = anvil.users.get_user()

    # Creates a new session for this upload.
    new_session = app_tables.sessions.add_row(
        user=current_user,
        upload_date=datetime.now()  # Gets the current date and time.
    )

    # Reads the file as a string.
    bibtex_str = blob_media.get_bytes().decode()
    # Uses bibtexparser.parse_string to process the BibTeX string.
    bibtex_database = bibtexparser.parse_string(bibtex_str)

    # Processes and stores each entry in the BibTeX file.
    for entry in bibtex_database.entries:
        entry_dict = {key: str(value) if value else None for key, value in entry.items()}
        
        app_tables.bib_data.add_row(
            session=new_session,
            author=entry_dict.get('author', None),
            title=entry_dict.get('title', None),
            year=entry_dict.get('year', None),
            journal=entry_dict.get('journal', None),
            doi=entry_dict.get('doi', None),
            keywords=entry_dict.get('keywords', None),
            correspondence_address=entry_dict.get('address', None),  # If 'address' is the correct field.
            publisher=entry_dict.get('publisher', None)
            # Add any other fields as necessary.
        )

    # Returns a confirmation message.
    return "Data processed and stored successfully for the session."

########################################################################################################################

@anvil.server.callable
def fetch_data_from_last_session():
    print("Starting to fetch data from the last session")
    current_user = anvil.users.get_user()
    
    # Finds the last session by ordering by 'upload_date' and taking the first one.
    last_session = app_tables.sessions.search(
        tables.order_by("upload_date", ascending=False),
        user=current_user
    )[0]
    
    # Searches for entries associated with the last session.
    entries_from_last_session = app_tables.bib_data.search(
        session=last_session
    )
    
    # Converts the entries into dictionaries to pass to the front end.
    data = [{
        'author': entry['author'],
        'title': entry['title'],
        'year': entry['year'],
        'journal': entry['journal'],
        'doi': entry['doi'],
        'keywords': entry['keywords'],
        'correspondence_address': entry['correspondence_address'],
        'publisher': entry['publisher']
    } for entry in entries_from_last_session]
    
    return data

#################PAPERS PER YEAR###########################################################################################

@anvil.server.callable
def fetch_data_last_session_by_year():
    # Retrieves the current user.
    current_user = anvil.users.get_user()
    # Finds the last session by sorting the sessions by 'upload_date' in descending order and selects the first one.
    last_session = app_tables.sessions.search(
        tables.order_by("upload_date", ascending=False),
        user=current_user
    )[0]

    # Searches for entries in the 'bib_data' table associated with the last session.
    entries = app_tables.bib_data.search(session=last_session)
    papers_by_year = {}
    
    # Iterates over each entry and counts the number of papers per year.
    for entry in entries:
        year = entry['year']
        if year in papers_by_year:
            papers_by_year[year] += 1
        else:
            papers_by_year[year] = 1
    
    # Sorts the dictionary by year (key) and converts it into a list of tuples.
    sorted_papers_by_year = sorted(papers_by_year.items())
    
    return sorted_papers_by_year
#######TOP JOURNALS###################################

@anvil.server.callable
def fetch_top_journals_last_session():
    # Retrieves the current user.
    current_user = anvil.users.get_user()
    # Finds the last session by sorting the sessions by 'upload_date' in descending order and selects the first one.
    last_session = app_tables.sessions.search(
        tables.order_by("upload_date", ascending=False),
        user=current_user
    )[0]
    
    # Searches for entries in the 'bib_data' table associated with the last session.
    entries = app_tables.bib_data.search(session=last_session)
    journal_counter = {}
    
    # Iterates over each entry and counts occurrences of each journal.
    for entry in entries:
        journal = entry['journal']
        if journal:
            journal_counter[journal] = journal_counter.get(journal, 0) + 1
    
    # Sorts the dictionary by count and retrieves the top 10 journals.
    top_journals = sorted(journal_counter.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return top_journals

########KEYWORDS EVOLUTION#####################################################################################################

@anvil.server.callable
def fetch_keywords_by_year():
    # Searches for all entries in the 'bib_data' table, ordered by year.
    entries = app_tables.bib_data.search(tables.order_by("year", ascending=True))

    # Initializes a counter for all keywords.
    keyword_counter = Counter()

    # Counts the frequency of each keyword.
    for entry in entries:
        if entry['keywords']:
            keywords = entry['keywords'].split(';')
            keyword_counter.update([keyword.strip() for keyword in keywords if keyword])

    # Selects the top 10 most frequent keywords.
    top_keywords = [keyword for keyword, count in keyword_counter.most_common(10)]

    # Initializes the data dictionary for the streamgraph.
    stream_data = {year: {kw: 0 for kw in top_keywords} for year in sorted(set(entry['year'] for entry in entries))}

    # Counts the keywords only if they are in the top 10.
    for entry in entries:
        year = entry['year']
        if year and entry['keywords']:
            for keyword in entry['keywords'].split(';'):
                keyword = keyword.strip()
                if keyword in top_keywords:
                    stream_data[year][keyword] += 1

    # Prepares the data for the streamgraph.
    stream_graph_data = [{'year': year, **counts} for year, counts in stream_data.items()]

    return stream_graph_data