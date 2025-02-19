import os
import sys
sys.path.append(os.pardir)
import subprocess
from Common import PathManager
from Common import PathData
from Common import FileManager
import shutil
import CCFinderSWData

'''
CCFinderSWでデータセットのクローンを解析する
engine_name: エンジンの名前
extention: 解析対象の拡張子(.は不要)
'''
def analyze(engine_name, extension):
    # データセットのフォルダパス
    datasets_folder_path = PathManager.get_engine_path(engine_name, PathData.PROGRAM_FOLDER_NAME)

    # データセットのフォルダを取得
    for dataset in os.listdir(datasets_folder_path):
        print(dataset)

        # CCFinderSWを実行
        output_file_name = PathManager.get_ccfindersw_result_file_name(dataset)
        subprocess.run(CCFinderSWData.get_ccfindersw_command(os.path.join(datasets_folder_path, dataset), extension, output_file_name), check=True)
        
        # 解析結果を保存
        result_folder = PathManager.get_engine_path(engine_name, PathData.CCFINDERSW_RESULT_FOLDER_NAME)
        FileManager.create_unique_Folder(result_folder)
        shutil.move(output_file_name, result_folder)