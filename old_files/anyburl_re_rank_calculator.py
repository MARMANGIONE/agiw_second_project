import pandas as pd

#DUBBIO: Corretto il modo in cui viene calcolato il totale delle entità??

data_set = ['FB15k', 'FB15k-237', "WN18", "WN18RR"]
for s in data_set:
    df = pd.read_csv('data/' + s + '/AnyBURL-RE/anyburl-re_filtered_ranks.csv', sep=';',
                     names=['head', 'relation', 'tail', 'head_rank', 'tail_rank'])
    # Per ognuno dei 4 dataset mi creo un set in cui inserisco tutte le entità tail ed head. Con il metodo length ottengo il numero complessivo
    entitySet=set()
    for index, row in df.iterrows():
        entitySet.add(row['head'])
        entitySet.add(row['tail'])
    # A questo punto ho trovato il numero di entità totali e procedo con la sostituzione
    ranks= ['head_rank', 'tail_rank']
    for index, row in df.iterrows():
        for r in ranks:
            if 'MISS_' in row[r]:
                n = int(row[r].replace("MISS_", ""))
                score = (n + len(entitySet))/2
                row[r] = score
    df.to_csv('data/' + s + '/AnyBURL-RE/anyburl-re_filtered_ranks.csv', sep=";", index=False)
