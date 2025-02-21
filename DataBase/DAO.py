def create_table(cur, table_name, schema):
    """テーブルを削除して再作成する

    cur: SQLiteカーソルオブジェクト

    table_name: 作成するテーブル名

    schema: CREATE TABLE のスキーマ定義
    """

    # テーブルが存在する場合削除
    cur.execute(f'DROP TABLE IF EXISTS {table_name}')

    # テーブルを再作成
    cur.execute(f'CREATE TABLE {table_name} ({schema})')

def get_all_columns(cur, table_name):
    ''' 全てのカラムを取得'''

    data = cur.execute(f'SELECT * FROM {table_name}')
    return data.fetchall()

def get_column(cur, table_name, column):
    ''' 指定したカラムを取得(単体)'''

    data = cur.execute(f'SELECT {column} FROM {table_name}')
    return [row[0] for row in data.fetchall()]

def get_columns(cur, table_name, *columns):
    ''' 指定したカラムを取得(複数)'''

    data = cur.execute(f'SELECT {", ".join(columns)} FROM {table_name}')
    return data.fetchall()

def get_column_sum(cur, table_name, *columns):
    ''' 指定したカラムの値の合計を取得'''

    data = cur.execute(f'SELECT {", ".join([f"SUM({col})" for col in columns])} FROM {table_name}')
    return data.fetchone()

def get_insert_schema(table_name, columns):
    """ INSERT スキーマを取得する """

    return f'''INSERT INTO {table_name}
                (id, {', '.join(columns)})
                VALUES (?, {', '.join(['?' for _ in columns])})
                ON CONFLICT(id) DO UPDATE SET
                {', '.join([f'{column} = excluded.{column}' for column in columns])};'''