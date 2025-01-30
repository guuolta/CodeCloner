import sqlite3
import Common

FOLDER_NAME = ''
DB_NAME = 'CloneRate.db'
TABLE_NAME = 'clone_rate'

def main():
    if FOLDER_NAME != '':
        conn = sqlite3.connect(Common.get_db_path(FOLDER_NAME, DB_NAME))
    else:
        conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    print_files(cur)
    print('-----------------')

def print_files(cur):
    cur.execute(f'SELECT * FROM {TABLE_NAME}')
    files = cur.fetchall()

    for file in files:
        print(file)

main()