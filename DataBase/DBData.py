import os
import sys

sys.path.append(os.path.abspath('../'))
from Common import PathManager
from CCFinderSW import CCFinderSWData as CCFinderSWData


DATA_BASE_FOLDER_NAME = 'DBs'

# 全クローンのデータベースを入れるフォルダ名
CLONE_RATE_DB_FOLDER_NAME = '0_CloneRate'

def get_output_folder_path(engine_name):
    ''' CCfinderSWの解析結果ファイルを保管するフォルダのパスを取得 '''

    return CCFinderSWData.get_output_folder_path(engine_name)

def get_db_folder_path(engine_name):
    ''' データベースフォルダのパスを取得 '''

    return PathManager.get_path(engine_name, DATA_BASE_FOLDER_NAME)

def get_db_path(engine_name, folder_name, db_name):
    ''' データベースファイルのパスを取得 '''

    return PathManager.get_path(engine_name, DATA_BASE_FOLDER_NAME, folder_name, db_name)