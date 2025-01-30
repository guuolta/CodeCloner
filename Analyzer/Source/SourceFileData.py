from dataclasses import dataclass

# データベースのテーブルの名前
TABLE_NAME = 'SourceFiles'

# ソースファイルのパラメータ数
SOURCE_FILE_DATASET_COUNT = 4
# パラメターごとのインデックス
ID_INDEX = 0
LINE_COUNT_INDEX = 1
TOKEN_COUNT_INDEX = 2
FILE_PATH_INDEX = 3

# スキーマ定義
SCHEMA = '''id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT, 
                lines INTEGER, 
                tokens INTEGER, 
                path TEXT'''

# ソースファイルの要素
@dataclass
class SourceFile:
    id: int
    name: str
    lines: int
    tokens: int
    path: str