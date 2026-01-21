import sys
import os
import pandas as pd
import igraph as ig
import sqlite3
from create_db import connect_database
from paths import db_file

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

db_path = db_file

def fill(file_path):

    conn, cursor = connect_database(db_path)

    data_df = pd.read_excel(file_path, sheet_name='Calculations')
    data_df = data_df.dropna(subset=['Input'])
    data_df['Input'] = data_df['Input'].str.strip()
    data_df['Output'] = data_df['Output'].str.strip()

    edges = list(zip(data_df['Input'], data_df['Output']))
    vertices = list(set(data_df['Input']).union(set(data_df['Output'])))

    graph = ig.Graph(directed=True)
    graph.add_vertices(vertices)
    graph.add_edges(edges)

    start_nodes = [v['name'] for v in graph.vs if graph.indegree(v.index)==0]
    final_nodes = [v['name'] for v in graph.vs if graph.outdegree(v.index)==0]

    workflow_list = []
    for starting_point in start_nodes:
      for target in final_nodes:
        paths = graph.get_all_simple_paths(starting_point, to=target)
        for p in paths:
            workflow_list.append({
                "Start": starting_point,
                "Output": target,
                "Steps": "->".join(graph.vs[v]["name"] for v in p)
            })

    steps_df = pd.DataFrame(workflow_list)
    data_df = data_df.dropna(subset=['Workflow'])
    workflows_df = data_df.merge(steps_df, how='inner', on='Output')

    for _, row in workflows_df.iterrows():

        workflow_name = row["Workflow"]
        steps = row["Steps"].split("->")
        
        cursor.execute("SELECT ID FROM Workflows WHERE Workflow=?", (workflow_name,))
        name = cursor.fetchone()

        if name is None:
           raise sqlite3.IntegrityError('To fill Nodes, Edges and Workflow_Edges you must first fill Workflows!')
        
        workflow_id = name[0]
        
        for step in steps:
            cursor.execute("INSERT OR IGNORE INTO Nodes (Node) VALUES (?)", (step,))
            conn.commit()

        for i in range(len(steps) - 1):
            cursor.execute("SELECT ID FROM Nodes WHERE Node=?", (steps[i],))
            input_id = cursor.fetchone()[0]
            cursor.execute("SELECT ID FROM Nodes WHERE Node=?", (steps[i+1],))
            output_id = cursor.fetchone()[0]

            cursor.execute("INSERT OR IGNORE INTO Edges (Input_ID, Output_ID) VALUES (?, ?)", (input_id, output_id))

            cursor.execute("SELECT ID FROM Edges WHERE Input_ID=? AND Output_ID=?", (input_id, output_id))
            edge_id = cursor.fetchone()[0]

            cursor.execute("""INSERT INTO Workflow_Edges (Workflow_id, Edge_id, StepNumber) VALUES (?, ?, ?)""", (workflow_id, edge_id, i+1))
            
            conn.commit()

    conn.close()



 


