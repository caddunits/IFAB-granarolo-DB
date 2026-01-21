import pandas as pd

def fill(file_path):
    data_df = pd.read_excel(file_path, sheet_name='CalculationClasses')
    df_insert = pd.Series(data_df['CalculationClass'].dropna().unique(), name='Class')
    df_insert = df_insert.str.strip()
    return df_insert


