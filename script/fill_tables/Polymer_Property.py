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

    data_df = pd.read_excel(file_path, sheet_name='Calculations')
    data_df['StudiedSystem'] = data_df['StudiedSystem'].str.split(';', n=1)
    data_df[['Polymer', 'SystemDetails']] = data_df['StudiedSystem'].apply(pd.Series)
    data_df['Polymer'] = data_df['Polymer'].str.strip()

    query1 = """SELECT ID AS Property_ID, Name AS PropertyName FROM Properties"""
    df_properties = pd.read_sql(query1, conn)

    query2 = """SELECT ID AS Polymer_ID, Name AS Polymer FROM Polymers"""
    df_polymers = pd.read_sql(query2, conn)

    conn.close()

    if df_properties.empty or df_polymers.empty:
        raise sqlite3.IntegrityError('To fill Polymer_Property you must first fill Properties and Polymers!')
    else:
        df_insert = data_df.merge(df_properties, how='inner', on='PropertyName')
        df_insert = df_insert.merge(df_polymers, how='inner', on='Polymer')
        df_insert = df_insert[['Polymer_ID', 'Property_ID']].drop_duplicates(subset=['Polymer_ID', 'Property_ID'], keep='first')
        return df_insert