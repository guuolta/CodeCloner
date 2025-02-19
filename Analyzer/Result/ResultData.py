import os
import sys
from dataclasses import dataclass

sys.path.append(os.path.abspath('../'))
from DataBase import DAO as DAO

# 結果のデータベース名
RESULT_DB_NAME = 'Result.db'

# データベースのテーブルの名前
TABLE_NAME = 'Result'

# スキーマ定義
TABLE_SCHEMA = '''id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT,
                clone_lines TEXT,
                clone_line_count INTEGER,
                line_count INTEGER,
                clone_rate REAL'''
INSERT_SCHEMA = DAO.get_insert_schema(TABLE_NAME,
    ['file_name',
        'clone_lines', 'clone_line_count',
        'line_count', 'clone_rate'])

# クローンのデータベースのフォルダ名
@dataclass
class ResultData:
    file_id: int
    file_name: str
    clone_lines: str
    clone_line_count: int
    line_count: int
    clone_rate: float