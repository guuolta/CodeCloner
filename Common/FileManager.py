import os

''' ファイルを読み込む
'''
def read_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        return f.readlines()

""" 指定したフォルダのパスがあるか確認する
"""
def Check_Folder_Path(folder_path):
    return os.path.exists(folder_path)

""" 指定したフォルダのパスがあるか確認し、なければ作成する
"""
def create_unique_Folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)

''' 空ファイルを生成
    file_name: 生成するファイルのパス(拡張子を含む)
'''
def create_file(path_name):
    with open(path_name,"w"):pass