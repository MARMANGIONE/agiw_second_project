#metodo per verificare quali relazioni sono state eliminate

import pandas as pd
from dfs_portatile_filtered import partenza_dfs
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import WordNetError

def recover_name_wn18(node):
    try:
        node_name = wn.synset_from_pos_and_offset('n', node)._lemma_names[0]
        return node_name
    except WordNetError as e:
        print(e)
        print(node)
        pass

def test_magic_dfs():
    dict_codici_nomi={}     # per velocizzare il processo e minimizzare le richieste al sito memorizzo le corrispondenze codice - nome
    for path in paths:
        relazioni_eliminate = []
        path_con_nomi=[]
        for step in path:
            if step[0] not in dict_codici_nomi:
                head=recover_name_wn18(step[0])
                dict_codici_nomi[step[0]]=head
            if step[2] not in dict_codici_nomi:
                tail=recover_name_wn18(step[2])
                dict_codici_nomi[step[2]]=tail
            step_con_nomi=(dict_codici_nomi[step[0]],step[1],dict_codici_nomi[step[2]])
            path_con_nomi.append(step_con_nomi)
            relation = df[(df['tail'] == step[2]) & (df['head'] == step[0]) & (df['relation']== step[1])]
            if relation.size > 0:#se la relazione esiste ancora non faccio nulla
                print()
            else:                #la relazione è stata eliminata nel dataset filtrato
                #print(relation)
                relazioni_eliminate = relazioni_eliminate + [step_con_nomi]
        print(path_con_nomi)
        print(relazioni_eliminate)




#with open("output/pathFB15k.txt", "r") as file:
 #   paths = eval(file.readline())

df = pd.read_csv('data/WN18RR/train_WN18RR.csv', sep='\t', names=['head', 'relation', 'tail'])
paths = partenza_dfs('9634494','7846',df,3,3)
test_magic_dfs()