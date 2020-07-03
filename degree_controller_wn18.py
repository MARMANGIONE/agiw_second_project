import pandas as pd
import dfs_portatile
import check_reverse_fact
import matplotlib.pyplot as plt
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import WordNetError


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

def bar_chart_different_ranks(serieDifferenze):
    # GRAPH FOR TAIL
    bins = [0, 50, 100, 150, 200, 250, 300, 350, 400, 500, 550, 600, 650, 700, 750]
    out = pd.cut(serieDifferenze, bins=bins, include_lowest=True)
    ax = out.value_counts(sort=False).plot.bar(rot=0, color="b")
    plt.tick_params(labelsize=9)
    group_labels = ['50', '100', '150', '200', '250', '300', '350', '400', '450', '500', '550', '600', '650', '700']
    ax.set_xticklabels(group_labels)
    plt.show()


# prendo solo l'intersezione dei due dataframe, in modo che ho solo i fatti presenti nel KG filtrato

intersection = pd.merge(df, df2, how='inner', on=['head', 'relation', 'tail'])
# seleziono le righe che hanno head rank o tail rank differenti
different_ranks = intersection[(intersection['head_rank'] != intersection['head_rank_2'])
                               | (intersection['tail_rank'] != intersection['tail_rank_2'])]
serieDifferenze_tail = different_ranks['tail_rank_2'] - different_ranks['tail_rank'] # faccio la differenza tra il tail rank del KG filtrato meno il tail rank del KG non filtrato

# GRAPH FOR TAIL
bar_chart_different_ranks(serieDifferenze_tail)

stdTail = pd.DataFrame.std(
    different_ranks['tail_rank_2'] - different_ranks['tail_rank'])  # calcolo la deviazione standard
meanTail = pd.DataFrame.mean(different_ranks['tail_rank_2'] - different_ranks['tail_rank'])
worst_result_tail = serieDifferenze_tail[
    serieDifferenze_tail > stdTail + meanTail]  # prendo solo i punteggi che sono peggiorati maggiormente

# faccio lo stesso per le head
serieDifferenze_head = different_ranks['head_rank_2'] - different_ranks['head_rank']


std_head = pd.DataFrame.std(different_ranks['head_rank_2'] - different_ranks['head_rank'])
mean_head = pd.DataFrame.mean(different_ranks['head_rank_2'] - different_ranks['head_rank'])
worst_result_head = serieDifferenze_head[serieDifferenze_head > std_head + mean_head]
# CONSIDERO SOLO I CASI PEGGIORI CHE NON HANNO L'INVERSA(Queste righe possono essere opportunamente commentate se si vogliono considerare anche i casi con inverso
worst_result_tail = worst_result_tail.sort_values(ascending=False)
worst_result_head = worst_result_head.sort_values(ascending=False)
worst_result_tail = check_reverse_fact.df_without_reverse(intersection.iloc[worst_result_tail.index.tolist(),:],df_train)

worst_result_head = check_reverse_fact.df_without_reverse(intersection.iloc[worst_result_head.index.tolist(),:],df_train)

# print(worst_result_head)
index_list = worst_result_tail.index.values.tolist()
for index in index_list:
    head = intersection.loc[index, :]['head']
    tail = intersection.loc[index, :]['tail']
    relation = intersection.loc[index, :]['relation']
    degreeheadrr = degree_rr(head)
    degreetailrr = degree_rr(tail)
    # and nome_head != '❔' and nome_tail != '❔'
    nome_head = recover_name_wn18(head)
    nome_tail = recover_name_wn18(tail)
    print(index, '---', nome_head, '(', head, ')', 'degree', degreeheadrr, '--->',
          relation, '--->', nome_tail, '(', tail, ')', 'degree', degreetailrr, 'WN18RR', 'paths', dfs_portatile.partenza_dfs(head, tail, df_train_rr, 4, 4))
    print(index, '---', nome_head, '(', head, ')', 'degree', degree(head), '--->',
          relation, '--->', nome_tail, '(', tail, ')', 'degree', degree(tail), 'WN18', 'paths', dfs_portatile.partenza_dfs(head, tail, df_train, 4, 4))
    print('')


