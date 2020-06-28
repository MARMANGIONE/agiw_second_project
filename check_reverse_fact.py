
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
