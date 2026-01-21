import pandas as pd

def fill(file_path):
    data_df = pd.read_excel(file_path, sheet_name='Expertises')
    df_insert = pd.Series(data_df['Name'].dropna().unique(), name='Description')
    return df_insert




