import os

''' フォルダのパス
'''
# CCFinderSWのパス
CCFINDERSW_PATH = os.path.expanduser("~/Documents/CCFinderSW-1.0")

'''フォルダ名
'''
# データセットフォルダ
DATA_SET_FOLDER_NAME = 'DataSets'

# プログラムのみを抽出したフォルダ
PROGRAM_FOLDER_NAME = 'Programs'

# CCFinderSWの結果を入れるフォルダ
CCFINDERSW_RESULT_FOLDER_NAME = 'Outputs'

# データベース
DATA_BASE_FOLDER_NAME = 'DBs'
# 全クローンのデータベースを入れるフォルダ名
CLONE_RATE_DB_FOLDER_NAME = '0_CloneRate'

# 箱ひげ図フォルダ
BOX_PLOT_FOLDER_NAME = 'BoxPlots'


''' フルパスを取得する
'''
def get_engine_path(engine_name):
    return os.path.join(CCFINDERSW_PATH, engine_name)

def get_path(engine_name, *folder_name):
    return os.path.join(CCFINDERSW_PATH, engine_name, *folder_name)

''' パスを結合する
'''
def join_path(*args):
    return os.path.join(*args)

''' 相対パスを取得する
    full_path: フルパス
    prev_path: 基準パス
'''
def get_relative_path(full_path, prev_path):
    return os.path.relpath(full_path, prev_path)