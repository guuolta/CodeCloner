# CCFinderSWの解析自動化ツール
このツールは、「ギットクローン -> プログラムファイル抽出・整形 -> CCFinderSWで解析 -> 解析結果をデータベースに格納 -> 箱ひげ図で可視化」という一連の流れを自動化したツールです。  
一応、拡張しやすいような設計にしているので、自由に機能拡張・修正してください。

## 目次
- [CCFinderSWの解析自動化ツール](#ccfinderswの解析自動化ツール)
  - [目次](#目次)
  - [使用ツール](#使用ツール)
  - [セットアップ](#セットアップ)
    - [要件](#要件)
    - [パスの設定](#パスの設定)
  - [使い方](#使い方)
    - [解析対象グループのフォルダを作成](#解析対象グループのフォルダを作成)
      - [実行例](#実行例)
    - [データセットのURLを記述](#データセットのurlを記述)
      - [記述例](#記述例)
    - [解析する](#解析する)
      - [実行例](#実行例-1)
  - [解析結果のフォルダ構成](#解析結果のフォルダ構成)
    - [BoxPlots](#boxplots)
    - [DBs](#dbs)
    - [Outputs](#outputs)
    - [Programs](#programs)
    - [Repositories](#repositories)
    - [datasets.txt](#datasetstxt)
  - [クローン率の計算法](#クローン率の計算法)
    - [行クローン率](#行クローン率)
    - [ファイルクローン率](#ファイルクローン率)
  - [実行ファイルのフォルダ構成](#実行ファイルのフォルダ構成)
  - [データベース](#データベース)
    - [Source](#source)
      - [テーブル名](#テーブル名)
      - [カラム](#カラム)
    - [CloneSet](#cloneset)
      - [テーブル名](#テーブル名-1)
      - [カラム](#カラム-1)
    - [Result](#result)
      - [テーブル名](#テーブル名-2)
      - [カラム](#カラム-2)
    - [CloneRate](#clonerate)
      - [テーブル名](#テーブル名-3)
      - [カラム](#カラム-3)

## 使用ツール
- [CCFinderSW](https://github.com/YuichiSemura/CCFinderSW)
- [grammars-v4](https://github.com/antlr/grammars-v4/tree/master)
- [Python](https://www.python.org/)

## セットアップ
### 要件
本ツールは以下の環境で制作しています。
- Python : 3.13.0

また、以下のPythonライブラリーを使用しています。
```
Package         Version
--------------- -----------
chardet         5.2.0
contourpy       1.3.1
cycler          0.12.1
fonttools       4.56.0
kiwisolver      1.4.8
matplotlib      3.10.0
numpy           2.2.3
packaging       24.2
pillow          11.1.0
pip             24.2
pyparsing       3.2.1
python-dateutil 2.9.0.post0
six             1.17.0
```

### パスの設定
「**Common/PathManager.py**」の```CCFINDERSW_PATH```の値を解析結果を保存したいフォルダのパスに設定してください。  
また、「**CCFinderSW/CCFinderSWData.py**」の```CCFINDERSW_JAVA_PATH```の値をCCFinderの実行ファイルの「**CCFinderSW-1.0/lib/CCFinderSW-1.0.jar**」につながるパスに設定してください。

## 使い方
### 解析対象グループのフォルダを作成
以下のコマンドを実行することで、**解析対象グループの結果を保管するフォルダ**と**データセットのURLを記述するテキストファイル**が生成されます。  
```python3 Initializer.py 解析対象グループ名```  
#### 実行例
```python3 Initializer.py Unity```というコマンドを実行すると、以下のようなフォルダとファイルが生成されます。  
```
Unity
└── datasets.txt
```

### データセットのURLを記述
先ほどのコマンドで生成した、```datasets.txt```にGitのリポジトリのURLを記述します。  
記述するURLは、```https://github.com/リポジトリ名.git```の形にしてください。  
また、URLは改行区切りにしてください。(空行は無視されます)

#### 記述例
```
https://github.com/guuolta/CodeCloner.git
https://github.com/hogehoge/hugahuga.git
・
・
・
```

### 解析する
以下のコマンドを実行することで、クローンから箱ひげ図化までの一連の流れを実行します。  
```python3 Action.py 解析対象グループ名 プログラミング言語 拡張子1 拡張子2 ・・・```  
- ```解析対象グループ名```  
    [はじめに生成した解析対象グループ名](#解析対象グループのフォルダを作成)と合わせてください。  
- ```プログラミング言語```  
    解析するプログラミング言語を指定してください。  
    このプログラミング言語名は、CCFinderSWの「**grammarsv4**」フォルダ内の「プログラミング言語のフォルダ名」にしてください。  
    (例：C# -> csharp, python -> python3)  
- ```拡張子```  
    調べるソースファイルの拡張子を **「.」なし** で指定してください。  
    拡張子は、何個でも指定できます。

#### 実行例
```
python3 Action.py Unity csharp cs
```
```
python3 Action.py Unreal cpp cpp h
```

## 解析結果のフォルダ構成
```
.
├── BoxPlots
│   ├── AllProjectLineCloneRate.png
│   └── TotalProjectCloneRate.png
├── DBs
│   ├── 0_CloneRate
│   │   └── CloneRate.db
│   └── プロジェクト名
│       ├── CloneSet.db
│       ├── Result.db
│       └── SourceFile.db
├── Outputs
│   └──プロジェクト名_output_ccfsw.txt
├── Programs
├── Repositories
└── datasets.txt
```
### BoxPlots
箱ひげ図を保管する
- #### AllProjectLineCloneRate
    プロジェクトごとに行クローン率の箱ひげ図
- #### TotalProjectCloneRate
    全プロジェクトの行クローン率とファイルクローン率の箱ひげ図

### DBs
プロジェクトごとにデータベースを保管する
- #### 0_CloneRate/CloneRate.db
    [全プロジェクトの情報をもつデータベース](#clonerate-1)
- #### CloneSet.db
    [CCFinderSWの結果のクローンセット部分をもつデータベース](#cloneset-2)
- #### Result
    [ファイルごとの情報をもつデータベース](#result-2)
- #### Source
    [CCFinderSWの結果のソースファイル部分をもつデータベース](#source-2)

### Outputs
CCFinderの解析結果のテキストファイルを保管する

### Programs
データセットのソースファイルだけを抽出したものをプロジェクトごとに保管する

### Repositories
GitHubのリポジトリを保管する

### datasets.txt
GitHubのURLが記載されたテキストファイル

## クローン率の計算法
### 行クローン率
$$ 行クローン率 = \frac{クローンになっている行数}{全行数} $$

### ファイルクローン率
$$ ファイルクローン率 = \frac{クローンになっているファイル数}{全ファイル数} $$

## 実行ファイルのフォルダ構成
```
.
├── Action.py
├── Analyzer
│   ├── Analyzer.py
│   ├── CloneRate
│   │   ├── CloneRateDB.py
│   │   └── CloneRateData.py
│   ├── CloneSet
│   │   ├── CloneSetDB.py
│   │   └── CloneSetData.py
│   ├── Result
│   │   ├── ResultDB.py
│   │   └── ResultData.py
│   └── Source
│       ├── SourceFileDB.py
│       └── SourceFileData.py
├── CCFinderSW
│   ├── CCFinderSWData.py
│   └── CCFinderSWHandler.py
├── Common
│   ├── Calculater.py
│   ├── ChangeEnv.sh
│   ├── FileManager.py
│   └── PathManager.py
├── DataBase
│   ├── DAO.py
│   └── DBData.py
├── DataSets
│   ├── DataSetsData.py
│   ├── ProgramExtract.py
│   └── RemoveUsing.py
├── Formater
│   └── CreateFolderFormat.py
├── Git
│   ├── CheckGitClone.py
│   ├── GitData.py
│   └── GitHandler.py
├── Initializer.py
└── Visualization
    ├── BoxPlot
    │   ├── BoxPlotData.py
    │   └── BoxPloter.py
    └── CommonVisualization.py
```
- ### 実行ファイル
    - #### Initializer.py
        ツール実行のための準備をする
    - #### Action.py
        ツールの実行をする

- ### Common
    全体に関連するファイルが格納されている
    - #### PathManager.py
        パス関連の操作や結果を保管するフォルダのパスの情報を持つ
    - #### FileManager.py
        ファイルの読み書きのような操作を行う
    - #### Calculater.py
        クローン率のような計算をする

- ### Formater
    フォルダの整形をする
    - #### CreateFolderFormat.py
        ツール実行のために必要なフォルダやファイルを作る

- ### Git
    Gitの操作に関連するファイルが保管されている
    - #### GitData.py
        Git操作に関連するパスやコマンドの情報を持つ
    - #### GitHandler.py
        Gitのコマンドの実行をする

- ### DataSets
    ソースファイルの抽出・整形に関するファイルが保管されている
    - #### DataSetsData.py
        ソースファイル抽出のための操作に関連するパスの情報を持つ
    - #### ProgramExtract.py
        クローンしたリポジトリから、ソースファイルを抽出・整形する
    - #### RemoveUsing.py
        ソースファイルからusingから始まる行を除く  
        C#のソースファイルでの使用を想定している

- ### CCFinderSW
    CCFinderSWに関するファイルが保管されている
    - #### CCFinderSWData.py
        CCFinderSW解析のための操作に関連するパスやコマンドの情報を持つ
    - #### CCFinderSWHandler.py
        CCFinderSWで解析する

- ### DataBase
    データベースに関するファイルが保管されている
    - #### DBData.py
        データベースに関するパスの情報を持つ
    - #### DAO.py
        データベースに実行するコマンドを持つ

- ### Analyzer
    データベースに格納したり、データベースから情報を取り出す
    - #### Analyzer.py
        データベースに格納したり、データベースから情報を取り出す
    - ### Source
        CCFinderSWの結果のソースファイル部分をデータベースに格納する
    - ### CloneSet
        CCFinderSWの結果のクローンセット部分をデータベースに格納する
    - ### Result
        CCFinderSWの結果からファイルごとの情報をデータベースに格納する
    - ### CloneRate
        CCFinderSWの結果からプロジェクトごとの情報をデータベースに格納する

- ### Visualization
    データベースの情報を可視化する
    - #### CommonVisualization.py
        可視化に必要な情報を持つ
    - ### BoxPlot
        箱ひげ図化する

## データベース
### Source
CCFinderSWの結果のソースファイル部分をもつデータベース
#### テーブル名
SourceFile
#### カラム
- id: ID(先頭から0,1,2・・・)
- name: ファイル名
- line_count: 行数
- token_count: トークン数
- path: ファイルのパス

### CloneSet
CCFinderSWの結果のクローンセット部分をもつデータベース
#### テーブル名
CloneSet
#### カラム
- id: ID(先頭から0,1,2・・・)
- clone_id: クローンセットID
- file_id: ソースファイルに対応するファイルID
- start_line: クローンになっている開始行
- start_token: クローンになっている開始番号
- end_line: クローンになっている最終行
- end_token: クローンになっている最終番号

### Result
ファイルごとの情報をもつデータベース
#### テーブル名
Result
#### カラム
- id: ID(先頭から0,1,2・・・)
- file_name: ファイル名
- clone_lines: クローンになっている行番号
- clone_line_count: ファイル内のクローンになっている行数
- line_count: ファイル内の行数
- clone_rate: ファイルの行クローン率

### CloneRate
全プロジェクトの情報をもつデータベース
#### テーブル名
CloneRate
#### カラム
- id: ID(先頭から0,1,2・・・)
- project_name: プロジェクト名
- file_count: プロジェクト内のファイル数
- file_clone_count: プロジェクト内のクローンを含むファイル数
- file_clone_rate: プロジェクト内のファイルクローン率
- line_count: プロジェクト内の行数
- line_clone_count: プロジェクト内のクローンになっている行数
- line_clone_rate: プロジェクト内の行クローン率