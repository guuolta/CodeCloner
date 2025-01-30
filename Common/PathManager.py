import PathData
import os

''' フルパスを取得する
'''
def get_path(engine_name, folder_name):
    return os.path.join(PathData.CCFINDERSW_PATH, engine_name, folder_name)

''' パスを結合する
'''
def join_path(*args):
    return os.path.join(*args)

''' CCfinderSWの解析結果ファイル名を取得する
'''
def get_ccfindersw_result_file_name(repository_name):
    return f"{repository_name}_ccfsw.txt"