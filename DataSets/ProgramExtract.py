import os
import sys
sys.path.append(os.pardir)
import shutil
from Common import PathManager
from Common import FileManager

''' クローンしたプロジェクトのプログラムファイルを抽出する
抽出後のファイルはフォルダ階層を維持してコピーされる
engine_name: 調査対象のゲームエンジン名
dot_extension: 抽出対象のプログラミング言語の拡張子(.が必要)
'''
def extract(engine_name, dot_extension):
    # データセットのパス
    dataset_path = PathManager.get_path(engine_name, PathManager.DATA_SET_FOLDER_NAME)
    # プログラムファイルの保存先フォルダパス
    program_path = PathManager.get_path(engine_name, PathManager.PROGRAM_FOLDER_NAME)

    # データセットのフォルダを再帰的に探索
    for root, dirs, files in os.walk(dataset_path):
        for file_path in files:
            # プログラムファイルがない場合はスキップ
            if not file_path.endswith(dot_extension):
                continue
            relative_path = PathManager.get_relative_path(root, dataset_path)

            # コピー元
            src_file_path = PathManager.join_path(root, file_path)
            # コピー先
            dst_file_path = PathManager.get_path(engine_name, program_path, relative_path, file_path)

            # フォルダがない場合は作成
            FileManager.create_unique_Folder(dst_file_path)

            # プログラムファイルをコピー
            print(f"Copying {src_file_path} to {dst_file_path}")
            shutil.copy2(src_file_path, dst_file_path)