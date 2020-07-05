import pandas as pd


# conta il numero di relazioni inverse che ci sono
def count_reverse_fact(df, df_train):
    count = 0
    for i, row in df.iterrows():
        if df_train[(df_train['tail'] == row['head'] ) &
                        (df_train['head'] == row['tail']) ].shape[0] == 1:
            count = count + 1
    return count

# Restituisce un nuovo dataset in cui sono esclusi tutti i fatti che hanno la relazione inversa
def df_without_reverse(df, df_train):
    df_new = df.copy()
    for index, row in df_new.iterrows():
        if df_train[(df_train['tail'] == row['head'] ) &
                        (df_train['head'] == row['tail']) ].shape[0] == 1:
            df_new.drop(index, inplace=True)
    return df_new


# verifica se è prerente nel dataset di training la relazione inversa
# Se sì restituisce 1 altrimenti 0
def have_reverse(tail, head, df_train):
    count = 0
    if df_train[(df_train['tail'] == head ) &
                    (df_train['head'] == tail )].shape[0] == 1:
                    count = count + 1
    return count