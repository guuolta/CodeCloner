import os
import sys

from . import SourceFileData as SourceFileData

sys.path.append(os.path.abspath('../'))
from Common import FileManager as FileManager
from Common import PathManager as PathManager
from DataBase import DAO as DAO

''' テーブル作成
'''
def create_table(cur):
    DAO.create_table(cur, SourceFileData.TABLE_NAME, SourceFileData.TABLE_SCHEMA)

''' ソースファイルの1行からデータセットを作成
'''
def create_source_file_data(source_file_line):
    # ソースファイルのデータセットを取得
    source_file_datas = source_file_line.split()
    
    # データセットが足りない場合はスキップ
    if len(source_file_datas) < SourceFileData.CCFINDERSW_SOURCE_FILE_DATASET_COUNT:
        return

    # 要素を取得
    id = int(source_file_datas[SourceFileData.CCFINDERSW_ID_INDEX])
    line_count = int(source_file_datas[SourceFileData.CCFINDERSW_LINE_COUNT_INDEX])
    token_count = int(source_file_datas[SourceFileData.CCFINDERSW_TOKEN_COUNT_INDEX])
    path = source_file_datas[SourceFileData.CCFINDERSW_FILE_PATH_INDEX]
    name = FileManager.get_file_name(path)

    return SourceFileData.SourceFile(id, name, line_count, token_count, path)

''' ファイル情報をデータベースに挿入
'''
def inset(cur, file):
    cur.execute(SourceFileData.INSERT_SCHEMA,
                (file.id, file.name, file.lines, file.tokens, file.path))