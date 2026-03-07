import ast
from pathlib import Path
import pathspec


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


if __name__ == "__main__":
    # tree = parse_file("/home/rohan/Desktop/work/tru-backend/apps/t86/utils.py")
    # functions = [
    #     node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
    # ]
    # print(functions)

    for file in traverse_project("/home/rohan/Desktop/work/tru-backend"):
        tree = parse_file(file)
        functions = [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
        ]
        print(file, functions)
