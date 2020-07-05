import pandas as pd

# OBIETTIVI DI QUESTO FILE:
# 1) Individuare, per ogni fatto di test nei 4 dataset, la differenza di head rank e tail rank  sulla versione "filtrata"
# rispetto alla versione "originale" nei 4 modelli
# 2) Estrarre una selezione di fatti di test su cui head rank e tail rank sono peggiorati maggiormente


def find_worst(set, data):
    df = pd.read_csv('data/' + set[0] + '/'+ data + '/' + data.lower() + '_filtered_ranks.csv', sep=';',
                     names=['head', 'relation', 'tail', 'head_rank', 'tail_rank'])
    df2 = pd.read_csv('data/' + set[1] + '/' + data + '/' + data.lower() + '_filtered_ranks.csv', sep=';',
                      names=['head', 'relation', 'tail', 'head_rank_2', 'tail_rank_2'])
    # prendo solo l'intersezione dei due dataframe, in modo che ho solo i fatti presenti nel KG filtrato
    intersection = pd.merge(df, df2, how='inner', on=['head', 'relation', 'tail'])
    # seleziono le righe che hanno head rank o tail rank differenti
    different_ranks = intersection[(intersection['head_rank'] != intersection['head_rank_2']) | (
                intersection['tail_rank'] != intersection['tail_rank_2'])]
    # si crea una colonna con la differenza e si ordina in base a quella
    different_ranks['score_diff_head'] = different_ranks['head_rank_2'] - different_ranks['head_rank']
    different_ranks['score_diff_tail'] = different_ranks['tail_rank_2'] - different_ranks['tail_rank']

    # Il nuovo dataframe avrà le prime 20 righe con la differenza maggiore nei rank di head e tail
    different_ranks.sort_values(['score_diff_head','score_diff_tail'] , ascending=[False, False])
    worst_ranks_df = df.head(20)
    worst_ranks_df.to_csv("output/" + set[1] + "/" + data + '/worst_ranks.csv', sep=";", index=False)
    # serieDifferenze_tail = different_ranks['tail_rank_2'] - different_ranks['tail_rank']  # faccio la differenza tra il tail rank del KG filtrato meno il tail rank del KG non filtrato
    # stdTail = pd.DataFrame.std(different_ranks['tail_rank_2'] - different_ranks['tail_rank'])  # calcolo la deviazione standard
    # worst_result_tail = serieDifferenze_tail[
    #    serieDifferenze_tail > stdTail]  # prendo solo i punteggi che sono peggiorati maggiormente
    # faccio lo stesso per le head
    #serieDifferenze_head = different_ranks['head_rank_2'] - different_ranks['head_rank']
    #std_head = pd.DataFrame.std(different_ranks['head_rank_2'] - different_ranks['head_rank'])
    #worst_result_head = serieDifferenze_head[serieDifferenze_head > std_head]


#Qui sarebbe da fare un ciclo for che vede nella cartella "data" per ogni dataset: ComplEx, AnyBURL-RE,HAKE,InteractE il peggiore.
data=["ComplEx", "AnyBURL-RE", "Hake", "InteractE"]
fb_set = ['FB15k', 'FB15k-237']
wn_set = ["WN18", "WN18RR"]

for d in data:
    find_worst(fb_set,d)
    find_worst(wn_set,d)




