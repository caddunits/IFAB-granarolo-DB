import pandas as pd

def fill(file_path):
    data_df = pd.read_excel(file_path, sheet_name='ResearchGroups')
    df_insert = pd.Series(data_df['UnitName'].dropna().unique(), name='Name')
    return df_insert