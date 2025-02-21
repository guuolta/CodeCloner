import sys
import os
sys.path.append(os.path.abspath('../'))

from Common import PathManager
from Common import FileManager
from Git import GitData

# 解析に必要なフォルダを生成
def create_folder(engineName):
    FileManager.create_unique_folder(PathManager.get_path(engineName))

    # データセット保管用
    FileManager.create_unique_folder(PathManager.get_path(engineName, PathManager.DATA_SET_FOLDER_NAME))
    # プログラムファイル保管用
    FileManager.create_unique_folder(PathManager.get_path(engineName, PathManager.PROGRAM_FOLDER_NAME))
    # CCFinderSW解析結果保管用
    FileManager.create_unique_folder(PathManager.get_path(engineName, PathManager.CCFINDERSW_RESULT_FOLDER_NAME))
    # データベース保管用
    FileManager.create_unique_folder(PathManager.get_path(engineName, PathManager.DATA_BASE_FOLDER_NAME))
    # 箱ひげ図保管用
    FileManager.create_unique_folder(PathManager.get_path(engineName, PathManager.BOX_PLOT_FOLDER_NAME))

# 解析に必要なファイルを生成
def create_file(engine_name):
    FileManager.create_file(PathManager.get_path(engine_name, PathManager.DATA_SET_FOLDER_NAME, GitData.GIT_URL_FILE_NAME))

create_folder(sys.argv[1])
create_file(sys.argv[1])
print("Created " + sys.argv[1] + " folder")