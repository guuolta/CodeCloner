import os
import sys
sys.path.append(os.pardir)
from Common import PathManager

# GitURLが書かれたテキストファイル
GIT_URL_FILE_NAME = 'datasets.txt'

''' git cloneするフォルダのパスを取得
'''
def get_git_url_path(engine_name):
    return PathManager.get_engine_path(engine_name, GIT_URL_FILE_NAME)

''' リポジトリ名(クローン後のフォルダ名)を取得
'''
def get_repository_name(url):
    return url.split("/")[-1].replace(".git", "")

''' git cloneコマンドを取得
'''
def get_git_clone_command(url, path):
    return ["git", "clone", "--depth", "1", url, path]