import os
import sys
import subprocess

sys.path.append(os.pardir)
from Common import PathManager
from Common import PathData
from Common import FileManager
import GitData

''' git cloneする
engine_name: 調査対象のゲームエンジン名
'''
def clone(engine_name):
    # URLリストのファイルパスを取得
    git_url_path = GitData.get_git_url_path(engine_name)
    
    # フォルダが存在しない場合は終了
    if(not FileManager.Check_Folder_Path(git_url_path)):
        print("Folder not found")
        return

    # URLリストのファイルを読み込む
    git_url_text_file = FileManager.read_file(git_url_path)
    # git cloneした結果を保存するフォルダパス
    git_clone_directory_path = PathManager.get_path(engine_name, PathData.GIT_CLONE_FOLDER_NAME)

    # テキストファイルから1行ずつURLを読み込む
    for line in git_url_text_file:
        # 改行や空白を削除
        url = line.strip()

        # 空行をスキップ
        if not url:
            continue

        # リポジトリ名を取得
        repo_name = GitData.get_repository_name(url)
        # git cloneするパス
        clone_path = os.path.join(git_clone_directory_path, repo_name)

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

