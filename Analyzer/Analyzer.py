import os
import sys
import sqlite3

import Analyzer.Source as Source
import Analyzer.CloneSet as CloneSet
import Analyzer.Result as Result
import Analyzer.CloneRate as CloneRate

sys.path.append(os.path.abspath('../'))
from Common import Calculater as Calculater
from Common import FileManager as FileManager
from Common import PathManager as PathManager
from CCFinderSW import CCFinderSWData as CCFinderSWData
from DataBase import DAO as DAO

def create_db(engine_name):
    ''' 全プロジェクトのCCFinderSWの解析結果ファイルをデータベースに登録 '''

    output_folder_path = _get_output_folder_path(engine_name)

    for root, _, files in os.walk(output_folder_path):
        for file in files:
            if not file.endswith(CCFinderSWData.OUTPUT_EXTENSION):
                continue
            _create_db(engine_name, CCFinderSWData.get_repository_name(file), PathManager.join_path(root, file))

    _create_clone_rate_db(engine_name)

def get_project_names(engine_name):
    ''' プロジェクトの名前を取得'''

    clone_rate_cur = sqlite3.connect(_get_db_path(engine_name, PathManager.CLONE_RATE_DB_FOLDER_NAME, CloneRate.CloneRateData.DB_NAME))
    return DAO.get_column(clone_rate_cur, CloneRate.CloneRateData.TABLE_NAME, CloneRate.CloneRateData.COLUMN_PROJECT_NAME)

def get_project_clone_rates(engine_name):
    ''' プロジェクトごとのファイル内クローン率を取得 '''

    project_clone_rates = []

    # データベースのフォルダパス
    data_base_folder_path = PathManager.get_path(engine_name, PathManager.DATA_BASE_FOLDER_NAME)

    for root, _, files in os.walk(data_base_folder_path):
        for file in files:
            # クローン率のデータベース以外はスキップ
            if not file == Result.ResultData.RESULT_DB_NAME:
                continue

            with sqlite3.connect(PathManager.join_path(root, file)) as result_cur:
                project_clone_rates.append(DAO.get_column(result_cur, Result.ResultData.TABLE_NAME, Result.ResultData.COLUMN_CLONE_RATE))

    return project_clone_rates

def get_file_clone_rates(engine_name):
    ''' 全プロジェクトのファイルクローン率を取得 '''

    clone_rate_cur = sqlite3.connect(_get_db_path(engine_name, PathManager.CLONE_RATE_DB_FOLDER_NAME, CloneRate.CloneRateData.DB_NAME))
    return DAO.get_column(clone_rate_cur, CloneRate.CloneRateData.TABLE_NAME, CloneRate.CloneRateData.COLUMN_FILE_CLONE_RATE)

def get_line_clone_rates(engine_name):
    ''' 全プロジェクトの行クローン率を取得 '''

    clone_rate_cur = sqlite3.connect(_get_db_path(engine_name, PathManager.CLONE_RATE_DB_FOLDER_NAME, CloneRate.CloneRateData.DB_NAME))
    return DAO.get_column(clone_rate_cur, CloneRate.CloneRateData.TABLE_NAME, CloneRate.CloneRateData.COLUMN_LINE_CLONE_RATE)

def calculate_line_clone_rate(engine_name):
    ''' プロジェクトの行のクローン率を計算 '''

    clone_rate_cur = sqlite3.connect(_get_db_path(engine_name, PathManager.CLONE_RATE_DB_FOLDER_NAME, CloneRate.CloneRateData.DB_NAME))
    # 全行数と全クローン行数を取得
    line_data = DAO.get_column_sum(clone_rate_cur,
        CloneRate.CloneRateData.TABLE_NAME,
        CloneRate.CloneRateData.COLUMN_LINE_COUNT,
        CloneRate.CloneRateData.COLUMN_LINE_CLONE_COUNT)

    if line_data is None:
        return 0

    return Calculater.calculate_clone_rate(line_data[0], line_data[1])

def calculate_file_clone_rate(engine_name):
    ''' プロジェクトのファイルのクローン率を計算 '''

    clone_rate_cur = sqlite3.connect(_get_db_path(engine_name, PathManager.CLONE_RATE_DB_FOLDER_NAME, CloneRate.CloneRateData.DB_NAME))
    # 全ファイル数と全クローンファイル数を取得
    file_data = DAO.get_column_sum(clone_rate_cur,
        CloneRate.CloneRateData.TABLE_NAME,
        CloneRate.CloneRateData.COLUMN_FILE_COUNT,
        CloneRate.CloneRateData.COLUMN_FILE_CLONE_COUNT)

    if file_data is None:
        return 0

    return Calculater.calculate_clone_rate(file_data[0], file_data[1])

