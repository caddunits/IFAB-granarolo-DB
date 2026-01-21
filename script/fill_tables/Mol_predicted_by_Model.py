import sys
import os
import pandas as pd
import sqlite3
from create_db import connect_database
from paths import db_file 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

db_path = db_file

def fill(file_path):
    conn, cursor = connect_database(db_path)

    data_df = pd.read_excel(file_path, sheet_name='Toxicity')
    data_df = data_df.melt(id_vars=['ID', 'SMILES', 'IUPACName', 'Ruolo', 'Annex I EU 10-2011'], value_vars=data_df.columns.tolist()[5:], value_name='Value')
    data_df['Value'] = data_df['Value'].str.split('(')
    data_df['Value'] = data_df['Value'].apply(lambda x: [i.strip(' )') for i in x] if isinstance(x, list) else x)
    data_df['Classification'] = data_df['Value'].apply(lambda x: x[0] if isinstance(x, list) and x and x[0] in ['Yes', 'No'] else None)
    data_df['Value'] = data_df['Value'].apply(lambda x: x[1] if isinstance(x, list) and x and len(x)==2 else None)
    data_df = data_df.rename(columns={'variable':'Model'})
    data_df['Value'] = pd.to_numeric(data_df['Value'], errors='coerce').astype('Int64')
    data_df = data_df.where(pd.notnull(data_df), None)

    query1 = """SELECT ID AS Model_ID, Model  FROM Models"""
    df_models = pd.read_sql(query1, conn)

    query2 = """SELECT ID AS SmallMolecule_ID, IUPACName FROM SmallMolecules"""
    df_smallmols = pd.read_sql(query2, conn)

    conn.close()

    if df_models.empty or df_smallmols.empty:
        raise sqlite3.IntegrityError('To fill Mol_predicted_by_Model you must first fill Models and SmallMolecules!')
    else:
        df_insert = data_df.merge(df_models, how='inner', on='Model')
        df_insert = df_insert.merge(df_smallmols, how='inner', on='IUPACName')
        df_insert = df_insert.where(pd.notnull(df_insert), None)
        df_insert = df_insert[['Value', 'Classification', 'Model_ID', 'SmallMolecule_ID']].drop_duplicates(subset=['Value', 'Classification', 'Model_ID', 'SmallMolecule_ID'], keep='first')
        return df_insert
    
