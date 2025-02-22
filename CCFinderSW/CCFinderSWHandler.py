import os
import sys
sys.path.append(os.path.abspath('../'))

import subprocess
from Common import PathManager
from Common import FileManager
import shutil
import CCFinderSW.CCFinderSWData as CCFinderSWData

def analyze(engine_name, extensions, language, executer_path):
    '''
    CCFinderSWでデータセットを解析する
    解析結果は、データセットフォルダ内に保存される

    engine_name: エンジンの名前

    extensions: 解析対象のプログラムファイルの拡張子のリスト(.は不要)

    language: 解析するプログラミング言語(grammarsv4内のプログラミング言語のフォルダ名)
        例：C++: cpp, C#: csharp
    '''

    # データセットのフォルダパス
    datasets_folder_path = CCFinderSWData.get_program_folder_path(engine_name)
    # 解析結果のフォルダパス
    output_folder_path = CCFinderSWData.get_output_folder_path(engine_name)

    # 解析結果のフォルダ作成
    FileManager.create_unique_folder(output_folder_path)

    # データセットのフォルダを取得
    for dataset in os.listdir(datasets_folder_path):
        # 2階層目以降のフォルダを対象外とする
        if not FileManager.is_directory(datasets_folder_path, dataset):
            continue

        # ソースファイルのパス
        program_file_path = PathManager.join_path(datasets_folder_path, dataset)
        # 出力ファイル名
        output_file_name = CCFinderSWData.get_result_file_name(dataset)
        # 出力ファイル名(拡張子付き)
        full_output_file_name = CCFinderSWData.get_result_file_name_with_extension(dataset)

        if FileManager.is_exist_path(PathManager.join_path(output_folder_path, full_output_file_name)):
            print(f"Already analyzed: {dataset}")
            continue

        # CCFinderSWを実行
        try:
            print(f"Analyzing: {CCFinderSWData.get_execute_command(program_file_path, extensions, language, output_file_name)}")
            subprocess.run(CCFinderSWData.get_execute_command(program_file_path, extensions, language, output_file_name))
        except Exception as e:
            print(f"{dataset} Error: {e}")
            continue

        # 移動元(このPythonファイルと同じフォルダ内)
        source_file_path = PathManager.join_path(executer_path, full_output_file_name)
        # 移動先(データセットフォルダ内)
        destination_file_path = PathManager.join_path(output_folder_path, full_output_file_name)

        # ファイルを移動
        try:
            shutil.move(source_file_path, destination_file_path)
        except Exception as e:
            print(f"Error: {e}")
            continue