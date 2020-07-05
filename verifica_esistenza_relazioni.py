#metodo per verificare quali relazioni sono state eliminate

import pandas as pd
import requests
from bs4 import BeautifulSoup
from dfs_portatile_filtered import partenza_dfs

def recover_name_fb15k(node):
    html_doc = requests.get('https://cofactor.io/'+ node).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    h1 = soup.find_all('h1')
    return h1[0].text

def test_magic_dfs():
    dict_codici_nomi={}     # per velocizzare il processo e minimizzare le richieste al sito memorizzo le corrispondenze codice - nome
    for path in paths:
        relazioni_eliminate = []
        path_con_nomi=[]
        for step in path:
            if step[0] not in dict_codici_nomi:
                head=recover_name_fb15k(step[0])
                dict_codici_nomi[step[0]]=head
            if step[2] not in dict_codici_nomi:
                tail=recover_name_fb15k(step[2])
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

df = pd.read_csv('data/FB15k-237/train_FB15k-237.csv', sep='\t', names=['head', 'relation', 'tail'])
paths = partenza_dfs('/m/0bxtg','/m/09nqf',df,3,3)
test_magic_dfs()