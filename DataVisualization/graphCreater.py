import os
import sqlite3
import matplotlib.pyplot as plt

SAVE_GRAPH_PATH ='/Users/ogurayuuki/Documents/CCFinderSW-1.0/Graphs'

def main(db_path, folder):
    analyze_conn = sqlite3.connect(db_path)
    analyze_cur = analyze_conn.cursor()

    analyze_cur.execute('SELECT fileName, cloneRate FROM analyze_results')
    results = analyze_cur.fetchall()

    file_names = [result[0] for result in results]
    clone_rates = [result[1] for result in results]

    plot_clone_rate(folder, file_names, clone_rates)

def plot_clone_rate(project_name, file_names, clone_rates):
    plt.figure(figsize=(12, 8), constrained_layout=True)
    plt.bar(file_names, clone_rates, color='skyblue')

    plt.xlabel('File Name')
    plt.ylabel('Clone Rate')
    plt.title('Clone Rate per File')

    plt.xticks(rotation=90)

    plt.tight_layout()
    save_graph(project_name, plt)
    plt.close()

def save_graph(project_name, plt):
    print(f"Saving graph for {project_name}")
    save_path = os.path.join(SAVE_GRAPH_PATH, project_name+"_graph.png")
    plt.savefig(save_path, format='png')