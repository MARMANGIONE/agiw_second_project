import pandas as pd
import requests
from bs4 import BeautifulSoup
import dfs_portatile_filtered
import check_reverse_fact
import matplotlib.pyplot as plt
import numpy as np
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import WordNetError

df = pd.read_csv('data/WN18/ComplEx/complex_filtered_ranks.csv', sep=';',
                 names=['head', 'relation', 'tail', 'head_rank', 'tail_rank'])
df2 = pd.read_csv('data/WN18RR/ComplEx/complex_filtered_ranks.csv', sep=';',
                  names=['head', 'relation', 'tail', 'head_rank_2', 'tail_rank_2'])
df_train237 = pd.read_csv('data/WN18RR/train_WN18RR.csv', sep='\t', names=['head', 'relation', 'tail'])
df_train = pd.read_csv('data/WN18/train_WN18.csv', sep='\t', names=['head', 'relation', 'tail'])


def degree(node):
    return df_train[df_train['head'] == node].shape[0] + df_train[df_train['tail'] == node].shape[0]


def degree_237(node):
    return df_train237[df_train237['head'] == node].shape[0] + df_train237[df_train237['tail'] == node].shape[0]


def recover_name_wn18(node):
    try:
        node_name = wn.synset_from_pos_and_offset('n', node)._lemma_names[0]
        return node_name
    except WordNetError as e:
        print(e)
        print(node)
        pass


# prendo solo l'intersezione dei due dataframe, in modo che ho solo i fatti presenti nel KG filtrato

intersection = pd.merge(df, df2, how='inner', on=['head', 'relation', 'tail'])
# seleziono le righe che hanno head rank o tail rank differenti
different_ranks = intersection[(intersection['head_rank'] != intersection['head_rank_2'])
                               | (intersection['tail_rank'] != intersection['tail_rank_2'])]
serieDifferenze_tail = different_ranks['tail_rank_2'] - different_ranks['tail_rank']
different_ranks['rank_difference_tail'] = different_ranks['tail_rank_2'] - different_ranks[
    'tail_rank']  # faccio la differenza tra il tail rank del KG filtrato meno il tail rank del KG non filtrato
# prendo solo i punteggi che sono peggiorati maggiormente

# faccio lo stesso per le head

"""
different_ranks['have_inv'] = np.zeros(different_ranks.shape[0])

newDataFrame = pd.DataFrame(columns=different_ranks.columns.values)
print(newDataFrame)

for index, row in different_ranks.iterrows():
    row['have_inv']=check_reverse_fact.have_reverse(row['tail'],row['head'],df_train )
    newDataFrame = newDataFrame.append(row)


newDataFrame.to_csv('different_rank.csv')
"""


different_ranks = pd.read_csv('different_rank.csv', sep=',')
serieDifferenze_head = different_ranks['head_rank_2'] - different_ranks['head_rank']

bins = np.arange(-2000,50000,200)
out = pd.cut(serieDifferenze_head, bins=bins, include_lowest=True)

frame = {'have_inv': different_ranks['have_inv'], 'intervallo': out}

result = pd.DataFrame(frame)
result = result.dropna()
result.to_csv('result_csv_specifico.csv')

# ----------------------------------------------------------------
# result = pd.read_csv('result_csv_specifico.csv', sep=',')
# ----------------------------------------------------------------

listaIntervalli = result['intervallo'].sort_values().unique()

listaPercentuali = []

for intervallo in listaIntervalli:
    print(intervallo)
    resultIntervallo = result[result['intervallo'] == intervallo]
    percentualeIntervallo = (resultIntervallo[resultIntervallo['have_inv'] == 1].shape[0] / resultIntervallo.shape[
        0]) * 100
    listaPercentuali.append(percentualeIntervallo)

plt.style.use('ggplot')
print((listaIntervalli))
x_pos = [i for i, _ in enumerate(listaIntervalli)]
print(x_pos)
plt.bar(x_pos, listaPercentuali, color='green')
plt.savefig('inverse-tail.png', transparent=True)
plt.show()


""" different_ranks.apply( lambda x : x.have_inv=check_reverse_fact.have_reverse(x['tail'],x['head'],df_train ), axis=1 ) """

"""
100%
..
30% 
20%
10%  

       bins = np.arange(0,14000,100)

percentuale di uno=100*(numero di relazioni che non hanno l'inversa)/numero di relazioni
percentuale di un intervallo = percentuale di tutti/numero di tutti

 """

# CONSIDERO SOLO I CASI PEGGIORI CHE NON HANNO L'INVERSA(Queste righe possono essere opportunamente commentate se si vogliono considerare anche i casi con inverso
