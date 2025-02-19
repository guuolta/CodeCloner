import os
import re
import sys

from CloneSet import CloneSetData as CloneSetData
import CommonAnalyze as CommonAnalyze

sys.path.append(os.path.abspath('../'))
from Common import FileManager as FileManager
from Common import PathManager as PathManager
from CCFinderSW import CCFinderSWData as CCFinderSWData
from DataBase import DAO as DAO

''' テーブル作成
'''
def create_table(cur):
    DAO.create_table(cur, CloneSetData.TABLE_NAME, CloneSetData.TABLE_SCHEMA)

''' クローンセットのIDを取得
'''
def get_id(line):
    return re.findall(fr'{CCFinderSWData.CLONE_SET_HEADER}(\d+)', line)[0]

''' クローンセットのデータを取得
'''
def get_clone_sets(line):
    return re.findall(r'\d+', line)

''' クローンセットのデータを作成
'''
def create_clone_set_file_data(id, clone_id, clone_set_datas):
    # データセットが足りない場合はスキップ
    if len(clone_set_datas) < CloneSetData.CCFINDERSW_CLONE_SET_DATASET_COUNT:
        return

    # 要素を取得
    file_id = int(clone_set_datas[CloneSetData.CCFINDERSW_FILE_ID_INDEX])
    start_line = int(clone_set_datas[CloneSetData.CCFINDERSW_START_LINE_INDEX])
    start_token = int(clone_set_datas[CloneSetData.CCFINDERSW_START_TOKEN_INDEX])
    end_line = int(clone_set_datas[CloneSetData.CCFINDERSW_END_LINE_INDEX])
    end_token = int(clone_set_datas[CloneSetData.CCFINDERSW_END_TOKEN_INDEX])

    return CloneSetData.CloneSet(id, clone_id, file_id, start_line, start_token, end_line, end_token)

''' ファイル情報をデータベースに挿入
'''
def inset(cur, clone_set):
    cur.execute(CloneSetData.INSERT_SCHEMA,
                (clone_set.id, clone_set.clone_id, clone_set.file_id, clone_set.start_line, clone_set.start_token, clone_set.end_line, clone_set.end_token))