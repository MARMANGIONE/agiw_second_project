import pandas as pd

df=pd.read_csv('data/FB15k/ComplEx/complex_filtered_ranks.csv',sep=';',names=['head','relation','tail','head_rank','tail_rank'])
df2=pd.read_csv('data/FB15k-237/ComplEx/complex_filtered_ranks.csv',sep=';',names=['head','relation','tail','head_rank_2','tail_rank_2'])

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