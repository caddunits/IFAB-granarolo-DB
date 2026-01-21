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
    data_df = data_df.melt(id_vars=['ID', 'SMILES', 'IUPACName', 'Ruolo','Acute Oral Toxicity', 'Androgenicity', 'Carcinogenicity','Estrogenicity', 'Eye Irritation', 'Hepatotoxicity', 'Mutagenicity','Skin Irritation'],value_vars=['Annex I EU 10-2011'], value_name='Present')
    data_df = data_df.rename(columns={'variable':'Law'})

    query1 = """SELECT ID AS Law_ID, Law  FROM Laws"""
    df_laws = pd.read_sql(query1, conn)

    query2 = """SELECT ID AS SmallMolecule_ID, IUPACName FROM SmallMolecules"""
    df_smallmols = pd.read_sql(query2, conn)

    conn.close()

    if df_laws.empty or df_smallmols.empty:
        raise sqlite3.IntegrityError('To fill Mol_present_in_Law you must first fill Laws and SmallMolecules!')
    else:
        df_insert = data_df.merge(df_laws, how='inner', on='Law')
        df_insert = df_insert.merge(df_smallmols, how='inner', on='IUPACName')
        df_insert = df_insert[['Present', 'Law_ID', 'SmallMolecule_ID']]
        return df_insert
    



