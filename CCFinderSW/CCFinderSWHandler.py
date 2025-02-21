import os
import sys
sys.path.append(os.path.abspath('../'))

import subprocess
from Common import PathManager
from Common import FileManager
import shutil
import CCFinderSWData

'''
CCFinderSWでデータセットのクローンを解析する
engine_name: エンジンの名前
language: 解析するプログラミング言語(grammarsv4内のプログラミング言語のフォルダ名)
    例：C++: cpp, C#: csharp
'''
def analyze(engine_name, language):
    # データセットのフォルダパス
    datasets_folder_path = CCFinderSWData.get_program_folder_path(engine_name)
    # 解析結果のフォルダパス
    output_folder_path = CCFinderSWData.get_output_folder_path(engine_name)

    # データセットのフォルダを取得
    for dataset in os.listdir(datasets_folder_path):
        # 2階層目以降のフォルダを対象外とする
        if not FileManager.is_directory(datasets_folder_path, dataset):
            continue

        # ソースファイルのパス
        program_file_path = PathManager.join_path(datasets_folder_path, dataset)
        # 出力ファイル名
        output_file_name = CCFinderSWData.get_result_file_name(dataset)

        # CCFinderSWを実行
        subprocess.run(CCFinderSWData.get_execute_command(program_file_path, language, output_file_name))

        # 出力ファイル名(拡張子付き)
        output_file_name_with_extension = CCFinderSWData.get_result_file_name_with_extension(dataset)
        # 移動元(このPythonファイルと同じフォルダ内)
        source_file_path = PathManager.join_path(os.path.dirname(os.path.abspath(__file__)), output_file_name_with_extension)
        # 移動先(データセットフォルダ内)
        destination_file_path = PathManager.join_path(output_folder_path, output_file_name_with_extension)

        # ファイルを移動
        try:
            shutil.move(source_file_path, destination_file_path)
        except Exception as e:
            print(f"Error: {e}")
            continue