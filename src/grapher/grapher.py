import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3

import ast  # noqa: E402
from pathlib import Path  # noqa: E402
import pathspec  # noqa: E402
from graphqlite import Graph  # noqa: E402

import networkx as nx
import matplotlib.pyplot as plt


project_dir = "/home/rohan/Desktop/work/product-duties-engine"


def draw_graph_for_given_func(project_dir, func_name):
    folder_name = Path(project_dir).name
    db_folder = Path("pie-databases")
    db_folder.mkdir(exist_ok=True)
    pie_graph_folder = Path(f"pie-graphs/{folder_name}")
    pie_graph_folder.mkdir(exist_ok=True)

    graph = Graph(f"{db_folder}/{folder_name}.db")
    print(graph.stats())


    g_query = graph.get_neighbors(func_name)    

    G = nx.Graph()
    G.add_node(func_name)
    for q in g_query:
        G.add_node(q['properties']['name'])
        G.add_edge(func_name, q['properties']['name'])
    
    nx.draw(G, with_labels=True) 
    plt.savefig(f"{pie_graph_folder}/{func_name}_neighbors.png", format="PNG") #


    

if __name__ == "__main__":
    draw_graph_for_given_func(
        "/home/rohan/Desktop/work/product-duties-engine",
        "normalize_hts_code_format"
    )    