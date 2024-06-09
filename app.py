from flask import Flask, render_template, request # Importando o Flask para manipulação em HTML
import pandas as pd # Importando o pandas para manipulação de dataframe
import sklearn.metrics.pairwise as pw # Biblioteca de machine learning

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/time')
def team():
    return render_template('team.html')

# CAPTURA E MANIPULAÇÃO DOS DADOS DA PÁGINA HTML
# ----------------------------------------------------------------------------------------------------------------------
@app.route('/receber', methods=['POST'])  # Criando um caminho para acessar os dados enviados pelo usuário
def submit():  # Def para o recebimento dos dados
    # Capturando dados do input
    input_usuario = request.form.get('nome_filme')  # Atribuindo a uma variável o dado(str) preenchido no input 'nome_filme' na pág HTML

    # Processando os dados (exibindo no terminal)
    print(f'Dado recebido: {input_usuario}')

    # Usando o pandas para ler os CSVs
    filmes = pd.read_csv('Filmes.csv', sep=',')
    ratings = pd.read_csv('Ratings.csv', sep=';')

    # Unindo a tabela filmes e a tabela ratings pela coluna movieId
    df = filmes.merge(ratings, on='movieId')

    # PERSONALIZA A TABELA FILMES EM "VETOR"
    tabela_filmes = pd.pivot_table(df, index='Título', columns='userId', values='rating').fillna(0)

    # CRIA NOVA VARIÁVEL PARA ADICIONAR A TABELA_FILMES À FÓRMULA MATEMÁTICA DO COSSENO
    rec = pw.cosine_similarity(tabela_filmes)
    rec_df = pd.DataFrame(rec, columns=tabela_filmes.index, index=tabela_filmes.index)

    # Verificando se o filme de entrada está na tabela
    titulos_minusculos = [titulo.lower() for titulo in rec_df.index]
    if input_usuario.lower() in titulos_minusculos:
        # Encontrando o título original do filme
        titulo_original = rec_df.index[titulos_minusculos.index(input_usuario.lower())]
        print(type(rec_df.index.str.lower()))

        # Ordenando os filmes pela similaridade com o filme de entrada.
        cossine_df = rec_df[titulo_original].sort_values(ascending=False).to_frame(name='Recomendação').reset_index()
        
        for index, row in cossine_df.iterrows():
            # Modificar o valor da coluna "Recomendação" para o dobro do valor atual.
            novo_valor = decimal_para_porcentagem(row['Recomendação'])
            cossine_df.at[index, 'Recomendação'] = novo_valor

        # Convertendo o DataFrame para HTML
        tabela_html = cossine_df.head(11).to_html(classes='', index=False)

        # Retornando a resposta com a tabela HTML e confirmando se há erros ou não.
        return render_template('resultado.html', tabela_html=tabela_html, input_usuario=input_usuario, erros=None)
    else:
        return render_template('resultado.html', tabela_html=None, input_usuario=input_usuario, erros=f'O filme "{input_usuario}" não foi encontrado na nossa base de dados.')

# Criação de função para transformação da similaridade para porcentagem.
def decimal_para_porcentagem(decimal):
    porcentagem = decimal * 100
    return f"{porcentagem:.2f}%"

print("")

#Subir alterações de código automaticamente.
if __name__ == '__main__':
    app.run(debug=True)
