# effettuo 2 dfs, una che parte dal nodo head e un'altra che parte dal nodo tail rispettando comunque il verso delle relazioni

import pandas as pd
from datetime import datetime
import os.path
starttime = datetime.now()


def creaInversi():
    with open("data/WN18/train_WN18.csv") as f:
        lines = f.readlines()
    CSVinv = open("data/WN18/train_WN18-inv.csv", 'w')

    for line in lines:
        CSVinv.write(line)

    lines = [x.strip() for x in lines]

    for line in lines:
        splitline = line.split('\t')
        end = splitline[0] + '\n'
        start = splitline[2] + '\t'
        relation = 'INV::' + splitline[1] + '\t'
        CSVinv.write(start + relation + end)
    f.close()


def partenza_dfs(head,tail,df,DEEPdfs,DEEPreversedfs):
    if(not os.path.isfile("data/WN18/train_WN18-inv.csv")):
        creaInversi()
    df=pd.read_csv('data/WN18/train_WN18-inv.csv', sep='\t', names=['head', 'relation', 'tail'])
    start = ('', '', head)
    stop = ('', '', tail)
    paths = []
    visitati = []
    dfs(df, start, stop,paths,DEEPdfs,visitati)

    start_reverse = (stop[2], stop[0], '')
    stop_reverse = (stop[2], start[0], '')
    dfs_reverse(df, stop_reverse, start_reverse,paths,DEEPreversedfs,visitati)

    return len(paths)

def dfs(df, start, end,paths,DEEPdfs,visitati, path=[], depth=0, visited=[]):
    if start[2] == end[2]:
        paths.append(path + [start])
    if depth < DEEPdfs and start[2] not in visited:
        if not (start[0] == ''):
            path = path + [start]
        if start[2] != end[2]:
            visited.append(start[2])
        for node in childrens(df, start[2]):
            if node not in path:
                if (DEEPdfs == depth + 1):
                    visitati.append((node[2], path + [node]))
                dfs(df, node, end,paths,DEEPdfs,visitati, path, depth + 1, visited)


def childrens(df, start):
    df_start = df[df['head'] == start]
    subset = df_start[['head', 'relation', 'tail']]
    tuples = [tuple(x) for x in df_start.to_numpy()]
    return tuples


def dfs_reverse(df, start, end,paths,DEEPreversedfs,visitati,path=[], depth=0, visited=[]):
    for tupla in visitati:
        if start[0] == tupla[0]:
            wholePath = tupla[1] + [start] + path
            paths.append(wholePath)
    if depth < DEEPreversedfs and start[0] not in visited:
        if not (start[2] == ''):
            path = [start] + path
        if start[0] != end[2]:
            visited.append(start[0])
        for node in childrens_reverse(df, start[0]):
            if node not in path:
                dfs_reverse(df, node, end,paths,DEEPreversedfs,visitati, path, depth + 1, visited)


def childrens_reverse(df, start):
    df_start = df[df['tail'] == start]
    # subset=df_start[['head','relation']]
    tuples = [tuple(x) for x in df_start.to_numpy()]
    return tuples






