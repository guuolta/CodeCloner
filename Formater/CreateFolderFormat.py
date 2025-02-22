import sys
import os

sys.path.append(os.path.abspath('../'))
from Common import PathManager
from Common import FileManager
from Git import GitData

# 解析に必要なフォルダを生成
def create_folder(engineName):
    FileManager.create_unique_folder(PathManager.get_path(engineName))

# 解析に必要なファイルを生成
def create_file(engine_name):
    FileManager.create_file(PathManager.get_path(engine_name, GitData.GIT_URL_FILE_NAME))