import os

# 設定
URL_FILE_PATH = '/Users/ogurayuuki/Documents/CCFinderSW-1.0/Datasets/DatasetUrls.txt'  # URLが書かれたテキストファイルのパス
DATASET_FOLDER_PATH = os.path.expanduser('~/Documents/CCFinderSW-1.0/Datasets')  # データセットフォルダのパス

def main():
    # URLをテキストファイルから読み込み
    urls = read_urls(URL_FILE_PATH)
    
    # データセットフォルダ内のプロジェクト名を取得
    existing_projects = get_existing_projects(DATASET_FOLDER_PATH)
    
    # クローンできていないプロジェクトを特定
    not_cloned_projects = find_not_cloned_projects(urls, existing_projects)
    
    # 結果を表示
    print("クローンできていないプロジェクト:")
    for project in not_cloned_projects:
        print(project)

def read_urls(file_path):
    """テキストファイルからURLを読み込む。"""
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except Exception as e:
        print(f"Error reading URL file: {e}")
        return []

def get_existing_projects(folder_path):
    """データセットフォルダ内のプロジェクト名を取得する。"""
    return [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]

def find_not_cloned_projects(urls, existing_projects):
    """クローンできていないプロジェクトを特定する。"""
    not_cloned = []
    for url in urls:
        # URLからプロジェクト名を抽出するロジックを実装
        project_name = extract_project_name_from_url(url)
        if project_name and project_name not in existing_projects:
            not_cloned.append(project_name)
    return not_cloned

def extract_project_name_from_url(url):
    """URLからプロジェクト名を抽出する（仮の実装）。"""
    # ここでは単純な例を示します。実際には URL の形式に応じて実装を調整する必要があります。
    # 例: 'https://github.com/user/repo.git' から 'repo' を抽出する
    parts = url.split('/')
    if len(parts) > 2:
        return parts[-1].replace('.git', '')  # .git を取り除く
    return None

if __name__ == "__main__":
    main()