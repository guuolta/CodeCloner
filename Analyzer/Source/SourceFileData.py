import os
import sys
from dataclasses import dataclass

sys.path.append(os.path.abspath('../'))
from DataBase import DAO as DAO

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

# スキーマ定義
TABLE_SCHEMA = '''id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT, 
                lines INTEGER, 
                tokens INTEGER, 
                path TEXT'''
INSERT_SCHEMA = DAO.get_insert_schema(TABLE_NAME,
    ['name', 'lines', 'tokens', 'path'])

# ソースファイルの要素
@dataclass
class SourceFile:
    id: int
    name: str
    lines: int
    tokens: int
    path: str