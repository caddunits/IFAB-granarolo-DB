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
    data_df = data_df[data_df['Workflow'].notna()]
    data_df = data_df.astype({'PropertyValue':float})
    
    query = """SELECT pd.ID AS Prediction_ID, pd.Value AS PropertyValue, pd.Unit AS PropertyUnit, pd.Error AS ErrorInPrediction, pr.Name AS PropertyName FROM Predictions pd JOIN Properties pr ON pr.ID=pd.Property_ID"""
    df_predictions = pd.read_sql(query, conn)
    df_predictions = df_predictions.astype({'PropertyValue':float})

    conn.close()
    
    if df_predictions.empty:
        raise sqlite3.IntegrityError('To fill Workflows you must first fill Predictions!')
    else:
        df_insert = data_df.merge(df_predictions, how='inner', on=['PropertyValue', 'PropertyUnit', 'ErrorInPrediction', 'PropertyName'])
        df_insert = df_insert[['Workflow', 'Prediction_ID']]
        return df_insert









