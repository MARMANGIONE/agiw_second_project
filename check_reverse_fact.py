import pandas as pd

def count_reverse_fact(df, df_train):
    count = 0
    for i, row in df.iterrows():
        if df_train[(df_train['tail'] == row['head'] ) &
                        (df_train['head'] == row['tail']) ].shape[0] == 1:
            print(df_train[(df_train['tail'] == row['head'] ) &
                        (df_train['head'] == row['tail']) ])
            print(row)
            count = count + 1
    return count

def df_without_reverse(df, df_train):
    df_new = df.copy()
    for index, row in df_new.iterrows():
        if df_train[(df_train['tail'] == row['head'] ) &
                        (df_train['head'] == row['tail']) ].shape[0] == 1:
            df_new.drop(index, inplace=True)
    return df_new