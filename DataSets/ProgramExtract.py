import os
import sys
import shutil
import time

import DataSets.DataSetsData as DataSetsData
import DataSets.RemoveUsing as RemoveUsing

sys.path.append(os.path.abspath('../'))
from Common import PathManager as PathManager
from Common import FileManager as FileManager

def extract(engine_name, extensions):
    ''' クローンしたプロジェクトのプログラムファイルを抽出する
    抽出後のファイルはフォルダ階層を維持してコピーされる

    extensions: 抽出対象のプログラミング言語の拡張子のリスト(.は不要)
    '''

    # データセットのパス
    dataset_path = DataSetsData.get_data_sets_path(engine_name)
    # プログラムファイルの保存先フォルダパス
    program_folder_path = DataSetsData.get_program_folder_path(engine_name)

    # 拡張子のドットを追加
    dot_extensions = DataSetsData.get_dot_extensions(extensions[0])
    print(dot_extensions)

    # プログラムファイルの保存先フォルダを作成
    FileManager.create_unique_folder(program_folder_path)

    # データセットのフォルダを再帰的に探索
    for root, dirs, files in os.walk(dataset_path):
        for file_path in files:
            # プログラムファイルでない場合はスキップ
            if not file_path.endswith(dot_extensions):
                continue

            # フォルダの階層を維持するための相対パス
            relative_path = PathManager.get_relative_path(root, dataset_path)

            # コピー元
            src_file_path = PathManager.join_path(root, file_path)
            # コピー先
            dst_file_path = DataSetsData.get_program_file_path(engine_name, relative_path, file_path)

            # すでにコピー済みの場合はスキップ
            if FileManager.is_exist_path(dst_file_path):
                print(f"{file_path} is already copied")
                continue

            # フォルダがない場合は作成
            FileManager.create_unique_folder(PathManager.get_path(program_folder_path, relative_path))

            # ファイルをコピー
            try:
                shutil.copy(src_file_path, dst_file_path)
            except Exception as e:
                print(f"Error: {e}")

            # usingを削除する
            if file_path.endswith(tuple(DataSetsData.REMOVE_USING_EXTENSIONS)):
                RemoveUsing.remove_using_in_file(dst_file_path)