import pandas as pd

def fill(file_path):
    data_df = pd.read_excel(file_path, sheet_name='Calculations')
    data_df = data_df.dropna(subset=['StudiedSystem'], how='any')
    data_df['StudiedSystem'] = data_df['StudiedSystem'].str.split(';', n=1)
    data_df[['Polymer', 'SystemDetails']] = data_df['StudiedSystem'].apply(pd.Series)
    data_df['Polymer'] = data_df['Polymer'].str.strip()
    df_insert = pd.Series(data_df['Polymer'].dropna().unique(), name='Name')
    return df_insert