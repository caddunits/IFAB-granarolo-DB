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

    query1 = """SELECT ID AS Group_ID, Name AS GroupName FROM Groups"""
    df_groups = pd.read_sql(query1, conn)

    query2 = """SELECT ID AS University_ID, Name AS University FROM Universities"""
    df_universities = pd.read_sql(query2, conn)

    conn.close()

    if df_groups.empty or df_universities.empty:
        raise sqlite3.IntegrityError('To fill University_Group you must first fill Universities and Groups!')
    else:
        df_insert = data_df.merge(df_groups, how='inner', on='GroupName')
        df_insert = df_insert.merge(df_universities, how='inner', on='University')
        df_insert = df_insert[['Group_ID', 'University_ID']].drop_duplicates(keep='first')
        return df_insert