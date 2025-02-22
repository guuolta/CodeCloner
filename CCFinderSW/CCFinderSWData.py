import sys
import os

sys.path.append(os.path.abspath('../'))
from Common import PathManager as PathManager
from DataSets import DataSetsData as DataSetsData

''' CCFinderの解析結果のヘッダー
'''
# ソースファイル一覧のヘッダー
SOURCE_FILES_HEADER = "#source_files"
# クローンセット一覧のヘッダー
CLONE_SETS_HEADER = "#clone_sets"

# クローンセットのヘッダー
CLONE_SET_HEADER = "cloneID:"

''' パス
'''
# CCFinderSWの解析結果フォルダ名
CCFINDERSW_RESULT_FOLDER_NAME = "Outputs"

# CCFinderSWの実行先パス
CCFINDERSW_JAVA_PATH = os.path.expanduser("~/Documents/CCFinderSW-1.0/lib/CCFinderSW-1.0.jar")

# CCFinderSWの解析結果の拡張子
OUTPUT_EXTENSION = ".txt"

def get_program_folder_path(engine_name):
    ''' ソースファイルを保管するフォルダパス取得 '''

    return DataSetsData.get_program_folder_path(engine_name)

def get_output_folder_path(engine_name):
    ''' 解析結果を補完するフォルダパス取得 '''

    return PathManager.get_path(engine_name, CCFINDERSW_RESULT_FOLDER_NAME)

def get_result_file_name(repository_name):
    ''' CCfinderSWの解析結果ファイル名を取得する'''
    
    return f"{repository_name}_output"

def get_result_file_name_with_extension(repository_name):
    ''' CCfinderSWの解析結果ファイル名を拡張子付きで取得する '''

    return f"{repository_name}_output_ccfsw{OUTPUT_EXTENSION}"

def get_repository_name(result_file_name):
    ''' リポジトリ名を取得する 

    result_file_name: 解析結果ファイル名(拡張子付き)
    '''

    return result_file_name.replace(f"_output_ccfsw{OUTPUT_EXTENSION}", "")

def get_execute_command(dataset_folder_path, extensions, language, output_file_name):
    ''' CCFinderSWのコマンド取得
    
    dataset_folder_path: データセットのフォルダパス
    
    language: 解析対象の言語
    
    output_file_name: 出力ファイル名
    '''

    return [
        "java", "-jar", CCFINDERSW_JAVA_PATH,
        "D", "-d", dataset_folder_path,
        "-antlr", *extensions,
        "-l", language,
        "-w", "2",
        "-o", output_file_name,
        "-ccfsw", "set"
    ]