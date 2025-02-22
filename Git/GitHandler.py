''' Gitの操作を行うモジュール'''

import os
import sys
import subprocess

import Git.GitData as GitData

sys.path.append(os.path.abspath('../'))
from Common import PathManager as PathManager
from Common import FileManager as FileManager

def clone(engine_name):
    ''' git cloneする'''

    # URLリストのファイルパスを取得
    git_url_path = GitData.get_git_url_path(engine_name)

    # フォルダが存在しない場合は終了
    if(not FileManager.is_exist_path(git_url_path)):
        print("DataSets File not Found")
        return

    # URLリストのファイルを読み込む
    git_url_text_file = FileManager.read_file(git_url_path)
    # git cloneした結果を保存するフォルダパス
    git_clone_directory_path = GitData.get_output_folder_path(engine_name)

    # テキストファイルから1行ずつURLを読み込む
    for line in git_url_text_file:
        # 改行や空白を削除
        url = line.strip()

        # 空行をスキップ
        if not url:
            continue

        # リポジトリ名を取得
        repo_name = GitData.get_repository_name(url)
        # git clone結果を保存するフォルダパス
        clone_path = PathManager.join_path(git_clone_directory_path, repo_name)

        # リポジトリがすでに存在している場合はスキップ
        if os.path.exists(clone_path):
            print(f"Repository already exists: {url}")
            continue

        # git cloneを実行
        try:
            print(f"Cloning repository: {url} into {clone_path}")
            subprocess.run(GitData.get_git_clone_command(url, clone_path), check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone {url}: {e}")