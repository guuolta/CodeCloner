import os
import re

DB_FOLDER_PATH = os.path.expanduser("~/Documents/CCFinderSW-1.0/GameMaker/DBs")

ANALYZE_DB_NAME = 'Analyze.db'
SOURCE_FILE_DB_NAME = 'SourceFile.db'
CLONE_SET_DB_NAME = 'CloneSet.db'
CLONE_RATE_DB_NAME = 'CloneRate.db'
CLONE_RATE_DB_FOLDER_NAME = '0_CloneRate'

output_file_path = ''

START_SUORCE_FILES = "#source_files"
START_CLONE_SETS = "#clone_sets"

def update_path(path):
    global output_file_path
    output_file_path = path


def read_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        return f.readlines()

def get_folder_name(file_path):
    contents = read_file(file_path)
    for line in contents:
        match = re.search(r'-d\s+(.+)', line)
        if match:
            path = match.group(1).strip()
            return path.split('/')[-1]

    print("パスが見つかりませんでした。")
    return None

def create_folder(folder_name):
    name = os.path.join(DB_FOLDER_PATH, folder_name)
    if not os.path.exists(name):
        os.makedirs(name)

def get_db_path(folder_name, db_name):
    return os.path.join(DB_FOLDER_PATH, folder_name, db_name)