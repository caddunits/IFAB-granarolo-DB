import sys
import os
import importlib
from create_db import connect_database
from tables_list import commands

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def fill_table(path, name, file_path):
    '''Fill tables with data'''
    if name in list(commands.keys()):
        try:
            module = importlib.import_module(f'fill_tables.{name}')
            fill = getattr(module, "fill")
            conn, cursor = connect_database(path=path)
            df_insert = fill(file_path)
            df_insert.to_sql(name, conn, if_exists='append', index=False, method='multi')
            print(f'Table {name} filled!')
        except Exception as e:
            print(f'Error while filling {name}: {e}')
        finally:
            conn.close()
    elif name == 'Graphs':
        try:
            module = importlib.import_module(f'fill_tables.{name}')
            fill = getattr(module, 'fill')
            fill(file_path)
            graphs_list = ['Nodes', 'Edges', 'Workflow_Edges']
            for t in graphs_list:
                print(f'Table {t} filled!')
        except Exception as e:
            print(f'Error while filling Graphs: {e}')
    else:
        print(f'table {name} non available!')
        print('Tables list: ', end='')
        for k in list(commands.keys()):
            print(f"'{k}', ", end='')
        print("Graphs")

