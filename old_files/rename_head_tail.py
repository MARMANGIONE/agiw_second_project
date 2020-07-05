from bs4 import BeautifulSoup
import requests
import pandas as pd
from nltk.corpus import wordnet as wn

# OBIETTIVO: Dato un dataframe per FB15k e WN18 recupera i nodi di ogni nodo:

def recover_name_fb15k(df):
    # 'head', 'relation', 'tail', 'head_rank', 'tail_rank'
    # head ha indice 0 e tail ha indice  2
    columns = list(df)
    heads = []
    tails = []
    for i in columns:
        head = df[i][0]
        tail = df[i][2]
        html_doc1 = requests.get('https://cofactor.io/'+ head).text
        html_doc2 = requests.get('https://cofactor.io/' + tail).text
        soup1 = BeautifulSoup(html_doc1, 'html.parser')
        soup2 = BeautifulSoup(html_doc2, 'html.parser')
        h1_1 = soup1.find_all('h1')
        h1_2 = soup2.find_all('h1')
        heads.append(h1_1[0].text)
        tails.append(h1_2[0].text)
    df['head_name'] = heads
    df['tail_name'] = tails

def recover_name_wordnet(df):
    columns = list(df)
    heads = []
    tails = []
    for i in columns:
        head = df[i][0]
        tail = df[i][2]
        # Da un synset è possibile ricavare una lista di lemmi ossia sinonimi per quella parola. Di regola prenderemo sempre il primo
        head = wn.synset_from_pos_and_offset('n', head)._lemma_names[0]
        tail = wn.synset_from_pos_and_offset('n',tail)._lemma_names[0]
        heads.append(head)
        tails.append(tail)
    df['head_name'] = heads
    df['tail_name'] = tails


# IL FILE DI INPUT SARA' QUELLO GENERATO DA estraggo_righe_comuni.py. Finito estraggo_righe_comuni.py va fatta la sostituzione qui
#df=pd.read_csv('data/FB15k/ComplEx/complex_filtered_ranks.csv',sep=';',names=['head','relation','tail','head_rank','tail_rank'])
#recover_name_fb15k(df)

#TEST PER WN18
df=pd.read_csv('data/WN18/ComplEx/complex_filtered_ranks.csv',sep=';',names=['head','relation','tail','head_rank','tail_rank'])
recover_name_wordnet(df)