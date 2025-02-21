import os
import sys

sys.path.append(os.path.abspath('../'))
from Common import PathManager as PathManager

# 画像サイズ
FIGURE_WIDTH = 10
FIGURE_HEIGHT = 6

# ラベル
Y_LABEL = 'Clone Rate'

# プロジェクトごとのファイル内クローンの箱ひげ図
ALL_PROJECT_CLONE_RATE_FILE_NAME = 'AllProjectLineCloneRate'

ALL_PROJECT_CLONE_RATE_TITLE = 'Line Clone Rate'

# 全プロジェクトの箱ひげ図
TOTAL_CLONE_RATE_FILE_NAME = 'TotalProjectCloneRate'

TOTAL_CLONE_RATE_TITLE = 'Total Clone Rate'

TOTAL_LINE_CLONE_RATE_LABEL = 'Total Line Clone Rate'
TOTAL_FILE_CLONE_RATE_LABEL = 'Total File Clone Rate'

def get_save_path(engine_name):
    '''箱ひげ図の保存先のパス'''

    return PathManager.get_path(engine_name, PathManager.BOX_PLOT_FOLDER_NAME)