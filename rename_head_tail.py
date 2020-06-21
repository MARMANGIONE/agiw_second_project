from bs4 import BeautifulSoup
import requests
import pandas as pd

df=pd.read_csv('data/FB15k/ComplEx/complex_filtered_ranks.csv',sep=';',names=['head','relation','tail','head_rank','tail_rank'])
tail_list = df['tail'].tolist()
head_list = df['head'].tolist()
html_doc = requests.get('https://cofactor.io/'+ tail_list[14]).text
soup = BeautifulSoup(html_doc, 'html.parser')
h1 = soup.find_all('h1')
print(h1[0].text)

#for el in tail_list:
   # html_doc = requests.get('https://cofactor.io/'+ el).text
   # soup = BeautifulSoup(html_doc, 'html.parser')
   # h1 = soup.find_all('h1')
   # print(h1[0].text)
