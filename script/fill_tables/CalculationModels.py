import pandas as pd

def fill(file_path):
    data_df = pd.read_excel(file_path, sheet_name='CalculationModels')
    df_insert = pd.Series(data_df['CalculationModel'].dropna().unique(), name='Model')
    df_insert = df_insert.str.strip()
    return df_insert


