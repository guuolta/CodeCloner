import os
import sys
sys.path.append(os.pardir)

import re
import sqlite3

from Common import FileManager
from Common import PathData
from Common import PathManager
from CCFinderSW import CCFinderSWData
from DataBase import DAO
import SourceFileData

''' データベースにファイル情報を保存
conn: データベースのコネクション
engine_name: 解析対象のエンジンの名前
extension: 解析対象の拡張子(.は不要)
'''
def store_database(conn, engine_name, extension):
    # テーブル作成
    cur = conn.cursor()
    DAO.create_table(cur, SourceFileData.TABLE_NAME, SourceFileData.SCHEMA)

    #　データベースにファイル情報を挿入
    files = _get_source_files(PathManager.get_path(engine_name, PathData.CCFINDERSW_RESULT_FOLDER_NAME))
    for file in files:
        _inset_file(cur, file)

    conn.commit()

''' ファイル情報をデータベースに挿入
'''
def _inset_file(cur, file):
    cur.execute('''INSERT INTO files
                (id, name, lines, tokens, path)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                lines = excluded.lines,
                tokens = excluded.tokens,
                path = excluded.path;''',
                (file.id, file.name, file.lines, file.tokens, file.path))

''' ファイル情報を取得
'''
def _get_source_files(file_path, extension):
    files = []
    contents = FileManager.read_file(file_path)
    source_files_started = False

    for line in contents:
        # クローンセットの部分が始まったら終了
        if line.startswith(PathData.START_CLONE_SETS):
            break

        # ソースファイルの部分が始まったらファイル取得開始
        if not source_files_started or line.startswith(CCFinderSWData.SOURCE_FILES_HEADER):
            source_files_started = True
            continue
        
        # ソースファイルのデータセットを取得
        source_file_datas = line.split()
        
        # データセットが足りない場合はスキップ
        if len(source_file_datas) < SourceFileData.SOURCE_FILE_DATASET_COUNT:
            continue

        id = int(source_file_datas[SourceFileData.ID_INDEX])
        lines = int(source_file_datas[SourceFileData.LINE_COUNT_INDEX])
        tokens = int(source_file_datas[SourceFileData.TOKEN_COUNT_INDEX])
        path = source_file_datas[SourceFileData.FILE_PATH_INDEX]
        names = re.findall(r'/([^/]+)\.(extension)$', path)
        
        # ファイル名が取得できなかった場合はスキップ
        if len(names) == 0:
            continue

        name = names[0][0]

        files.append(SourceFileData.SourceFile(id, name, lines, tokens, path))

    return files
