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
    data_df['Polymer_ref'] = data_df['Polymer_ref'].str.split(',')
    data_df = data_df.explode('Polymer_ref').reset_index(drop=True)
    data_df['Polymer_ref'] = data_df['Polymer_ref'].str.strip()

    query1 = """SELECT ID AS SmallMolecule_ID, IUPACName FROM SmallMolecules"""
    df_smallmols = pd.read_sql(query1, conn)

    query2 = """SELECT ID AS Polymer_ID, Name AS Polymer_ref FROM Polymers"""
    df_polymers = pd.read_sql(query2, conn)

    conn.close()

    if df_smallmols.empty or df_polymers.empty:
        raise sqlite3.IntegrityError('To fill Mol_to_Polymer you must first fill SmallMolecules and Polymers!')
    else:
        df_insert = data_df.merge(df_smallmols, how='inner', on='IUPACName')
        df_insert = df_insert.merge(df_polymers, how='inner', on='Polymer_ref')
        df_insert = df_insert[['SmallMolecule_ID', 'Polymer_ID']]
        return df_insert

