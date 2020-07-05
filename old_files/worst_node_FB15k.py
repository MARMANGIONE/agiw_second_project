import pandas as pd
import requests
from bs4 import BeautifulSoup
df=pd.read_csv('data/FB15k/ComplEx/complex_filtered_ranks.csv',sep=';',names=['head','relation','tail','head_rank','tail_rank'])
df2=pd.read_csv('data/FB15k-237/ComplEx/complex_filtered_ranks.csv',sep=';',names=['head','relation','tail','head_rank_2','tail_rank_2'])
df_train237 = pd.read_csv('data/FB15k-237/train_FB15k-237.csv', sep='\t', names=['head', 'relation', 'tail'])
df_train = pd.read_csv('data/FB15k/train_FB15k.csv', sep='\t', names=['head', 'relation', 'tail'])
def degree_node(node):
    return df_train[df_train['head'] == node].shape[0] + df_train[df_train['tail'] == node].shape[0]

def degree_node_237(node):
    return df_train237[df_train237['head'] == node].shape[0] + df_train237[df_train237['tail'] == node].shape[0]

def recover_name_fb15k(node):
    html_doc = requests.get('https://cofactor.io/'+ node).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    h1 = soup.find_all('h1')
    return h1[0].text
#prendo solo l'intersezione dei due dataframe, in modo che ho solo i fatti presenti nel KG filtrato
intersection = pd.merge(df, df2, how='inner', on=['head', 'relation','tail'])
#seleziono le righe che hanno head rank o tail rank differenti
different_ranks=intersection[(intersection['head_rank']!=intersection['head_rank_2'])|(intersection['tail_rank']!=intersection['tail_rank_2'])]
serieDifferenze_tail=different_ranks['tail_rank_2']-different_ranks['tail_rank'] #faccio la differenza tra il tail rank del KG filtrato meno il tail rank del KG non filtrato
stdTail=pd.DataFrame.std(different_ranks['tail_rank_2']-different_ranks['tail_rank'])  #calcolo la deviazione standard
worst_result_tail=serieDifferenze_tail[serieDifferenze_tail>stdTail]  #prendo solo i punteggi che sono peggiorati maggiormente

#faccio lo stesso per le head
serieDifferenze_head=different_ranks['head_rank_2']-different_ranks['head_rank']
std_head=pd.DataFrame.std(different_ranks['head_rank_2']-different_ranks['head_rank'])
worst_result_head=serieDifferenze_head[serieDifferenze_head>std_head]
worst_result_tail=worst_result_tail.sort_values(ascending=False)
worst_result_head=worst_result_head.sort_values(ascending=False)
worst_result_head = worst_result_head.head(20)
worst_result_tail= worst_result_tail.head(20)
print(worst_result_tail)
print(worst_result_head)
index_list=worst_result_tail.index.values.tolist()
for index in index_list:
    head=intersection.loc[ index, : ]['head']
    tail=intersection.loc[ index, : ]['tail']
    relation=intersection.loc[ index, : ]['relation']
    nome_head=recover_name_fb15k(head)
    nome_tail=recover_name_fb15k(tail)
    degreehead237=degree_node_237(head)
    degreetail237=degree_node_237(tail)
    if(degreehead237!=0 and degreetail237!=0 and nome_head != '❔' and nome_tail != '❔'):
        print(index,'---', nome_head,'(',head,')','--->', degreehead237,'---',relation,'---', nome_tail,'(',tail,')','--->', degreetail237,'FB15k-237')
        print(index, '---', nome_head,'(',head,')', '--->', degree_node(head), '---',relation,'---', nome_tail,'(',tail,')', '--->', degree_node(tail),'FB15k')
        print(' ')
#print(df_train237[df_train237['head'] == intersection.loc[17018, :]['head']].shape[0])
#print(intersection.loc[ 17018, : ])


