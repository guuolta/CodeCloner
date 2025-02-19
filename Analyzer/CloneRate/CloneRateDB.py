import os
import sys
from CloneRate import CloneRateData as CloneRateData

sys.path.append(os.path.abspath('../'))
from DataBase import DAO

''' ファイル情報をデータベースに挿入
'''
def create_table(cur):
    DAO.create_table(cur, CloneRateData.TABLE_NAME, CloneRateData.TABLE_SCHEMA)

''' ファイル情報をデータベースに挿入
'''
def insert(cur, clone_rate_data):
    cur.execute(CloneRateData.INSERT_SCHEME,
                    (clone_rate_data.file_name,
                        clone_rate_data.file_count, clone_rate_data.file_clone_count, clone_rate_data.file_clone_rate,
                        clone_rate_data.line_count, clone_rate_data.line_clone_count, clone_rate_data.line_clone_rate))

''' クローン率のデータを作成
'''
def create_clone_rate_data(file_name, analyze_cur, rate_cur):
    line_count = 0
    clone_line_count = 0
    clone_file_count = 0

    analyze_cur.execute(f"SELECT file_name, clone_line_count, line_count, clone_rate FROM {CloneRateData.TABLE_NAME}")
    datas = analyze_cur.fetchall()

    for data in datas:
        line_count += data[2]
        clone_line_count += data[1]
        if data[3] > 0:
            clone_file_count += 1

    return CloneRateData.CloneRate(file_name,
                                len(datas),
                                clone_file_count,
                                clone_file_count / (1 if len(datas)==0 else len(datas)),
                                line_count,
                                clone_line_count,
                                clone_line_count / (1 if line_count == 0 else line_count))
