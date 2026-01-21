import pandas as pd

def fill(file_path):
    data_df = pd.read_excel(file_path, sheet_name='Toxicity')
    data_df = data_df[data_df['Ruolo'].notna()]
    data_df['Ruolo'] = data_df['Ruolo'].str.split(';')
    data_df['Ruolo'] = data_df['Ruolo'].apply(lambda x: [i.strip() for i in x])
    data_df = data_df.explode('Ruolo').reset_index(drop=True)
    df_insert = pd.Series(data_df['Ruolo'].dropna().unique(), name='Role')
    return df_insert

