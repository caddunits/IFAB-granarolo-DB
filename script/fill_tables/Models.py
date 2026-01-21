import pandas as pd

def fill(file_path):
    data_df = pd.read_excel(file_path, sheet_name='Toxicity')
    models = data_df.columns.tolist()[6:]
    df_insert = pd.Series(models, name='Model')
    return df_insert



