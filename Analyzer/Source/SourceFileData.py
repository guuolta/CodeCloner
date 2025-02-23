import os
import sys
from dataclasses import dataclass

sys.path.append(os.path.abspath('../'))
from DataBase import DAO as DAO
from DataBase import DBData as DBData

# ソースファイルデータベースの名前
SOURCE_FILE_DB_NAME = 'SourceFile.db'

# データベースのテーブルの名前
TABLE_NAME = 'SourceFile'

# ソースファイルのパラメータ数
CCFINDERSW_SOURCE_FILE_DATASET_COUNT = 4
# CCFinderの結果のインデックス
CCFINDERSW_ID_INDEX = 0
CCFINDERSW_LINE_COUNT_INDEX = 1
CCFINDERSW_TOKEN_COUNT_INDEX = 2
CCFINDERSW_FILE_PATH_INDEX = 3

# ソースファイルのインデックス
ID_INDEX = 0
NAME_INDEX = 1
LINES_INDEX = 2
TOKENS_INDEX = 3
PATH_INDEX = 4

# カラム名
COLUMN_NAME = 'name'
COLUMN_LINE_COUNT = 'line_count'
COLUMN_TOKEN_COUNT = 'token_count'
COLUMN_PATH = 'path'

# スキーマ定義
TABLE_SCHEMA = f'''{DBData.COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                {COLUMN_NAME} TEXT,
                {COLUMN_LINE_COUNT} INTEGER,
                {COLUMN_TOKEN_COUNT} INTEGER,
                {COLUMN_PATH} TEXT'''

INSERT_SCHEMA = DAO.get_insert_schema(TABLE_NAME,
    [COLUMN_NAME, COLUMN_LINE_COUNT, COLUMN_TOKEN_COUNT, COLUMN_PATH])

# ソースファイルの要素
@dataclass
class SourceFile:
    id: int
    name: str
    line_count: int
    token_count: int
    path: str