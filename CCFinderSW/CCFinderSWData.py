import os

''' CCFinderの解析結果のヘッダー
'''
# ソースファイル一覧のヘッダー
SOURCE_FILES_HEADER = "#source_files"
# クローンセット一覧のヘッダー
CLONE_SETS_HEADER = "#clone_sets"

# CCFinderSWの実行先パス
CCFINDERSW_JAVA_PATH = os.path.expanduser("~/Documents/CCFinderSW-1.0/lib/CCFinderSW-1.0.jar")

''' CCFinderSWのコマンド取得
dataset_folder_path: データセットのフォルダパス
extension: 拡張子(.なし)
output_file_name: 出力ファイル名
'''
def get_ccfindersw_command(dataset_folder_path, extension, output_file_name):
    return [
        "java", "-jar", CCFINDERSW_JAVA_PATH,
        "D", "-d", dataset_folder_path,
        "-antlr", extension,
        "-w", "2",
        "-o", output_file_name,
        "-ccfsw", "set"
    ]