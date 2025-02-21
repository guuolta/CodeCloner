import os
import sys
from Analyzer.CloneRate import CloneRateData

sys.path.append(os.path.abspath('../'))
from DataBase import DAO
from Common import PathManager as PathManager
from Common import Calculater as Calculater

''' ファイル情報をデータベースに挿入
'''
def create_table(cur):
    DAO.create_table(cur, CloneRateData.TABLE_NAME, CloneRateData.TABLE_SCHEMA)

''' クローン率のデータを作成
'''
def create_clone_rate_data(result_cur, id, file_name):
    data = result_cur.execute(CloneRateData.SELECT_SCHEME).fetchall()

    file_count = data[0][0]
    line_count = data[0][1] if data[0][1] is not None else 0
    clone_line_count = data[0][2] if data[0][2] is not None else 0
    clone_file_count = data[0][3]


    return CloneRateData.CloneRate(id, file_name,
                                file_count,
                                clone_file_count,
                                Calculater.calculate_clone_rate(file_count, clone_file_count),
                                line_count,
                                clone_line_count,
                                Calculater.calculate_clone_rate(line_count, clone_line_count))

''' ファイル情報をデータベースに挿入
'''
def insert(cur, clone_rate_data):
    cur.execute(CloneRateData.INSERT_SCHEME,
                    (clone_rate_data.id, clone_rate_data.project_name,
                        clone_rate_data.file_count, clone_rate_data.file_clone_count, clone_rate_data.file_clone_rate,
                        clone_rate_data.line_count, clone_rate_data.line_clone_count, clone_rate_data.line_clone_rate))
