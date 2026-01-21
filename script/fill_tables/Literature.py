import pandas as pd

def fill(file_path):
    data_df = pd.read_excel(file_path, sheet_name='Literature')
    data_df = data_df.dropna().drop_duplicates()
    df_insert = data_df[['Title', 'PaperDOI']]
    return df_insert



    
    