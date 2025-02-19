"""テーブルを削除して再作成する
cur: SQLiteカーソルオブジェクト
table_name: 作成するテーブル名
schema: CREATE TABLE のスキーマ定義
"""
def create_table(cur, table_name, schema):
    # テーブルが存在する場合削除
    cur.execute(f'DROP TABLE IF EXISTS {table_name}')

    # テーブルを再作成
    cur.execute(f'CREATE TABLE {table_name} ({schema})')

''' 全てのカラムを取得
'''
def get_all_columns(cur, table_name):
    data = cur.execute(f'SELECT * FROM {table_name}')
    return data.fetchall()

"""INSERT スキーマを取得する
table_name: テーブル名
columns: カラム名リスト
"""
def get_insert_schema(table_name, columns):
    return f'''INSERT INTO {table_name}
                (id, {', '.join(columns)})
                VALUES (?, {', '.join(['?' for _ in columns])})
                ON CONFLICT(id) DO UPDATE SET
                {', '.join([f'{column} = excluded.{column}' for column in columns])};'''