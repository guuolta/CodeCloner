import os
from graphCreater import main as create_graph

GRAPH_PYTHON_PATH = os.path.expanduser("~/Documents/CCFinderSW-1.0/Python/Analyzer/graphCreater.py")
DB_FOLDER_PATH = os.path.expanduser("~/Documents/CCFinderSW-1.0/DBs")
CLONE_RATE_DB_FOLDER_NAME = '0_CloneRate'
ANALYZE_DB_NAME = 'Analyze.db'

def main():
    for folder in os.listdir(DB_FOLDER_PATH):
        if folder != CLONE_RATE_DB_FOLDER_NAME:
            folder_path = os.path.join(DB_FOLDER_PATH, folder)
            if os.path.isdir(folder_path):
                db_path = os.path.join(folder_path, ANALYZE_DB_NAME)
                create_graph(db_path, folder)

main()