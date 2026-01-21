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
    data_df = data_df[data_df['UsedBy'].notna()]
    data_df['UsedBy'] = data_df['UsedBy'].str.split(',')
    data_df['UsedBy'] = data_df['UsedBy'].apply(lambda x: [i.strip() for i in x])
    data_df = data_df.explode('UsedBy').reset_index(drop=True)

    query1 = """SELECT ID AS Group_ID, Name AS UsedBy FROM Groups"""
    df_groups = pd.read_sql(query1, conn)

    query2 = """SELECT ID AS ForceField_ID, Name AS ForceField FROM ForceFields"""
    df_ff = pd.read_sql(query2, conn)

    conn.close()

    if df_groups.empty or df_ff.empty:
        raise sqlite3.IntegrityError('To fill Unit_use_FF you must first fill Groups and ForceFields!')
    else:
        df_insert = data_df.merge(df_groups, how='inner', on='UsedBy')
        df_insert = df_insert.merge(df_ff, how='inner', on='ForceField')
        df_insert = df_insert[['Group_ID', 'ForceField_ID']]
        return df_insert
    
    

