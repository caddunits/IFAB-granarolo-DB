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

    data_df = pd.read_excel(file_path, sheet_name='ResearchGroups')

    query = """SELECT ID, Name AS GroupName FROM Groups"""
    df_groups = pd.read_sql(query, conn)

    conn.close()
    
    if df_groups.empty:
        raise sqlite3.IntegrityError('To fill Researchers you must first fill Groups!')
    else:
        df_insert = data_df.merge(df_groups, how='inner', on='GroupName')
        df_insert = df_insert.rename(columns={'Members':'FullName', 'EmailAddress':'Email', 'ID':'Group_ID'})
        df_insert = df_insert[['FullName', 'Email', 'Group_ID']]
        return df_insert




