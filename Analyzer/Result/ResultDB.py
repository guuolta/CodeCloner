import os
import sys
from Result import ResultData as ResultData
from CloneSet import CloneSetData as CloneSetData
from Source import SourceFileData as SourceFileData

sys.path.append(os.path.abspath('../'))
from DataBase import DAO
from Common import FileManager as FileManager

''' クローンとなっているかの2重リストを取得(ファイルID*行数)
'''
def get_clone_line_flags(source_file_cur, clone_sets):
    # クローンとなっているかの2重リストを作成
    clone_flags = create_clone_line_flags(source_file_cur)

    # クローンセットの情報を設定
    for clone_set in clone_sets:
        file_id = clone_set[CloneSetData.FILE_ID_INDEX]
        start_line = clone_set[CloneSetData.START_LINE_INDEX]
        end_line = clone_set[CloneSetData.END_LINE_INDEX]

        # ファイルが存在するかを確認
        if file_id in clone_flags:
            # コードクローンになっている行にフラグを立てる
            for i in range(start_line, end_line):
                clone_flags[file_id][i-1] = True
        else:
            print(f"Warning: file_id {file_id} not found in clone_dic")

    return clone_flags

''' クローンとなっているかの2重リストを作成(ファイルID*行数)
'''
def create_clone_line_flags(source_file_cur):
    clone_flags = {}

    # 全のファイルの行数を取得
    all_files = source_file_cur.execute(f'SELECT id, lines FROM {SourceFileData.TABLE_NAME}').fetchall()

    # 行数分のコードクローンになっているかのフラグを追加
    for row in all_files:
        clone_flags[row[0]] = [False] * row[1]

    return clone_flags

''' データセットを作成
'''
def create_result_data(source_file, clone_flags):
    line_count = source_file[SourceFileData.LINES_INDEX]
    # コードクローンになっている行番号
    clone_lines = []
    clone_line_count = 0

    # フラグガッタている行を探索
    for i in range(len(clone_flags)):
        if clone_flags[i]:
            clone_lines.append(i+1)
            clone_line_count += 1

    return ResultData.ResultData(source_file[SourceFileData.ID_INDEX],
        FileManager.get_file_name(source_file[SourceFileData.NAME_INDEX]),
        ', '.join(map(str, sorted(clone_lines))),
        clone_line_count,
        line_count,
        clone_line_count / (1 if line_count == 0 else line_count))

''' テーブル作成
'''
def create_table(cur):
    DAO.create_table(cur, ResultData.TABLE_NAME, ResultData.TABLE_SCHEMA)

''' ファイル情報をデータベースに挿入
'''
def insert(cur, result_data):
    cur.execute(ResultData.INSERT_SCHEMA,
                    (result_data.file_id, result_data.file_name,
                        result_data.clone_lines, result_data.clone_line_count,
                        result_data.line_count, result_data.clone_rate))