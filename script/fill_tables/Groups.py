import pandas as pd
import sqlite3

def fill(file_path):

    data_df = pd.read_excel(file_path, sheet_name='ResearchGroups')
    df_insert = data_df.rename(columns={'GroupName':'Name'})
    df_insert = df_insert[['Name', 'Website']].drop_duplicates(subset=['Name'], keep='first')
    df_insert = df_insert.where(pd.notnull(df_insert), None)
    return df_insert

