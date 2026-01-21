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
    data_df['Ruolo'] = data_df['Ruolo'].str.split(';')
    data_df = data_df.explode('Ruolo').reset_index(drop=True)
    data_df['Ruolo'] = data_df['Ruolo'].str.strip()

    query1 = """SELECT ID AS Role_ID, Role AS Ruolo  FROM Roles"""
    df_roles = pd.read_sql(query1, conn)

    query2 = """SELECT ID AS SmallMolecule_ID, IUPACName FROM SmallMolecules"""
    df_smallmols = pd.read_sql(query2, conn)

    conn.close()

    if df_roles.empty or df_smallmols.empty:
        raise sqlite3.IntegrityError('To fill Mol_Role you must first fill Roles and SmallMolecules!')
    else:
        df_insert = data_df.merge(df_roles, how='inner', on='Ruolo')
        df_insert = df_insert.merge(df_smallmols, how='inner', on='IUPACName')
        df_insert = df_insert[['Role_ID', 'SmallMolecule_ID']]
        return df_insert
    