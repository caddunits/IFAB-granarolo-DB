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
    data_df = data_df.rename(columns={'CalculationDetails': 'Details'})
    data_df = data_df.dropna(subset=['Input'])
    data_df['Software'] = data_df['Software'].str.split('+')
    data_df['Software'] = data_df['Software'].apply(lambda x: [i.strip() for i in x])
    data_df = data_df.explode('Software').reset_index(drop=True)

    data_df['StudiedSystem'] = data_df['StudiedSystem'].str.split(';', n=1)
    data_df['StudiedSystem'] = data_df['StudiedSystem'].apply(lambda x: [i.strip() for i in x])
    data_df[['Polymer', 'System']] = data_df['StudiedSystem'].apply(pd.Series)

    data_df['CalculationClass'] = data_df['CalculationClass'].str.strip()
    data_df['CalculationModel'] = data_df['CalculationModel'].str.strip()
    data_df['Input'] = data_df['Input'].str.strip()
    data_df['Output'] = data_df['Output'].str.strip()

    query1 = """SELECT ID AS Class_ID, Class AS CalculationClass FROM CalculationClasses"""
    df_calcclasses = pd.read_sql(query1, conn)
    df_calcclasses['CalculationClass'] = df_calcclasses['CalculationClass'].str.strip()

    if df_calcclasses.empty:
        raise sqlite3.IntegrityError('To fill Calculations you must first fill CalculationClasses!')
    else:
        merged_df1 = data_df.merge(df_calcclasses, how='inner', on='CalculationClass')

    query2 = """SELECT ID AS Model_ID, Model AS CalculationModel FROM CalculationModels"""
    df_calcmodels = pd.read_sql(query2, conn)
    df_calcmodels['CalculationModel'] =  df_calcmodels['CalculationModel'].str.strip()


    if df_calcmodels.empty:
        raise sqlite3.IntegrityError('To fill Calculations you must first fill CalculationModels!')
    else:
        merged_df2 = merged_df1.merge(df_calcmodels, how='inner', on='CalculationModel')

    query3 = """SELECT ID AS Group_ID, Name FROM Groups"""
    df_groups = pd.read_sql(query3, conn)
    df_groups = df_groups.rename(columns={'Name':'Group'})

    if df_groups.empty:
        raise sqlite3.IntegrityError('To fill Calculations you must first fill Groups!')
    else:
        merged_df3 = merged_df2.merge(df_groups, how='inner', on='Group')
    
    query4 = """SELECT ID AS ForceField_ID, Name AS ForceField FROM ForceFields"""
    df_forcefield = pd.read_sql(query4, conn)

    if df_forcefield.empty:
        raise sqlite3.IntegrityError('To fill Calculations you must first fill ForceFields!')
    else:
        merged_df4 = merged_df3.merge(df_forcefield, how='left', on='ForceField')

    query5 = """SELECT ID AS Software_ID, Name AS Software FROM Software"""
    df_software = pd.read_sql(query5, conn)

    if df_software.empty:
        raise sqlite3.IntegrityError('To fill Calculations you must first fill Software!')
    else:
        merged_df5 = merged_df4.merge(df_software, how='inner', on='Software')

    query6 = """SELECT ID AS Polymer_ID, Name as Polymer FROM Polymers"""
    df_polymers = pd.read_sql(query6, conn)

    if df_polymers.empty:
        raise sqlite3.IntegrityError('To fill Calculations you must first fill Polymers!')
    else:     
        merged_df6 = merged_df5.merge(df_polymers, how='inner', on='Polymer')

    query7 = """SELECT ID AS Hardware_ID, Name AS Hardware FROM Hardware"""
    df_hardware = pd.read_sql(query7, conn)

    if df_hardware.empty:
        raise sqlite3.IntegrityError('To fill Calculations you must first fill Hardware!')
    else:
        merged_df7 = merged_df6.merge(df_hardware, how='inner', on='Hardware')
    
    query8 = """SELECT e.ID AS Edge_ID, n1.Node AS Input, n2.Node AS Output  FROM Edges e JOIN Nodes n1 ON n1.ID=e.Input_ID JOIN Nodes n2 ON n2.ID=e.Output_ID"""
    df_edges = pd.read_sql(query8, conn)

    conn.close()

    if df_edges.empty:
        raise sqlite3.IntegrityError('To fill Calculations you must first fill Nodes, Edges and Workflow_Edges!')
    else:
        merged_df8 = merged_df7.merge(df_edges, how='left', on=['Input', 'Output'])
        df_insert = merged_df8[['Details', 'System', 'LinkToData', 'Class_ID', 'Model_ID', 'Edge_ID','Group_ID','ForceField_ID','Software_ID', 'Polymer_ID', 'Hardware_ID']]
        df_insert = df_insert.where(pd.notnull(df_insert), None)
        return df_insert
