import os
import sys

sys.path.append(os.path.abspath('../'))
from Common import PathManager

# GitURLが書かれたテキストファイル
GIT_URL_FILE_NAME = 'datasets.txt'

''' git cloneするURLリストのファイルパスを取得
'''
def get_git_url_path(engine_name):
    return PathManager.get_path(engine_name, PathManager.DATA_SET_FOLDER_NAME, GIT_URL_FILE_NAME)

''' git cloneした結果を保存するフォルダパスを取得
'''
def get_output_folder_path(engine_name):
    return PathManager.get_path(engine_name, PathManager.DATA_SET_FOLDER_NAME)

''' リポジトリ名(クローン後のフォルダ名)を取得
'''
def get_repository_name(url):
    return url.split("/")[-1].replace(".git", "")

''' git cloneコマンドを取得
'''
def get_git_clone_command(url, path):
    return ["git", "clone", "--depth", "1", url, path]