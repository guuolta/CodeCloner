import os
import sys
import sqlite3

from Source import SourceFileDB as SourceFileDB
from Source import SourceFileData as SourceFileData

from CloneSet import CloneSetDB as CloneSetDB
from CloneSet import CloneSetData as CloneSetData

from Result import ResultDB as ResultDB
from Result import ResultData as ResultData

import CommonAnalyze as CommonAnalyze

sys.path.append(os.path.abspath('../'))
from Common import FileManager as FileManager
from Common import PathManager as PathManager
from CCFinderSW import CCFinderSWData as CCFinderSWData
from DataBase import DAO as DAO

def to_database(engine_name, folder_name, output_file_path):
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

    source_files=DAO.get_all_columns(source_file_cur, SourceFileData.TABLE_NAME)
    clone_files=DAO.get_all_columns(clone_set_cur, CloneSetData.TABLE_NAME)

    clone_line_flags = ResultDB.get_clone_line_flags(source_file_cur, clone_files)
    for source_file in source_files:
        data = ResultDB.create_result_data(source_file, clone_line_flags[source_file[SourceFileData.ID_INDEX]])
        ResultDB.insert(result_cur, data)

    result_cur.commit()

    # ファイルを閉じる
    source_file_cur.close()
    clone_set_cur.close()
    result_cur.close()

to_database('GameMaker', 'arcane.git', PathManager.get_path('GameMaker', PathManager.CCFINDERSW_RESULT_FOLDER_NAME, 'arcane.git_output_ccfsw.txt'))

