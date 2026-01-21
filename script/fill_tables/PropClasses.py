import pandas as pd

def fill(file_path):
    data_df = pd.read_excel(file_path, sheet_name='PropertyClasses')
    df_insert = pd.Series(data_df['PropertyClass'].dropna().unique(), name='Name')
    return df_insert
