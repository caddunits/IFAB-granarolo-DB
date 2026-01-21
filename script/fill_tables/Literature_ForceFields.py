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

    data_df = pd.read_excel(file_path, sheet_name='ForceFields')

    query1 = """SELECT ID AS Literature_ID, PaperDOI AS Doi FROM Literature"""
    df_literature = pd.read_sql(query1, conn)

    query2 = """SELECT ID AS ForceField_ID, Name AS ForceField FROM ForceFields"""
    df_forcefields = pd.read_sql(query2, conn)

    conn.close()

    if df_literature.empty or df_forcefields.empty:
        raise sqlite3.IntegrityError('To fill Literature_ForceFields you must first fill Literature and ForceFields!')
    else:
        df_insert = data_df.merge(df_literature, how='inner', on='Doi')
        df_insert = df_insert.merge(df_forcefields, how='inner', on='ForceField')
        df_insert = df_insert[['Literature_ID', 'ForceField_ID']].dropna().drop_duplicates()
        return df_insert