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

    query1 = """SELECT ID AS Unit_ID, Name AS UnitName FROM Units"""
    df_units = pd.read_sql(query1, conn)

    query2 = """SELECT ID AS Researcher_ID, FullName AS Members FROM Researchers"""
    df_researchers = pd.read_sql(query2, conn)

    conn.close()

    if df_units.empty or df_researchers.empty:
        raise sqlite3.IntegrityError('To fill Unit_Researcher you must first fill Units and Researchers!')
    else:
        df_insert = data_df.merge(df_units, how='inner', on='UnitName')
        df_insert = df_insert.merge(df_researchers, how='inner', on='Members')
        df_insert = df_insert[['Researcher_ID', 'Unit_ID']].drop_duplicates(keep='first')
        return df_insert