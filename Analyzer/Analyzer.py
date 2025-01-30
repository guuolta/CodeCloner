import os
import re
import sqlite3
from dataclasses import dataclass
import sys
from SourceFileDB import main as SourceFileDB
from CloneSetDB import main as CloneSetDB
import Common

@dataclass
class AnalyzeData:
    fileId: int
    fileName: str
    cloneLines: str
    cloneLineCount: int
    cloneTokenCount: int
    lineCount: int
    cloneRate: float

def main():
    source_path = sys.argv[1]
    Common.update_path(source_path)

    file_name = Common.get_folder_name(Common.output_file_path)
    print(file_name)
    Common.create_folder(file_name)

    source_file_conn = sqlite3.connect(Common.get_db_path(file_name, Common.SOURCE_FILE_DB_NAME))
    clone_set_conn = sqlite3.connect(Common.get_db_path(file_name, Common.CLONE_SET_DB_NAME))
    analyze_conn = sqlite3.connect(Common.get_db_path(file_name, Common.ANALYZE_DB_NAME))
    clone_rate_conn = sqlite3.connect(Common.get_db_path(Common.CLONE_RATE_DB_FOLDER_NAME, Common.CLONE_RATE_DB_NAME))

    SourceFileDB(source_file_conn)
    CloneSetDB(clone_set_conn)

    source_file_cur = source_file_conn.cursor()
    clone_set_cur = clone_set_conn.cursor()

    clone_sets = get_all_clone(clone_set_cur)
    clone_dic = get_cloneDic(clone_sets, source_file_cur)

    create_db(analyze_conn)
    datas = get_analyze_datas(source_file_cur, clone_dic)

    insert_analyze_data(analyze_conn, datas)

    create_rate_db(clone_rate_conn)
    insert_clone_rate_data(file_name, analyze_conn, clone_rate_conn)

def get_all_clone(clone_set_cur):
    clone_set_cur.execute('SELECT * FROM cloneSets')
    clone_sets = clone_set_cur.fetchall()
    return clone_sets

def get_cloneDic(clone_sets, source_file_cur):
    clone_dic = {}

    source_file_cur.execute('SELECT id, lines FROM files')
    all_files = source_file_cur.fetchall()
    print(all_files)

    for row in all_files:
        clone_dic[row[0]] = [False] * row[1]

    for clone_set in clone_sets:
        file_id = clone_set[2]
        start_line = clone_set[3]
        end_line = clone_set[5]

        # ファイルの行数を取得
        if file_id in clone_dic:
            file_length = len(clone_dic[file_id])
            start_line = max(0, start_line)
            end_line = min(file_length, end_line)

            # start_line と end_line がファイルの行数の範囲内であるかを確認
            if start_line < file_length and end_line <= file_length:  # end_lineを含むため <= を使用
                new_range = range(start_line, end_line)  # end_lineを含まないため、end_lineをそのまま使用しない

                for i in new_range:
                    clone_dic[file_id][i] = True
            else:
                print(f"Warning: clone_set with file_id {file_id} has out of range indices (start: {start_line}, end: {end_line}, file_length: {file_length})")
        else:
            print(f"Warning: file_id {file_id} not found in clone_dic")

    return clone_dic

def get_analyze_datas(source_file_cur, dic):
    datas = []
    for key in dic:
        file_id = key

        file_name_row = source_file_cur.execute('SELECT name FROM files WHERE id = ?', (file_id,)).fetchone()
        file_name = file_name_row[0] if file_name_row else 'Unknown'

        clone_lines = []
        for file in range(len(dic[file_id])):
            if dic[file_id][file]:
                clone_lines.append(file)

        clone_line_count = len(clone_lines)

        line_count_row = source_file_cur.execute('SELECT lines FROM files WHERE id = ?', (file_id,)).fetchone()
        line_count = line_count_row[0]
        if line_count == 0:
            line_count = 1

        clone_rate = clone_line_count / line_count

        clone_token_count_row = source_file_cur.execute('SELECT tokens FROM files WHERE id = ?', (file_id,)).fetchone()
        clone_token_count = sum(clone_token_count_row) if clone_token_count_row else 0

        # AnalyzeData オブジェクトをリストに追加
        datas.append(AnalyzeData(file_id, file_name, ', '.join(map(str, sorted(clone_lines))), clone_line_count, clone_token_count, line_count, clone_rate))

    return datas

def create_db(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS analyze_results
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                fileId INTEGER,
                fileName TEXT,
                cloneLines TEXT,
                cloneLineCount INTEGER,
                cloneTokenCount INTEGER,
                lineCount INTEGER,
                cloneRate REAL)''')

def insert_analyze_data(conn, datas):
    cur = conn.cursor()

    for data in datas:
        cur.execute('''INSERT INTO analyze_results
                    (fileId, fileName, cloneLines, cloneLineCount, cloneTokenCount, lineCount, cloneRate)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON Conflict(id) DO UPDATE SET
                    fileId = excluded.fileId,
                    fileName = excluded.fileName,
                    cloneLines = excluded.cloneLines,
                    cloneLineCount = excluded.cloneLineCount,
                    cloneTokenCount = excluded.cloneTokenCount,
                    lineCount = excluded.lineCount,
                    cloneRate = excluded.cloneRate;''',
                    (data.fileId, data.fileName, data.cloneLines, data.cloneLineCount, data.cloneTokenCount, data.lineCount, data.cloneRate))

    conn.commit()

def create_rate_db(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS clone_rate
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                fileName TEXT,
                fileCount INTEGER,
                fileCloneCount INTEGER,
                fileCloneRate REAL,
                lineCount INTEGER,
                lineCloneCount INTEGER,
                lineCloneRate REAL)''')

def insert_clone_rate_data(fileName, analyze_conn, rate_conn):
    analyze_cur = analyze_conn.cursor()
    rate_cur = rate_conn.cursor()

    lineCount = 0
    cloneLineCount = 0
    cloneFileCount = 0

    analyze_cur.execute("SELECT fileName, cloneLineCount, lineCount, cloneRate FROM analyze_results")
    datas = analyze_cur.fetchall()

    for data in datas:
        lineCount += data[2]
        cloneLineCount += data[1]
        if data[3] > 0:
            cloneFileCount += 1

    rate_cur.execute('''INSERT INTO clone_rate
                    (fileName, fileCount, fileCloneCount, fileCloneRate, lineCount, lineCloneCount, lineCloneRate)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON Conflict(id) DO UPDATE SET
                    fileCount = excluded.fileCount,
                    fileCloneCount = excluded.fileCloneCount,
                    fileCloneRate = excluded.fileCloneRate,
                    lineCount = excluded.lineCount,
                    lineCloneCount = excluded.lineCloneCount,
                    lineCloneRate = excluded.lineCloneRate;''',
                    (fileName, len(datas), cloneFileCount, cloneFileCount / (1 if len(datas)==0 else len(datas)), lineCount, cloneLineCount, cloneLineCount / (1 if lineCount == 0 else lineCount)))

    rate_conn.commit()

main()