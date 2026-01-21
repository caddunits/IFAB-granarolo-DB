import pandas as pd

def fill(file_path):
    data_df = pd.read_excel(file_path, sheet_name='Hardware')
    data_df = data_df.dropna(subset=['Hardware'], how='all').drop_duplicates(subset=['Hardware'])
    df_insert = data_df.rename(columns={'Hardware':'Name', 'HardwareDetails':'Details'})
    df_insert = df_insert.where(pd.notnull(df_insert), None)
    return df_insert


