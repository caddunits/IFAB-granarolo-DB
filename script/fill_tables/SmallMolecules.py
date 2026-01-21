import pandas as pd

def fill(file_path):
    data_df = pd.read_excel(file_path, sheet_name='Toxicity')
    df_insert = data_df[['SMILES', 'IUPACName']]
    return df_insert





