import pandas as pd
import numpy
from datetime import datetime

starttime = datetime.now()
df = pd.read_csv('train.csv', sep='\t', names=['head', 'relation', 'tail'])

start = ('', '', '/m/027rn')

stop = ('', '', '/m/06cx9')

start_reverse = (stop[2], stop[0], '')

stop_reverse = (stop[2], start[0], '')
paths = []
visitati = []
DEEPdfs = 3
DEEPreversedfs = 2


def dfs(df, start, end, path=[], depth=0, visited=[]):
    if start[2] == end[2]:
        paths.append(path)
    if depth < DEEPdfs and start[2] not in visited:
        if not (start[0] == ''):
            path = path + [start]
        if start[2] != end[2]:
            visited.append(start[2])
        for node in childrens(df, start[2]):
            if node not in path:
                if (DEEPdfs == depth + 1):
                    visitati.append((node[2], path + [node]))
                dfs(df, node, end, path, depth + 1, visited)


def childrens(df, start):
    df_start = df[df['head'] == start]
    subset = df_start[['head', 'relation', 'tail']]
    tuples = [tuple(x) for x in df_start.to_numpy()]
    return tuples


def dfs_reverse(df, start, end, path=[], depth=0, visited=[]):
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
                dfs_reverse(df, node, end, path, depth + 1, visited)


def childrens_reverse(df, start):
    df_start = df[df['tail'] == start]
    # subset=df_start[['head','relation']]
    tuples = [tuple(x) for x in df_start.to_numpy()]
    return tuples


def test_magic_dfs():
    giusti = 0
    sbagliati = 0
    percorso_sbagliato = []
    for path in paths:
        for step in path:
            tail = df[df['tail'] == step[2]]
            head = tail[tail['head'] == step[0]]
            relation = head[head['relation'] == step[1]]
            if relation.size > 0 or step[1] == '':
                giusti = giusti + 1
            else:
                sbagliati = sbagliati + 1
                percorso_sbagliato = percorso_sbagliato + [path]
                print(percorso_sbagliato)
                print('giusti: ' + str(giusti) + '  |  sbagliati: ' + str(sbagliati))


dfs(df, start, stop)
print(len(paths))
print('ho fatto un pezzo')
dfs_reverse(df, stop_reverse, start_reverse)
print(len(paths))
print('fatto')
test_magic_dfs()

print(datetime.now() - starttime)