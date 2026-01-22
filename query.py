import os
import sys
import pandas as pd
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

root= Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root))

from script.create_db import connect_database
from script.paths import db_file

db_path = db_file

def query_db(sql:str):
    conn, _ = connect_database(db_path)
    df=pd.read_sql(sql, conn)
    return df

df_polymers = query_db("SELECT DISTINCT Name FROM Polymers")

df_properties = query_db("SELECT DISTINCT Name FROM Properties")


    
