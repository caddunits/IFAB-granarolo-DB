import pandas as pd

def fill(file_path):
    data_df = pd.read_excel(file_path, sheet_name='ForceFields')
    data_df = data_df.dropna(subset=['ForceField'], how='all')
    df_insert = data_df.rename(columns={'ForceField':'Name'})
    df_insert = df_insert[['Name', 'Details', 'Doi']]
    df_insert = df_insert.where(pd.notnull(df_insert), None)
    return df_insert


