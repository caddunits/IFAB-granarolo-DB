import os
import sqlite3
from script.tables_list import commands

def del_database(path):
    '''Delete a database'''
    if os.path.exists(path):
        os.remove(path)
        

def connect_database(path):
    '''Create a database'''
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    return conn, cursor


def add_tables(path, tables=None):
    '''Add tables to a database'''
    conn, cursor = connect_database(path)
    if tables is None:
          for command in commands.values():
            try:
               cursor.execute(command)
            except Exception as e:
                print(f'Error for {command}: {e}')
    else:
        for name in tables:
            if name in commands.keys():
                cursor.execute(commands[name])
            else:
                print(f'table {name} non existent!' )
    conn.commit()
    conn.close()