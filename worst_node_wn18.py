import pandas as pd
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import WordNetError


df=pd.read_csv('data/WN18/ComplEx/complex_filtered_ranks.csv',sep=';',names=['head','relation','tail','head_rank','tail_rank'])
df2=pd.read_csv('data/WN18RR/ComplEx/complex_filtered_ranks.csv',sep=';',names=['head','relation','tail','head_rank_2','tail_rank_2'])
df_trainRR = pd.read_csv('data/WN18RR/train_WN18RR.csv', sep='\t', names=['head', 'relation', 'tail'])
df_train = pd.read_csv('data/WN18/train_WN18.csv', sep='\t', names=['head', 'relation', 'tail'])


# POICHE' IL GRAFO NON E' DIREZIONATO PER OGNI NODO IL GRADO SI CALCOLA OSSSERVANDO SIA GLI ARCHI ENTRANTI SIA GLI ARCHI USCENTI
def degree_node(node):
    degree_head = df_train[df_train['head'] == node].shape[0]
    degree_tail = df_train[df_train['tail'] == node].shape[0]
    return degree_head + degree_tail

def degree_node_RR(node):
    degree_head = df_trainRR[df_trainRR['head'] == node].shape[0]
    degree_tail = df_trainRR[df_trainRR['tail'] == node].shape[0]
    return degree_head + degree_tail



def recover_name_wn(node):
    try:
  # 00144722:
        node_name = wn.synset_from_pos_and_offset('n', node)._lemma_names[0]
        return node_name
    except WordNetError as e:
        print(e)
        print(node)
        pass



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
node_0_degree_set = set()
for index in index_list:
    head=intersection.loc[ index, : ]['head']
    tail=intersection.loc[ index, : ]['tail']
    relation=intersection.loc[ index, : ]['relation']
    nome_head=recover_name_wn(head)
    nome_tail=recover_name_wn(tail)
    degreeheadRR=degree_node_RR(head)
    degreetailRR=degree_node_RR(tail)
    if(degreeheadRR!=0 and degreetailRR!=0):
        print(index,'---', nome_head,'(',head,')','--->', degreeheadRR,'---',relation,'---', nome_tail,'(',tail,')','--->', degreetailRR,'WN18')
        print(index, '---', nome_head,'(',head,')', '--->', degree_node(head), '---',relation,'---', nome_tail,'(',tail,')', '--->', degree_node(tail),'WN18RR')
        print(' ')
    elif degreeheadRR == 0:
        node_0_degree_set.add(head)
    else:
        node_0_degree_set.add(tail)



