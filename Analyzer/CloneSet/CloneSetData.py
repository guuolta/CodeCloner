import os
import sys
from dataclasses import dataclass

sys.path.append(os.path.abspath('../'))
from DataBase import DAO as DAO
from DataBase import DBData as DBData

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

# カラム名
COLUMN_CLONE_ID = 'clone_id'
COLUMN_FILE_ID = 'file_id'
COLUMN_START_LINE = 'start_line'
COLUMN_START_TOKEN = 'start_token'
COLUMN_END_LINE = 'end_line'
COLUMN_END_TOKEN = 'end_token'

# スキーマ定義
TABLE_SCHEMA = f'''{DBData.COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                {COLUMN_CLONE_ID} INTEGER,
                {COLUMN_FILE_ID} INTEGER,
                {COLUMN_START_LINE} INTEGER,
                {COLUMN_START_TOKEN} INTEGER,
                {COLUMN_END_LINE} INTEGER,
                {COLUMN_END_TOKEN} INTEGER'''

INSERT_SCHEMA = DAO.get_insert_schema(TABLE_NAME,
    [COLUMN_CLONE_ID, COLUMN_FILE_ID,
        COLUMN_START_LINE, COLUMN_START_TOKEN,
        COLUMN_END_LINE, COLUMN_END_TOKEN])

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