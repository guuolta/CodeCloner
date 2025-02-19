import sys
import os

sys.path.append(os.path.abspath('../'))
from Common import PathManager as PathManager

''' CCFinderの解析結果のヘッダー
'''
# ソースファイル一覧のヘッダー
SOURCE_FILES_HEADER = "#source_files"
# クローンセット一覧のヘッダー
CLONE_SETS_HEADER = "#clone_sets"

# CCFinderSWの実行先パス
CCFINDERSW_JAVA_PATH = os.path.expanduser("~/Documents/CCFinderSW-1.0/lib/CCFinderSW-1.0.jar")

''' ソースファイルを保管するフォルダパス取得
'''
def get_program_folder_path(engine_name):
    return PathManager.get_path(engine_name, PathManager.PROGRAM_FOLDER_NAME)

''' 解析結果を補完するフォルダパス取得
'''
def get_output_folder_path(engine_name):
    return PathManager.get_path(engine_name, PathManager.CCFINDERSW_RESULT_FOLDER_NAME)

''' CCfinderSWの解析結果ファイル名を取得する
'''
def get_result_file_name(repository_name):
    return f"{repository_name}_output"

''' CCfinderSWの解析結果ファイル名を拡張子付きで取得する
'''
def get_result_file_name_with_extension(repository_name):
    return f"{repository_name}_output_ccfsw.txt"


''' CCFinderSWのコマンド取得
dataset_folder_path: データセットのフォルダパス
language: 解析対象の言語
output_file_name: 出力ファイル名
'''
def get_execute_command(dataset_folder_path, language, output_file_name):
    return [
        "java", "-jar", CCFINDERSW_JAVA_PATH,
        "D", "-d", dataset_folder_path,
        "-antlr", "gml", "-l", language,
        "-w", "2",
        "-o", output_file_name,
        "-ccfsw", "set"
    ]