import sys
import os
sys.path.append(os.path.abspath('../'))

from Common import PathManager as PathManager
from Common import FileManager as FileManager

# 解析に必要なフォルダを生成
def create_folder(engineName):
    FileManager.create_unique_Folder(PathManager.get_engine_path(engineName))

    # データセット保管用
    FileManager.create_unique_Folder(PathManager.get_path(engineName, PathManager.DATA_SET_FOLDER_NAME))
    # プログラムファイル保管用
    FileManager.create_unique_Folder(PathManager.get_path(engineName, PathManager.PROGRAM_FOLDER_NAME))
    # CCFinderSW解析結果保管用
    FileManager.create_unique_Folder(PathManager.get_path(engineName, PathManager.CCFINDERSW_RESULT_FOLDER_NAME))
    # データベース保管用
    FileManager.create_unique_Folder(PathManager.get_path(engineName, PathManager.DATA_BASE_FOLDER_NAME))
    # 箱ひげ図保管用
    FileManager.create_unique_Folder(PathManager.get_path(engineName, PathManager.BOX_PLOT_FOLDER_NAME))

create_folder(sys.argv[1])
print("Created " + sys.argv[1] + " folder")