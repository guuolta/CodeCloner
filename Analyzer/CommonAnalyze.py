import os
import sys

sys.path.append(os.path.abspath('../'))
from Common import PathManager as PathManager
from Common import FileManager as FileManager

ANALYZE_DB_NAME = 'Analyze.db'
CLONE_SET_DB_NAME = 'CloneSet.db'
CLONE_RATE_DB_NAME = 'CloneRate.db'
CLONE_RATE_DB_FOLDER_NAME = '0_CloneRate'

# データベースのフォルダを作成
def create_db_folder(engine_name, folder_name):
    FileManager.create_unique_folder(PathManager.get_path(engine_name, PathManager.DATA_BASE_FOLDER_NAME, folder_name))

# CCfinderSWの解析結果ファイルを保管するフォルダのパスを取得
def get_output_folder_path(engine_name):
    return PathManager.get_path(engine_name, PathManager.CCFINDERSW_RESULT_FOLDER_NAME)

# データベースファイルのパスを取得
def get_db_path(engine_name, folder_name, db_name):
    return PathManager.get_path(engine_name, PathManager.DATA_BASE_FOLDER_NAME, folder_name, db_name)