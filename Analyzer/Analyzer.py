import os
import sys
import sqlite3

from Source import SourceFileDB as SourceFileDB
from Source import SourceFileData as SourceFileData

from CloneSet import CloneSetDB as CloneSetDB
from CloneSet import CloneSetData as CloneSetData

from Result import ResultDB as ResultDB
from Result import ResultData as ResultData

from CloneRate import CloneRateDB as CloneRateDB
from CloneRate import CloneRateData as CloneRateData

import CommonAnalyze as CommonAnalyze

sys.path.append(os.path.abspath('../'))
from Common import FileManager as FileManager
from Common import PathManager as PathManager
from CCFinderSW import CCFinderSWData as CCFinderSWData
from DataBase import DAO as DAO

def Analyze(engine_name):
    output_folder_path = CommonAnalyze.get_output_folder_path(engine_name)

    for root, _, files in os.walk(output_folder_path):
        for file in files:
            if not file.endswith(CCFinderSWData.OUTPUT_EXTENSION):
                continue
            create_db(engine_name, FileManager.get_file_name(file), PathManager.join_path(root, file))

    create_clone_rate_db(engine_name)

''' CCFinderSWの解析結果ファイルをデータベースに登録
'''
def create_db(engine_name, folder_name, output_file_path):
    FileManager.create_unique_folder(PathManager.get_path(engine_name, PathManager.DATA_BASE_FOLDER_NAME, folder_name))

    # データベースファイルを作成
    source_file_cur = sqlite3.connect(CommonAnalyze.get_db_path(engine_name, folder_name, SourceFileData.SOURCE_FILE_DB_NAME))
    clone_set_cur = sqlite3.connect(CommonAnalyze.get_db_path(engine_name, folder_name, CloneSetData.CLONE_SETS_DB_NAME))
    result_cur = sqlite3.connect(CommonAnalyze.get_db_path(engine_name, folder_name, ResultData.RESULT_DB_NAME))

    # テーブル作成
    SourceFileDB.create_table(source_file_cur)
    CloneSetDB.create_table(clone_set_cur)
    ResultDB.create_table(result_cur)

    contents = FileManager.read_file(output_file_path)

    # クローンセットの部分が始まるか確認
    is_start_clone_sets = False
    id = 0

    for line in contents:
        # SOURCE_FILES_HEADER~CLONE_SETS_HEADERの間はソースファイルのデータ
        # それ以降はクローンセットのデータ
        if line.startswith(CCFinderSWData.SOURCE_FILES_HEADER):
            is_start_clone_sets = False
            continue
        elif line.startswith(CCFinderSWData.CLONE_SETS_HEADER):
            is_start_clone_sets = True
            continue

        if not is_start_clone_sets:
            # ソースファイルのデータをデータベースに登録
            data = SourceFileDB.create_source_file_data(line)
            if data is not None:
                SourceFileDB.inset(source_file_cur, data)
        else:
            # cloneIDが書かれている行ならID設定
            if line.startswith(CCFinderSWData.CLONE_SET_HEADER):
                clone_id = CloneSetDB.get_id(line)
                continue

            # クローンのデータをデータベースに登録
            clone_sets = CloneSetDB.get_clone_sets(line)
            CloneSetDB.inset(clone_set_cur, CloneSetDB.create_clone_set_file_data(id, clone_id, clone_sets))

            # IDを次のものに設定
            id += 1

    # コミット
    source_file_cur.commit()
    clone_set_cur.commit()

    # クローン率のデータを作成
    source_files=DAO.get_all_columns(source_file_cur, SourceFileData.TABLE_NAME)
    clone_files=DAO.get_all_columns(clone_set_cur, CloneSetData.TABLE_NAME)

    clone_line_flags = ResultDB.get_clone_line_flags(source_file_cur, clone_files)
    for source_file in source_files:
        data = ResultDB.create_result_data(source_file, clone_line_flags[source_file[SourceFileData.ID_INDEX]])
        ResultDB.insert(result_cur, data)

    # コミット
    result_cur.commit()

    # ファイルを閉じる
    source_file_cur.close()
    clone_set_cur.close()
    result_cur.close()

''' 全プロジェクトのクローン率のデータベースを作成
'''
def create_clone_rate_db(engine_name):
    clone_rate_folder_path = PathManager.get_path(engine_name, PathManager.DATA_BASE_FOLDER_NAME, PathManager.CLONE_RATE_DB_FOLDER_NAME)
    FileManager.create_unique_folder(clone_rate_folder_path)

    # データベースファイルを作成
    clone_rate_cur = sqlite3.connect(PathManager.join_path(clone_rate_folder_path, CloneRateData.DB_NAME))

    # テーブル作成
    CloneRateDB.create_table(clone_rate_cur)

    dataset_folder_path = PathManager.get_path(engine_name, PathManager.DATA_BASE_FOLDER_NAME)

    id = 0
    for root, _, files in os.walk(dataset_folder_path):
        for file in files:
            if not file == ResultData.RESULT_DB_NAME:
                continue
            result_cur = sqlite3.connect(PathManager.join_path(root, file))

            data = CloneRateDB.create_clone_rate_data(result_cur, id, os.path.basename(root))
            CloneRateDB.insert(clone_rate_cur, data)

            id += 1
            result_cur.close()
    
    # コミット
    clone_rate_cur.commit()

    # ファイルを閉じる
    clone_rate_cur.close()