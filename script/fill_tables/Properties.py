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

    data_df = pd.read_excel(file_path, sheet_name='MaterialProperties')

    query = """SELECT ID AS Class_ID, Name AS PropertyClass FROM PropClasses"""
    df_propclasses = pd.read_sql(query, conn)

    conn.close()
    
    if df_propclasses.empty:
        raise sqlite3.IntegrityError('To fill Properties you must first fill PropClasses!')
    else:
         df_insert = data_df.merge(df_propclasses, how='inner', on='PropertyClass')
         df_insert = df_insert.rename(columns={'Property':'Name'})
         df_insert = df_insert[['Name', 'IsKPI', 'Class_ID', 'Doi']]
         df_insert = df_insert.where(pd.notnull(df_insert), None)
         return df_insert
        

