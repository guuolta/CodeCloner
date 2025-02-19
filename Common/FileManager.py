import os

''' ファイルを読み込む
'''
def read_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        return f.readlines()

""" 指定したフォルダのパスがあるか確認する
"""
def check_folder_Path(folder_path):
    return os.path.exists(folder_path)

""" 指定したフォルダのパスがあるか確認し、なければ作成する
"""
def create_unique_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)

''' 空ファイルを生成
    file_name: 生成するファイルのパス(拡張子を含む)
'''
def create_file(path_name):
    with open(path_name,"w"):pass

''' ファイルパスからファイル名を取得
'''
def get_file_name(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

''' 1階層目のディレクトリかどうかを判定
'''
def is_directory(folder_path, file_name):
    return os.path.isdir(os.path.join(folder_path, file_name))