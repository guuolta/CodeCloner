import os

# 一連のツールの操作結果を保存するフォルダ
CCFINDERSW_PATH = os.path.expanduser("~/Documents/CCFinderSW-1.0")

def get_path(engine_name, *folder_name):
    ''' フルパスを取得する'''

    return os.path.join(CCFINDERSW_PATH, engine_name, *folder_name)

def join_path(*args):
    ''' パスを結合する'''

    return os.path.join(*args)

def get_relative_path(full_path, prev_path):
    ''' 相対パスを取得する

    full_path: フルパス

    prev_path: 基準パス
    '''

    return os.path.relpath(full_path, prev_path)