import os
import sys
import shutil
import chardet

USING = 'using'
EXTENSION = '.cs'

RESULT_FOLDER_NAME = 'RemoveUsingFiles'

def main(source_path):
    project_name = get_project_name(source_path)
    folder_path = get_result_folder_path(project_name)

    copy_remove_using_files(source_path, folder_path)

def get_project_name(source_path):
    return os.path.basename(os.path.normpath(source_path))

def get_result_folder_path(project_name):
    current_folder = os.path.dirname(os.path.abspath(__file__))
    parent_folder = os.path.dirname(current_folder)

    project_folder = os.path.join(parent_folder, RESULT_FOLDER_NAME, project_name)
    return project_folder

def copy_remove_using_files(path, dest_folder):
    ensure_directory_exists(dest_folder)

    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith(EXTENSION):
                continue

            dest_file = copy_file(root, file, dest_folder)

            contents = read_file(dest_file)

            write_file(dest_file, remove_using(contents))

def ensure_directory_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def copy_file(root, file, dest_folder):
    source_file = os.path.join(root, file)
    dest_file = os.path.join(dest_folder, file)

    shutil.copyfile(source_file, dest_file)

    return dest_file

def read_file(file):
    try:
        # ファイルのエンコーディングを判別
        with open(file, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']

        # 判別したエンコーディングでファイルを読み込む
        with open(file, 'r', encoding=encoding) as f:
            return f.readlines()  # 行をリストとして返す
    except Exception as e:
        print(f"Error reading file {file}: {e}")
        return []

def write_file(file, contents):
    with open(file, 'w', encoding='utf-8') as f:
        f.writelines(line for line in contents)

def print_files(files):
    for file in files:
        print(file)
        print("\n")

def remove_using(lines):
    return [line for line in lines if USING not in line.strip()]