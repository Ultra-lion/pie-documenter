import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3

import ast  # noqa: E402
from pathlib import Path  # noqa: E402
import pathspec  # noqa: E402
from graphqlite import Graph  # noqa: E402


def traverse_project(project_path: str):
    project = Path(project_path)
    gitignore_path = project / ".gitignore"

    spec = None
    if gitignore_path.exists():
        with open(gitignore_path, "r") as f:
            spec = pathspec.PathSpec.from_lines("gitwildmatch", f)

    for file in project.rglob("*.py"):
        if spec:
            relative_path = file.relative_to(project)
            if spec.match_file(str(relative_path)):
                continue
        yield file

def parse_file(file_path: str) -> ast.Module:
    with open(file_path, "r") as f:
        return ast.parse(f.read())



def node_ingester(project_dir):
    folder_name = Path(project_dir).name

    db_folder = Path("pie-databases")
    db_folder.mkdir(exist_ok=True)

    graph = Graph(f"{db_folder}/{folder_name}.db")

    for file in traverse_project(project_dir):
        tree = parse_file(file)

        functions = []
        classes = {}

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                methods = [
                    method.name
                    for method in node.body
                    if isinstance(method, ast.FunctionDef)
                ]
                classes[node.name] = methods

        func_batch = []
        for func_name in functions:
            func_batch.append((func_name, {"name": func_name}, "function"))

        if func_batch:
            graph.upsert_nodes_batch(func_batch)
            print(graph.stats())

        class_batch = []
        class_methods_batch = []

        for class_name, methods in classes.items():
            class_batch.append((class_name, {"name": class_name}, "class"))
            for method in methods:
                class_methods_batch.append((method, {"name": method, "class": class_name}, "method"))
        
        if class_batch:
            graph.upsert_nodes_batch(class_batch)
            print(graph.stats())

        if class_methods_batch:
            graph.upsert_nodes_batch(class_methods_batch)
            print(graph.stats())
        
    print(graph.stats())


def get_inner_function_calls(func_node):
    calls = []

    for node in ast.walk(func_node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.append(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                calls.append(node.func.attr)
    return calls



def linker(project_dir):
    folder_name = Path(project_dir).name
    db_folder = Path("pie-databases")
    db_folder.mkdir(exist_ok=True)
    graph = Graph(f"{db_folder}/{folder_name}.db")
    print(graph.stats())
    
    for file in traverse_project(project_dir):
        tree = parse_file(file)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                parent_func_name = node.name
                calls = get_inner_function_calls(node)
                for call in calls:
                    graph.upsert_edge(parent_func_name, call, "", rel_type="CALLS")

            elif isinstance(node, ast.ClassDef):
                class_name = node.name
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_name = item.name
                        
                        graph.upsert_edge(class_name, method_name, "", rel_type="OWNS")

                        calls = get_inner_function_calls(item)

                        for call in calls:
                            graph.upsert_edge(method_name, call, "", rel_type="CALLS")
    
    print(graph.stats())




if __name__ == "__main__":
    # node_ingester("/home/rohan/Desktop/work/tru-backend")
    # node_ingester("/home/rohan/Desktop/work/product-duties-engine")
    linker("/home/rohan/Desktop/work/product-duties-engine")
    
