import os
import sqlite3
import sys
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath('../'))
from DataBase import DAO
from Common import PathManager as PathManager
from Common import FileManager as FileManager

def save_figure(save_folder_path, file_name, fig):
    ''' 図を保存(png)

    save_folder_path: 保存先フォルダパス

    file_name: 保存ファイル名(拡張子は不要)

    fig: 保存する図
    '''

    # 保存先フォルダが存在しない場合は作成
    FileManager.create_unique_folder(save_folder_path)

    save_path = PathManager.join_path(save_folder_path, f"{file_name}.png")
    fig.savefig(save_path, format='png')