from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import plotly.graph_objs as go



class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    # Preenche o Data Grid com dados
    self.preencher_data_grid()

  def button_logout_click(self, **event_args):
    # Encerra a sessão do usuário atual
    anvil.users.logout()
    
    # Redireciona o usuário de volta ao Form1 (tela de login)
    anvil.open_form('signin_signup')

  def file_loader_1_change(self, file, **event_args):
    # Salva o arquivo carregado em uma variável de instância para uso posterior
    self.loaded_file = file
    # Torna o botão de processamento visível
    self.process_archive.visible = True

  # No evento de clique do botão (para processar o arquivo .bib)
  def process_archive_click(self, **event_args):
    if self.loaded_file:
      # Chama a função do servidor para processar e armazenar os dados do arquivo .bib
      resultado = anvil.server.call('processar_bibtex_e_armazenar', self.loaded_file)
      # Exibe uma mensagem de confirmação
      alert(resultado)
      # Atualiza o repeating panel com os novos dados processados
      self.preencher_data_grid()  # Ou self.mostrar_dados(), dependendo da função que você está usando.
      # Torna o Data Grid visível
      self.data_grid.visible = True
    else:
      alert("Nenhum arquivo foi carregado. Por favor, carregue um arquivo .bib para processar.")
    self.desenhar_grafico()
    self.desenhar_grafico_top_journals()
    self.desenhar_streamgraph_keywords()


  def mostrar_dados(self):
    dados = anvil.server.call('buscar_dados')
    self.data_grid.items = dados  # Atualiza o Data Grid com os dados recebidos
    
  def preencher_data_grid(self):
    try:
        # Chama a função do servidor para buscar os dados da última sessão
        dados = anvil.server.call('buscar_dados_da_ultima_sessao')
        # Atualiza os itens do Data Grid diretamente com os dados
        self.repeating_panel_1.items = dados
    except Exception as e:
        print(e)  # Isso imprimirá o erro no console de execução

  def desenhar_grafico(self):
        dados_grafico = anvil.server.call('dados_papers_ultima_sessao_por_ano')

        # Cria as coordenadas X e Y para o gráfico
        anos = [ano for ano, _ in dados_grafico]
        contagem_papers = [contagem for _, contagem in dados_grafico]
        
        # Cria o gráfico
        data = [go.Bar(x=anos, y=contagem_papers)]
        layout = go.Layout(title='Papers published per year')
        fig = go.Figure(data=data, layout=layout)

        # Exibe o gráfico no Plot component
        self.plot_1.data = fig.data
        self.plot_1.layout = fig.layout

  def desenhar_grafico_top_journals(self):
    top_journals = anvil.server.call('top_journals_ultima_sessao')

    # Define uma lista de cores para as barras
    cores_barras = [
        'rgba(255, 99, 132, 0.5)',  # Por exemplo, um tom de vermelho com transparência
        'rgba(54, 162, 235, 0.5)',  # Azul
        'rgba(255, 206, 86, 0.5)',  # Amarelo
        # ... Adicione mais cores conforme necessário
    ]

    # Certifique-se de que temos cores suficientes para todas as barras
    cores_barras = cores_barras * (len(top_journals) // len(cores_barras) + 1)

    # Cria as coordenadas X e Y para o gráfico
    nomes_journals = [journal.replace(' ', '<br>') for journal, _ in top_journals]
    contagem_papers = [contagem for _, contagem in top_journals]

    # Cria o gráfico de barras com cores personalizadas
    data = [go.Bar(
        x=nomes_journals,
        y=contagem_papers,
        marker=dict(color=cores_barras[:len(top_journals)])  # Aplica as cores às barras
    )]
    
    layout = go.Layout(
        title='Top 10 Journals com Mais Publicações',
        xaxis={
            'title': 'Journal',
            'tickangle': 0,  # Sem inclinação
            'tickmode': 'array',
            'tickvals': list(range(len(nomes_journals))),
            'ticktext': nomes_journals  # Rótulos personalizados com quebra de linha
        },
        yaxis={'title': 'Número de Publicações'},
        margin={'l': 50, 'r': 50, 't': 50, 'b': 100},  # Ajusta as margens
    )
    fig = go.Figure(data=data, layout=layout)

    # Exibe o gráfico no componente Plot
    self.plot_2.data = fig.data
    self.plot_2.layout = fig.layout


  def desenhar_streamgraph_keywords(self):
    # Chama a função do backend para obter os dados
    dados_keywords = anvil.server.call('dados_keywords_por_ano')

    # Assume que os dados vêm com as top 10 palavras-chave
    years = [dado['year'] for dado in dados_keywords]
    series = {keyword: [] for keyword in dados_keywords[0].keys() if keyword != 'year'}

    for dado in dados_keywords:
        for keyword, value in dado.items():
            if keyword != 'year':
                series[keyword].append(value)

    # Agora temos os dados prontos para serem adicionados ao gráfico
    data = []
    for keyword, values in series.items():
        data.append(go.Scatter(
            x=years,
            y=values,
            mode='lines',
            line=dict(shape='spline', smoothing=1.3),
            stackgroup='one',
            name=keyword
        ))

    # Cria e configura o gráfico
    fig = go.Figure(data=data)
    fig.update_layout(
        title='Evolução das Palavras-Chave ao Longo dos Anos - Top 10',
        xaxis_title='Ano',
        yaxis_title='Frequência',
        showlegend=True
    )

    # Exibe o gráfico no componente Plot
    self.plot_3.data = fig.data
    self.plot_3.layout = fig.layout