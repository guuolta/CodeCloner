import os
import re
import sqlite3
from dataclasses import dataclass
import Common.FileManager as FileManager
import Common.FileManager as PathManager

CLONE_ID_HEADER = 'cloneID'

CLONE_SET_DATASET_COUNT = 5
CLONE_SET_FILE_ID_INDEX = 0
CLONE_SET_START_LINE_INDEX = 1
CLONE_SET_START_TOKEN_INDEX = 2
CLONE_SET_END_LINE_INDEX = 3
CLONE_SET_END_TOKEN_INDEX = 4

@dataclass
class CloneSet:
    id: int
    fileID: int
    startLine: int
    startToken: int
    endLine: int
    endToken: int

def main(conn):
    cur = conn.cursor()
    create_db(cur)

    clone_sets = get_clone_sets()

    for clone_set in clone_sets:
        inset_file(cur, clone_set)
    
    conn.commit()

def create_db(cur):
    cur.execute('DROP TABLE IF EXISTS cloneSets')

    cur.execute('''CREATE TABLE IF NOT EXISTS cloneSets
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                cloneID INTEGER UNIQUE,
                fileID INTEGER,
                startLine INTEGER,
                startToken INTEGER,
                endLine INTEGER,
                endToken INTEGER)''')

def inset_file(cur, clone_set):
    cur.execute('''INSERT INTO cloneSets
                (cloneID, fileID, startLine, startToken, endLine, endToken)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(cloneID) DO UPDATE SET
                fileID = excluded.fileID,
                startLine = excluded.startLine,
                startToken = excluded.startToken,
                endLine = excluded.endLine,
                endToken = excluded.endToken;''',
                (clone_set.id, clone_set.fileID, clone_set.startLine, clone_set.startToken, clone_set.endLine, clone_set.endToken))

def get_clone_sets(file_path):
    files = []

    contents = FileManager.read_file(file_path)

    is_clone_sets_started = False

    id = -1
    for line in contents:
        # クローンセットの部分が始まるか確認
        if not is_clone_sets_started or line.startswith(PathManager.START_CLONE_SETS):
            is_clone_sets_started = True
            continue

        # cloneIDが書かれている行ならID設定
        if line.startswith(CLONE_ID_HEADER):
            id = re.findall(r'cloneID:(\d+)', line)[0]
            continue

        # クローンのデータを取得
        numbers = re.findall(r'\d+', line)

        # データが揃っていたらCloneSetに追加
        if len(numbers) == CLONE_SET_DATASET_COUNT:
            files.append
            (
                CloneSet(
                    id,
                    int(numbers[CLONE_SET_FILE_ID_INDEX]),
                    int(numbers[CLONE_SET_START_LINE_INDEX]),
                    int(numbers[CLONE_SET_START_TOKEN_INDEX]),
                    int(numbers[CLONE_SET_END_LINE_INDEX]),
                    int(numbers[CLONE_SET_END_TOKEN_INDEX])
                )
            )

    return files