def _create_db(engine_name, folder_name, output_file_path):
    ''' 対象プロジェクトのCCFinderSWの解析結果ファイルをデータベースに登録 '''

    # 対象プロジェクトのデータベースを保管するフォルダを作成
    FileManager.create_unique_folder(PathManager.get_path(engine_name, PathManager.DATA_BASE_FOLDER_NAME, folder_name))

    # データベースファイルを作成
    source_file_cur = sqlite3.connect(_get_db_path(engine_name, folder_name, Source.SourceFileData.SOURCE_FILE_DB_NAME))
    clone_set_cur = sqlite3.connect(_get_db_path(engine_name, folder_name, CloneSet.CloneSetData.CLONE_SETS_DB_NAME))
    result_cur = sqlite3.connect(_get_db_path(engine_name, folder_name, Result.ResultData.RESULT_DB_NAME))

    # テーブル作成
    Source.SourceFileDB.create_table(source_file_cur)
    CloneSet.CloneSetDB.create_table(clone_set_cur)
    Result.ResultDB.create_table(result_cur)

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
            data = Source.SourceFileDB.create_source_file_data(line)
            if data is not None:
                Source.SourceFileDB.inset(source_file_cur, data)
        else:
            # cloneIDが書かれている行ならID設定
            if line.startswith(CCFinderSWData.CLONE_SET_HEADER):
                clone_id = CloneSet.CloneSetDB.get_id(line)
                continue

            # クローンのデータをデータベースに登録
            clone_sets = CloneSet.CloneSetDB.get_clone_sets(line)
            CloneSet.CloneSetDB.inset(clone_set_cur, CloneSet.CloneSetDB.create_clone_set_file_data(id, clone_id, clone_sets))

            # IDを次のものに設定
            id += 1

    # コミット
    source_file_cur.commit()
    clone_set_cur.commit()

    # クローン率のデータを作成
    source_files=DAO.get_all_columns(source_file_cur, Source.SourceFileData.TABLE_NAME)
    clone_files=DAO.get_all_columns(clone_set_cur, CloneSet.CloneSetData.TABLE_NAME)

    clone_line_flags = Result.ResultDB.get_clone_line_flags(source_file_cur, clone_files)
    for source_file in source_files:
        data = Result.ResultDB.create_result_data(source_file, clone_line_flags[source_file[Source.SourceFileData.ID_INDEX]])
        Result.ResultDB.insert(result_cur, data)

    # コミット
    result_cur.commit()

    # ファイルを閉じる
    source_file_cur.close()
    clone_set_cur.close()
    result_cur.close()

def _create_clone_rate_db(engine_name):
    ''' 全プロジェクトのクローン率のデータベースを作成 '''

    # クローン率のデータベースを保管するフォルダを作成
    clone_rate_folder_path = PathManager.get_path(engine_name, PathManager.DATA_BASE_FOLDER_NAME, PathManager.CLONE_RATE_DB_FOLDER_NAME)
    FileManager.create_unique_folder(clone_rate_folder_path)

    # データベースファイルを作成
    clone_rate_cur = sqlite3.connect(PathManager.join_path(clone_rate_folder_path, CloneRate.CloneRateData.DB_NAME))

    # テーブル作成
    CloneRate.CloneRateDB.create_table(clone_rate_cur)

    # データベースのフォルダパス
    data_base_folder_path = PathManager.get_path(engine_name, PathManager.DATA_BASE_FOLDER_NAME)

    # プロジェクトID
    id = 0
    for root, _, files in os.walk(data_base_folder_path):
        for file in files:
            # クローン率のデータベース以外はスキップ
            if not file == Result.ResultData.RESULT_DB_NAME:
                continue

            # プロジェクトごとのクローン率の情報をデータベースに格納
            with sqlite3.connect(PathManager.join_path(root, file)) as result_cur:
                data = CloneRate.CloneRateDB.create_clone_rate_data(result_cur, id, os.path.basename(root))
                CloneRate.CloneRateDB.insert(clone_rate_cur, data)

                id += 1

    # コミット
    clone_rate_cur.commit()

    # ファイルを閉じる
    clone_rate_cur.close()

def _get_output_folder_path(engine_name):
    ''' CCfinderSWの解析結果ファイルを保管するフォルダのパスを取得 '''

    return PathManager.get_path(engine_name, PathManager.CCFINDERSW_RESULT_FOLDER_NAME)

def _get_db_path(engine_name, folder_name, db_name):
    ''' データベースファイルのパスを取得 '''

    return PathManager.get_path(engine_name, PathManager.DATA_BASE_FOLDER_NAME, folder_name, db_name)