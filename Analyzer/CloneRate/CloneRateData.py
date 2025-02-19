import os
import sys
from dataclasses import dataclass

sys.path.append(os.path.abspath('../'))
from DataBase import DAO as DAO

# データベース名
DB_NAME = 'CloneRate.db'

# データベースのテーブルの名前
TABLE_NAME = 'CloneRate'

# スキーマ定義
TABLE_SCHEMA = '''id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT,
                file_count INTEGER,
                file_clone_count INTEGER,
                file_clone_rate REAL,
                line_count INTEGER,
                line_clone_count INTEGER,
                line_clone_rate REAL'''

INSERT_SCHEME = DAO.get_insert_schema(TABLE_NAME,
    ['project_name',
        'file_count', 'file_clone_count', 'file_clone_rate',
        'line_count', 'line_clone_count', 'line_clone_rate'])


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