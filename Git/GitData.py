''' Gitに関するデータ'''

import os
import sys

sys.path.append(os.path.abspath('../'))
from Common import PathManager

# クローン結果を保存するフォルダ名
REPOSITORY_FOLDER_NAME = 'Repositories'

# GitURLが書かれたテキストファイル
GIT_URL_FILE_NAME = 'datasets.txt'

def get_git_url_path(engine_name):
    ''' クローンするURLリストのファイルパスを取得 '''

    return PathManager.get_path(engine_name, GIT_URL_FILE_NAME)

def get_output_folder_path(engine_name):
    ''' クローンした結果を保存するフォルダパスを取得'''

    return PathManager.get_path(engine_name, REPOSITORY_FOLDER_NAME)

def get_repository_name(url):
    ''' リポジトリ名(クローン後のフォルダ名)を取得'''

    return url.split("/")[-1].replace(".git", "")

def get_git_clone_command(url, path):
    ''' git cloneコマンドを取得'''

    # `.git` がなければ追加
    if not url.endswith(".git"):
        url += ".git"

    return ["git", "clone", "--depth", "1", url, path]