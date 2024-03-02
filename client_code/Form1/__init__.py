# Importações e Classe Form1
from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go
import anvil.server

class Form1(Form1Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.fill_data_grid()

    def logout_button_click(self, **event_args):
        anvil.users.logout()
        anvil.open_form('signin_signup')

    def file_loader_change(self, file, **event_args):
        self.loaded_file = file
        self.process_file_button.visible = True

    def process_file_button_click(self, **event_args):
        if self.loaded_file:
            result = anvil.server.call('process_bibtex_and_store', self.loaded_file)
            alert(result)
            self.fill_data_grid()
            self.data_grid.visible = True
        else:
            alert("No file loaded. Please upload a .bib file to process.")
        self.draw_chart()
        self.draw_top_journals_chart()
        self.draw_keywords_streamgraph()

    def fill_data_grid(self):
        try:
            data = anvil.server.call('fetch_last_session_data')
            self.repeating_panel_1.items = data
        except Exception as e:
            print(e)

    def draw_generic_chart(self, data, layout, plot_component):
        fig = go.Figure(data=data, layout=layout)
        plot_component.data = fig.data
        plot_component.layout = fig.layout

    def draw_chart(self):
        chart_data = anvil.server.call('fetch_papers_per_year')
        years = [year for year, _ in chart_data]
        paper_counts = [count for _, count in chart_data]
        data = [go.Bar(x=years, y=paper_counts)]
        layout = go.Layout(title='Papers Published Per Year')
        self.draw_generic_chart(data, layout, self.plot_1)

    def draw_top_journals_chart(self):
        top_journals = anvil.server.call('fetch_top_journals')
        colors = ['rgba(255, 99, 132, 0.5)', 'rgba(54, 162, 235, 0.5)', 'rgba(255, 206, 86, 0.5)']
        colors *= (len(top_journals) // len(colors) + 1)
        journal_names = [journal.replace(' ', '<br>') for journal, _ in top_journals]
        paper_counts = [count for _, count in top_journals]
        data = [go.Bar(x=journal_names, y=paper_counts, marker=dict(color=colors[:len(top_journals)]))]
        layout = go.Layout(
            title='Top 10 Journals by Number of Publications',
            xaxis=dict(title='Journal', tickangle=0, tickmode='array', tickvals=list(range(len(journal_names))), ticktext=journal_names),
            yaxis=dict(title='Number of Publications'),
            margin=dict(l=50, r=50, t=50, b=100)
        )
        self.draw_generic_chart(data, layout, self.plot_2)

    def draw_keywords_streamgraph(self):
        keywords_data = anvil.server.call('fetch_keywords_data_by_year')
        years = [data['year'] for data in keywords_data]
        series = {keyword: [] for keyword in keywords_data[0].keys() if keyword != 'year'}
        for data in keywords_data:
            for keyword, value in data.items():
                if keyword != 'year':
                    series[keyword].append(value)
        data = [go.Scatter(x=years, y=values, mode='lines', line=dict(shape='spline', smoothing=1.3), stackgroup='one', name=keyword) for keyword, values in series.items()]
        layout = go.Layout(
            title='Keywords Evolution Over Years - Top 10',
            xaxis_title='Year',
            yaxis_title='Frequency',
            showlegend=True
        )
        self.draw_generic_chart(data, layout, self.plot_3)


# Server-side Functions (Placeholder)
# As funções do lado do servidor, como 'process_bibtex_and_store', 'fetch_last_session_data', 'fetch_papers_per_year', 'fetch_top_journals', e 'fetch_keywords_data_by_year' devem ser atualizadas no servidor Anvil para corresponder aos novos nomes e estruturas.






