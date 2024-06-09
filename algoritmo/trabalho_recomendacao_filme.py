import csv #importando nosso csv
import pandas as pd #importando o pandas para manipulação de dataframe
import sklearn.metrics.pairwise as pw #biblioteca de machinelearne


#CSV INPORTADO DO MOVIELENS

filmes = pd.read_csv('Filmes.csv', sep=',') #importando o csv filmes
ratings = pd.read_csv('Ratings.csv',sep=';') #importando o csv ratings

#Unindo a tabela filmes e a tabela ratings pela coluna movieId
df = filmes.merge(ratings, on='movieId')

#PERSONALIZA A TABELA FILMES EM EM "VETOR"
tabela_filmes= pd.pivot_table(df, index='title',columns='userId',values='rating').fillna(0)

#CRIA NOVA VARIAVEL PARA ADICIONA A TABELA_FILMES A FORMULA MATEMÁTICA DO COSSENO 
rec = pw.cosine_similarity(tabela_filmes)
rec_df = pd.DataFrame(rec, columns=tabela_filmes.index,index=tabela_filmes.index)
rec_df.head()

cossine_df = rec_df['Thor'].sort_values(ascending=False)
cossine_df.colums=['Recomendação']
cossine_df.head()
