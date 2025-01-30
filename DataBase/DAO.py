"""テーブルを削除して再作成する汎用関数。
Parameters:
cur (sqlite3.Cursor): SQLiteカーソルオブジェクト。
table_name (str): 作成するテーブル名。
schema (str): CREATE TABLE のスキーマ定義。
"""
def create_table(cur, table_name, schema):
    # テーブルが存在する場合削除
    cur.execute(f'DROP TABLE IF EXISTS {table_name}')

    # テーブルを再作成
    cur.execute(f'CREATE TABLE {table_name} ({schema})')
