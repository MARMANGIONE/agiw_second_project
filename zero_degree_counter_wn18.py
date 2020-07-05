import pandas as pd
import dfs_portatile_filtered
import dfs_portatile
import check_reverse_fact
import matplotlib.pyplot as plt
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import WordNetError



# Conta tutti i nodi che hanno come grado zero


df = pd.read_csv('data/WN18/ComplEx/complex_filtered_ranks.csv', sep=';',
                 names=['head', 'relation', 'tail', 'head_rank', 'tail_rank'])
df2 = pd.read_csv('data/WN18RR/ComplEx/complex_filtered_ranks.csv', sep=';',
                  names=['head', 'relation', 'tail', 'head_rank_2', 'tail_rank_2'])
df_train_rr = pd.read_csv('data/WN18RR/train_WN18RR.csv', sep='\t', names=['head', 'relation', 'tail'])
df_train = pd.read_csv('data/WN18/train_WN18.csv', sep='\t', names=['head', 'relation', 'tail'])


def degree(node):
    return df_train[df_train['head'] == node].shape[0] + df_train[df_train['tail'] == node].shape[0]

def degree_rr(node):
    return df_train_rr[df_train_rr['head'] == node].shape[0] + df_train_rr[df_train_rr['tail'] == node].shape[0]

def recover_name_wn18(node):
    try:
        node_name = wn.synset_from_pos_and_offset('n', node)._lemma_names[0]
        return node_name
    except WordNetError as e:
        print(e)
        print(node)
        pass

intersection = pd.merge(df, df2, how='inner', on=['head', 'relation', 'tail'])
# seleziono le righe che hanno head rank o tail rank differenti
different_ranks = intersection[(intersection['head_rank'] != intersection['head_rank_2'])
                               | (intersection['tail_rank'] != intersection['tail_rank_2'])]
column_to_list = different_ranks["head"].tolist()
column_to_list = column_to_list + different_ranks["tail"].tolist()
column_to_set = set(column_to_list)
count = 0
print(len(column_to_set))
for el in column_to_set:
    if degree_rr(el) == 0:
        count = count + 1
print(count)


OU
# 3252
# 209