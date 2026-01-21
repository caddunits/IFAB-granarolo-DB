import pandas as pd

def fill(file_path):
    data_df = pd.read_excel(file_path, sheet_name='Software')
    data_df = data_df.dropna(subset=['Software'], how='all').drop_duplicates(subset=['Software'])
    df_insert = data_df.rename(columns={'Software':'Name', 'SoftwareDetails':'Details', 'SoftwareWebsite':'Website', 'SoftwareProvider':'Provider'})
    df_insert = df_insert.where(pd.notnull(df_insert), None)
    return df_insert


