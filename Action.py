''' ツールを使うためのスクリプト '''

import os
import sys

from Formater import CreateFolderFormat as CreateFolderFormat

# Git関連
from Git import GitHandler as GitHandler

# データセット関連
from DataSets import ProgramExtract as ProgramExtract

# CCFinderSW関連
from CCFinderSW import CCFinderSWHandler as CCFinderSWHandler

# データベース関連
from Analyzer import Analyzer as Analyzer

# 図式化関連
from Visualization.BoxPlot import BoxPloter as BoxPloter

def analyze():
    engine_name = sys.argv[1]
    language = sys.argv[2]
    extensions = sys.argv[3:]

    my_path = os.path.abspath(os.path.dirname(__file__))

    # GitHubのリポジトリをクローン
    GitHandler.clone(engine_name)

    # プログラムファイルのみを抽出
    ProgramExtract.extract(engine_name, extensions)

    # CCFinderSWでデータセットからクローンを調査
    CCFinderSWHandler.analyze(engine_name, extensions, language, my_path)

    # CCFinderSWの解析結果からデータベースを作成
    Analyzer.create_db(engine_name)

    # プロジェクトごとのファイル内クローン率を箱ひげ図で表示
    project_names = Analyzer.get_project_names(engine_name)
    project_clone_rates = Analyzer.get_project_clone_rates(engine_name)

    BoxPloter.create_all_project_clone_rate_box_plot(engine_name, project_names, project_clone_rates)

    # 全プロジェクトのクローン率を箱ひげ図で表示
    line_clone_rates = Analyzer.get_line_clone_rates(engine_name)
    file_clone_rates = Analyzer.get_file_clone_rates(engine_name)

    BoxPloter.create_total_project_clone_rate_box_plot(engine_name, line_clone_rates, file_clone_rates)

    # 全プロジェクトのクローン率を表示
    print(f'Line Clone Rate: {Analyzer.calculate_line_clone_rate(engine_name)}')
    print(f'File Clone Rate: {Analyzer.calculate_file_clone_rate(engine_name)}')

def format():
    CreateFolderFormat.create_folder(sys.argv[1])
    CreateFolderFormat.create_file(sys.argv[1])

analyze()