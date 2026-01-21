import pandas as pd

def fill(file_path):
    data_df = pd.read_excel(file_path, sheet_name='Toxicity')
    laws = data_df.columns.tolist()[5]
    df_insert = pd.Series(laws, name='Law')
    return df_insert



