import os
import sys
from dataclasses import dataclass

sys.path.append(os.path.abspath('../'))
from DataBase import DAO as DAO

# ソースファイルデータベースの名前
CLONE_SETS_DB_NAME = 'CloneSet.db'

# データベースのテーブルの名前
TABLE_NAME = 'CloneSet'

# クローンセットデータ数(IDは除く)
CCFINDERSW_CLONE_SET_DATASET_COUNT = 5
# CCFinderの結果のインデックス
CCFINDERSW_FILE_ID_INDEX = 0
CCFINDERSW_START_LINE_INDEX = 1
CCFINDERSW_START_TOKEN_INDEX = 2
CCFINDERSW_END_LINE_INDEX = 3
CCFINDERSW_END_TOKEN_INDEX = 4

# インデックス
ID_INDEX = 0
CLONE_ID_INDEX = 1
FILE_ID_INDEX = 2
START_LINE_INDEX = 3
START_TOKEN_INDEX = 4
END_LINE_INDEX = 5
END_TOKEN_INDEX = 6

# スキーマ定義
TABLE_SCHEMA = '''id INTEGER PRIMARY KEY AUTOINCREMENT,
                clone_id INTEGER,
                file_id INTEGER,
                start_line INTEGER,
                start_token INTEGER,
                end_line INTEGER,
                end_token INTEGER'''
INSERT_SCHEMA = DAO.get_insert_schema(TABLE_NAME,
    ['clone_id', 'file_id', 'start_line', 'start_token', 'end_line', 'end_token'])

# クローンセットの要素
@dataclass
class CloneSet:
    id: int
    clone_id: int
    file_id: int
    start_line: int
    start_token: int
    end_line: int
    end_token: int