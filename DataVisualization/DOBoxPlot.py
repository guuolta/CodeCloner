import os
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

BOX_PLOT_PATH = os.path.expanduser("~/Documents/CCFinderSW-1.0/GameMaker/BoxPlots")

DB_FOLDER_PATH = os.path.expanduser("~/Documents/CCFinderSW-1.0/GameMaker/DBs")
CLONE_RATE_DB_FOLDER_NAME = '0_CloneRate'
ANALYZE_DB_NAME = 'Analyze.db'
CLONE_RATE_DB_NAME = 'CloneRate.db'

def main():
    datasets = []
    labels = []
    
    # 各フォルダのクローン率データを取得
    for folder in os.listdir(DB_FOLDER_PATH):
        if folder != CLONE_RATE_DB_FOLDER_NAME:
            folder_path = os.path.join(DB_FOLDER_PATH, folder)
            if os.path.isdir(folder_path):
                db_path = os.path.join(folder_path, ANALYZE_DB_NAME)
                dataset = get_datasets(db_path)
                
                if dataset:
                    datasets.append(dataset)
                    labels.append(folder)  # フォルダ名をラベルとして保存
    
    clone_rate_path = os.path.join(DB_FOLDER_PATH, CLONE_RATE_DB_FOLDER_NAME, CLONE_RATE_DB_NAME)
    file_clone_rate, line_clone_rate = get_clone_rate_data(clone_rate_path)

    create_combined_box_plot(datasets, labels)
    create_box_plot(file_clone_rate, line_clone_rate)

def get_datasets(db_path):
    analyze_conn = sqlite3.connect(db_path)
    analyze_cur = analyze_conn.cursor()
    
    # データを取得してリスト形式に変換
    datas = analyze_cur.execute('SELECT cloneRate FROM analyze_results').fetchall()
    return [data[0] for data in datas]  # cloneRateの値のみ抽出

def create_combined_box_plot(datasets, labels):
    plt.figure(figsize=(10, 6))  # プロットのサイズ設定
    plt.title('Box plot of CloneRate for All Folders')
    plt.grid()
    
    # 箱ひげ図の描画
    plt.boxplot(datasets, labels=labels)
    plt.xticks(rotation=90)  # ラベルが見やすいように回転
    plt.ylabel('Clone Rate')

    plt.tight_layout()  # レイアウト調整
    save_box_plot('CloneRate', plt)

def get_clone_rate_data(db_path):
    clone_rate_conn = sqlite3.connect(db_path)
    clone_rate_cur = clone_rate_conn.cursor()
    clone_rate_cur.execute('SELECT fileCloneRate, lineCloneRate FROM clone_rate')
    clone_rate_data = clone_rate_cur.fetchall()
    
    file_clone_rate = []
    line_clone_rate = []

    for data in clone_rate_data:
        file_clone_rate.append(data[0])
        line_clone_rate.append(data[1])

    return file_clone_rate, line_clone_rate

def create_box_plot(file_clone_rate, line_clone_rate):
    plt.figure(figsize=(10, 6))
    plt.title('Box plot of Clone Rate')
    plt.grid()

    plt.boxplot([line_clone_rate], labels=['Line Clone Rate'])
    plt.ylabel('Clone Rate')

    plt.tight_layout()
    save_box_plot('AllCloneRate', plt)

def save_box_plot(project_name, plt):
    print(f"Saving box plot for {project_name}")
    save_path = os.path.join(BOX_PLOT_PATH, project_name+"_box_plot.png")
    plt.savefig(save_path, format='png')
    plt.close()

main()
