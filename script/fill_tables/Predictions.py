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
    data_df = data_df[data_df['PropertyName'].notna()]

    query = """SELECT ID AS Property_ID, Name AS PropertyName FROM Properties"""
    df_properties = pd.read_sql(query, conn)

    conn.close()

    if df_properties.empty:
        raise sqlite3.IntegrityError('To fill Predictions you must first fill Properties!')
    else:
        df_insert = data_df.merge(df_properties, how='inner', on='PropertyName')
        df_insert = df_insert.rename(columns={'PropertyValue':'Value', 'PropertyUnit':'Unit', 'ErrorInPrediction':'Error'})
        df_insert = df_insert[['Value', 'Unit', 'Error', 'Property_ID']]
        df_insert = df_insert.astype({'Value': float, 'Error': float})
        df_insert = df_insert.where(pd.notnull(df_insert), None)
        return df_insert



