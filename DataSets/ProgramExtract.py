import os
import sys
sys.path.append(os.pardir)
import shutil
from Common import PathManager
from Common import PathData
from Common import FileManager

''' クローンしたプロジェクトのプログラムファイルを抽出する
抽出後のファイルはフォルダ階層を維持してコピーされる
engine_name: 調査対象のゲームエンジン名
dot_extension: 抽出対象のプログラミング言語の拡張子(.が必要)
'''
def extract(engine_name, dot_extension):
    # データセットのパス
    dataset_path = PathManager.get_engine_path(engine_name, PathData.DATASETS_FOLDER_NAME)
    # プログラムファイルの保存先フォルダパス
    program_path = PathManager.get_engine_path(engine_name, PathData.PROGRAM_FOLDER_NAME)

    # データセットのフォルダを再帰的に探索
    for root, dirs, files in os.walk(dataset_path):
        # フォルダ内のファイルを拡張子でフィルタリング
        program_files = [f for f in files if f.endswith(dot_extension)]

        # プログラムファイルがない場合はスキップ
        if not program_files:
            continue

        # 保存先ディレクトリを作成
        FileManager.create_unique_Folder(program_path)

        # プログラムファイルをコピー
        for program_file in program_files:
            src_file_path = PathManager.join_path(dataset_path, program_file)
            dst_file_path = PathManager.join_path(program_path, program_file)
            
            print(f"Copying {src_file_path} to {dst_file_path}")
            shutil.copy2(src_file_path, dst_file_path)