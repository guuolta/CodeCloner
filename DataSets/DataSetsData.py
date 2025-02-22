import os
import sys

sys.path.append(os.path.abspath('../'))
from Common import PathManager as PathManager
from Common import FileManager as FileManager
from Git import GitData as GitData

# プログラムファイルの保存先フォルダ名
PROGRAM_FOLDER_NAME = 'Programs'

# usingを削除するファイルの拡張子(dotを含む)
REMOVE_USING_EXTENSIONS = ['.cs']

def get_data_sets_path(engine_name):
    ''' データセットのフォルダパスを取得 '''

    return GitData.get_output_folder_path(engine_name)

def get_program_folder_path(engine_name):
    ''' プログラムファイルを保管するフォルダパス取得 '''

    return PathManager.get_path(engine_name, PROGRAM_FOLDER_NAME)

def get_program_file_path(engine_name, relative_path, file_path):
    ''' プログラムファイルの保存先パスを取得

    relative_path: フォルダの階層
    file_path: ファイル名(拡張子付き)
    '''

    return PathManager.get_path(engine_name, PROGRAM_FOLDER_NAME, relative_path, file_path)

def get_dot_extensions(*extensions):
    ''' 探索するファイルの拡張子を取得 '''

    return tuple(f".{ext}" for ext in extensions)