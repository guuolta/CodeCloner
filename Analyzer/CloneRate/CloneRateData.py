import os
import sys
from dataclasses import dataclass
import Analyzer.Result as Result

sys.path.append(os.path.abspath('../'))
from DataBase import DAO as DAO
from DataBase import DBData as DBData

# データベース名
DB_NAME = 'CloneRate.db'

# データベースのテーブルの名前
TABLE_NAME = 'CloneRate'

# カラム名
COLUMN_PROJECT_NAME = 'project_name'
COLUMN_FILE_COUNT = 'file_count'
COLUMN_FILE_CLONE_COUNT = 'file_clone_count'
COLUMN_FILE_CLONE_RATE = 'file_clone_rate'
COLUMN_LINE_COUNT = 'line_count'
COLUMN_LINE_CLONE_COUNT = 'line_clone_count'
COLUMN_LINE_CLONE_RATE = 'line_clone_rate'

# スキーマ定義
TABLE_SCHEMA = f'''{DBData.COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                {COLUMN_PROJECT_NAME} TEXT,
                {COLUMN_FILE_COUNT} INTEGER,
                {COLUMN_FILE_CLONE_COUNT} INTEGER,
                {COLUMN_FILE_CLONE_RATE} REAL,
                {COLUMN_LINE_COUNT} INTEGER,
                {COLUMN_LINE_CLONE_COUNT} INTEGER,
                {COLUMN_LINE_CLONE_RATE} REAL'''

INSERT_SCHEME = DAO.get_insert_schema(TABLE_NAME,
    [COLUMN_PROJECT_NAME,
        COLUMN_FILE_COUNT, COLUMN_FILE_CLONE_COUNT, COLUMN_FILE_CLONE_RATE,
        COLUMN_LINE_COUNT, COLUMN_LINE_CLONE_COUNT, COLUMN_LINE_CLONE_RATE])

SELECT_SCHEME = f'''SELECT COUNT(*),
        SUM({Result.ResultData.COLUMN_LINE_COUNT}),
        SUM({Result.ResultData.COLUMN_CLONE_LINE_COUNT}),
        COUNT(CASE WHEN clone_rate > 0 THEN 1 END)
        FROM {Result.ResultData.TABLE_NAME}'''

# クローン率のデータベースのフォルダ名
@dataclass
class CloneRate:
    id: int
    project_name: str
    file_count: int
    file_clone_count: int
    file_clone_rate: float
    line_count: int
    line_clone_count: int
    line_clone_rate: float