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

    nodes_num = len(g_query)+1  

    G = nx.Graph()

    G.add_node(func_name)
    for q in g_query:
        G.add_node(q['properties']['name'])
        G.add_edge(func_name, q['properties']['name'])

    # pos = nx.spring_layout(G)
    plt.figure(figsize=(20, 20))
    nx.draw(G, with_labels=True, node_size=200, font_size=10) 
    plt.savefig(f"{pie_graph_folder}/{func_name}_neighbors.png", format="PNG") #



def retrieve_neighbours_of_a_node(project_dir, func_name):
    folder_name = Path(project_dir).name
    db_folder = Path("pie-databases")
    db_folder.mkdir(exist_ok=True)
    pie_graph_folder = Path(f"pie-graphs/{folder_name}")
    pie_graph_folder.mkdir(exist_ok=True)

    graph = Graph(f"{db_folder}/{folder_name}.db")
    print(graph.stats())


    g_query = graph.get_neighbors(func_name)  

    return g_query


def load_graph(project_dir):
    folder_name = Path(project_dir).name
    db_folder = Path("pie-databases")
    db_folder.mkdir(exist_ok=True)
    pie_graph_folder = Path(f"pie-graphs/{folder_name}")
    pie_graph_folder.mkdir(exist_ok=True)

    graph = Graph(f"{db_folder}/{folder_name}.db")
    return graph


def get_all_functions(graph, offset=0, limit=100):
    g_functions = graph.query(f"MATCH (a:function) return a ORDER BY a.id ASC SKIP {offset} LIMIT {limit} ") 
    function_names = [n['a']['properties']['name'] for n in g_functions]
    return function_names

def get_all_classes(graph, offset=0, limit=100):
    g_classes = graph.query(f"MATCH (a:class) return a ORDER BY a.id ASC SKIP {offset} LIMIT {limit} ") 
    classes_names = [n['a']['properties']['name'] for n in g_classes]
    return classes_names

def get_all_class_methods(graph, offset=0, limit=100):
    g_methods = graph.query(f"MATCH (a:class) return a ORDER BY a.id ASC SKIP {offset} LIMIT {limit} ") 
    method_names = [n['a']['properties']['name'] for n in g_methods]
    return method_names


if __name__ == "__main__":
    graph = load_graph("/home/rohan/Desktop/work/proj1")
    sample_funcs = get_all_functions(graph)
    sample_classes = get_all_classes(graph)
    sample_methods = get_all_class_methods(graph)
    print(sample_funcs)