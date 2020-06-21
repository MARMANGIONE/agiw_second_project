import pandas as pd

def totalEntity_calculator():
    set = ['FB15k', 'FB15k-237', "WN18", "WN18RR"]
    for s in set:
        df = pd.read_csv('data/' + s + '/AnyBURL-RE/anyburl-re_filtered_ranks.csv', sep=';',
                         names=['head', 'relation', 'tail', 'head_rank', 'tail_rank'])