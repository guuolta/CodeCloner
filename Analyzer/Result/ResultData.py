import os
import sys
from dataclasses import dataclass

sys.path.append(os.path.abspath('../'))
from DataBase import DAO as DAO

# 結果のデータベース名
RESULT_DB_NAME = 'Result.db'

# データベースのテーブルの名前
TABLE_NAME = 'Result'

# カラム名
COLUMN_FILE_NAME = 'file_name'
COLUMN_CLONE_LINES = 'clone_lines'
COLUMN_CLONE_LINE_COUNT = 'clone_line_count'
COLUMN_LINE_COUNT = 'line_count'
COLUMN_CLONE_RATE = 'clone_rate'

# スキーマ定義
TABLE_SCHEMA = f'''id INTEGER PRIMARY KEY AUTOINCREMENT,
                {COLUMN_FILE_NAME} TEXT,
                {COLUMN_CLONE_LINES} TEXT,
                {COLUMN_CLONE_LINE_COUNT} INTEGER,
                {COLUMN_LINE_COUNT} INTEGER,
                {COLUMN_CLONE_RATE} REAL'''
INSERT_SCHEMA = DAO.get_insert_schema(TABLE_NAME,
    [COLUMN_FILE_NAME,
        COLUMN_CLONE_LINES, COLUMN_CLONE_LINE_COUNT,
        COLUMN_LINE_COUNT, COLUMN_CLONE_RATE])

# クローンのデータベースのフォルダ名
@dataclass
class ResultData:
    file_id: int
    file_name: str
    clone_lines: str
    clone_line_count: int
    line_count: int
    clone_rate: float