import chardet
import os

def read_file(file):
    ''' ファイルを読み込む'''

    try:
        # ファイルのエンコーディングを判別
        with open(file, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']

        # UTF-8をデフォルトにする
        if encoding is None:
            encoding = 'utf-8'

        # 判別したエンコーディングでファイルを読み込む
        with open(file, 'r', encoding=encoding) as f:
            return f.readlines()  # 行をリストとして返す
    except Exception as e:
        print(f"Error reading file {file}: {e}")
        return []

def write_file(file, contents):
    ''' ファイルに書き込む'''

    try:
        with open(file, 'w', encoding='utf-8') as f:
            f.writelines(line for line in contents)
    except Exception as e:
        print(f"Error writing file {file}: {e}")

def is_exist_path(path):
    """ 指定したパスがあるか確認する"""

    return os.path.exists(path)

def is_directory(folder_path, file_name):
    ''' 1階層目のディレクトリかどうかを判定'''

    return os.path.isdir(os.path.join(folder_path, file_name))

def create_unique_folder(folder_path):
    """ 指定したフォルダのパスがあるか確認し、なければ作成する"""

    os.makedirs(folder_path, exist_ok=True)

def create_file(path_name):
    ''' 空ファイルを生成

    file_name: 生成するファイルのパス(拡張子を含む)'''

    with open(path_name,"w"):pass

def get_file_name(file_path):
    ''' ファイルパスからファイル名を取得'''

    return os.path.splitext(os.path.basename(file_path))[0]