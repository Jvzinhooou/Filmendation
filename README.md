# Sistema de Recomendação de Filmes com Flask

## Descrição do Projeto

### Problema
O objetivo deste projeto é desenvolver um sistema de recomendação de filmes utilizando a técnica de similaridade do cosseno. O sistema permite que o usuário insira o nome de um filme e, com base nisso, retorna uma lista de filmes similares. Esse tipo de recomendação pode ser útil para ajudar usuários a encontrar filmes que eles provavelmente irão gostar, com base em suas preferências passadas.

### Metodologia Utilizada
1. **Captura de Dados**: O usuário insere o nome de um filme na interface web.
2. **Manipulação de Dados**: Os dados dos filmes e suas avaliações são carregados de arquivos CSV.
3. **Processamento dos Dados**: 
   - Os dados são mesclados para criar uma tabela unificada.
   - Utiliza-se uma tabela dinâmica para preparar os dados para o cálculo de similaridade.
   - A similaridade do cosseno é calculada entre os filmes.
4. **Recomendação**: 
   - Verifica-se se o filme inserido está presente no banco de dados.
   - Retorna uma lista de filmes similares ordenados pela similaridade.
5. **Exibição dos Resultados**: Os resultados são exibidos em uma tabela HTML na interface web.

### Resultados Obtidos
O sistema é capaz de retornar uma lista de filmes similares ao filme inserido pelo usuário, mostrando as recomendações com a porcentagem de similaridade. 

### Conclusões
O projeto demonstra a viabilidade de utilizar técnicas de similaridade para criar sistemas de recomendação eficazes, utilizando bibliotecas de Python como pandas e scikit-learn para manipulação de dados e cálculos de similaridade.

## Código Fonte do Sistema de Recomendação

```python
from flask import Flask, render_template, request
import pandas as pd
import sklearn.metrics.pairwise as pw

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/time')
def team():
    return render_template('team.html')

@app.route('/receber', methods=['POST'])
def submit():
    input_usuario = request.form.get('nome_filme')
    print(f'Dado recebido: {input_usuario}')

    filmes = pd.read_csv('Filmes.csv', sep=',')
    ratings = pd.read_csv('Ratings.csv', sep=';')
    df = filmes.merge(ratings, on='movieId')

    tabela_filmes = pd.pivot_table(df, index='Título', columns='userId', values='rating').fillna(0)
    rec = pw.cosine_similarity(tabela_filmes)
    rec_df = pd.DataFrame(rec, columns=tabela_filmes.index, index=tabela_filmes.index)

    titulos_minusculos = [titulo.lower() for titulo in rec_df.index]
    if input_usuario.lower() in titulos_minusculos:
        titulo_original = rec_df.index[titulos_minusculos.index(input_usuario.lower())]
        print(type(rec_df.index.str.lower()))

        cossine_df = rec_df[titulo_original].sort_values(ascending=False).to_frame(name='Recomendação').reset_index()

        for index, row in cossine_df.iterrows():
            novo_valor = decimal_para_porcentagem(row['Recomendação'])
            cossine_df.at[index, 'Recomendação'] = novo_valor

        tabela_html = cossine_df.head(11).to_html(classes='', index=False)
        return render_template('resultado.html', tabela_html=tabela_html, input_usuario=input_usuario, erros=None)
    else:
        return render_template('resultado.html', tabela_html=None, input_usuario=input_usuario, erros=f'O filme "{input_usuario}" não foi encontrado na nossa base de dados.')

def decimal_para_porcentagem(decimal):
    porcentagem = decimal * 100
    return f"{porcentagem:.2f}%"

if __name__ == '__main__':
    app.run(debug=True)
```

### Comentários no Código
O código está organizado em funções claras e documentado para facilitar a compreensão. Cada parte do processo, desde a captura de dados do usuário até a exibição dos resultados, está separada em funções distintas, com comentários explicativos.

## Uso de Inteligência Artificial

### Similaridade do Cosseno
A técnica de similaridade do cosseno é usada para calcular a similaridade entre os filmes. Essa técnica é bastante utilizadas em sistemas de recomendação, pois auxilia a medir a similaridade entre dois vetores de maneira que se desconsidera a magnitude dos vetores, focando apenas na direção.

### Bibliotecas Utilizadas
- **Pandas**: Para manipulação de dados e criação de tabelas dinâmicas.
- **Scikit-learn**: Para cálculo da similaridade do cosseno.
- **Flask**: Para integração entre Front-End e Back-End, além do auxílio na criação das rotas e estilização da Web.


