# CCFinderSWの解析自動化ツール
このツールは、「ギットクローン -> プログラムファイル抽出・整形 -> CCFinderSWで解析 -> 解析結果をデータベースに格納 -> 箱ひげ図で可視化」という一連の流れを自動化したツールです。  
一応、拡張しやすいような設計にしているので、自由に機能拡張・修正してください。

## 目次
- [セットアップ](#セットアップ)
  - [要件](#要件)
  - [パスの設定](#パスの設定)
- [使い方](#使い方)
  - [解析対象グループのフォルダを作成](#解析対象グループのフォルダを作成)
  - [データセットのURLを記述](#データセットのURLを記述)
  - [解析する](#解析する)
- [フォルダ構成](#フォルダ構成)
  - [実行ファイル](#実行ファイル)
    - [Initializer.py](#initializerpy)
    - [Action.py](#actionpy)
  - [Common](#common)
    - [PathManager.py](#pathmanagerpy)
    - [FileManager.py](#filemanagerpy)
    - [Calculater.py](#calculaterpy)
  - [Formater](#formater)
    - [CreateFolderFormat.py](#createfolderformatpy)
  - [Git](#git)
    - [GitData.py](#gitdatapy)
    - [GitHandler.py](#githandlerpy)
  - [DataSets](#datasets)
    - [DataSetsData.py](#datasetsdatapy)
    - [ProgramExtract.py](#programextractpy)
    - [RemoveUsing.py](#removeusingpy)
  - [CCFinderSW](#ccfindersw)
    - [CCFinderSWData.py](#ccfinderswdatapy)
    - [CCFinderSWHandler.py](#ccfinderswhandlerpy)
  - [DataBase](#database)
    - [DBData.py](#dbdatapy)
    - [DAO.py](#daopy)
  - [Analyzer](#analyzer)
    - [Analyzer.py](#analyzerpy)
    - [Source](#source)
    - [CloneSet](#cloneset)
    - [Result](#result)
    - [CloneRate](#clonerate)
  - [Visualization](#visualization)
    - [CommonVisualization.py](#commonvisualizationpy)
    - [BoxPlot](#boxplot)

## セットアップ
### 要件
本ツールは以下の環境で制作しています。
- Python : 3.13.0

また、以下のPythonライブラリーを使用しています。
- chardet : 5.2.0
- contourpy : 1.3.1
- cycler : 0.12.1
- fonttools : 4.56.0
- kiwisolver : 1.4.8
- matplotlib : 3.10.0
- numpy : 2.2.3
- packaging : 24.2
- pillow : 11.1.0
- pip : 24.2
- pyparsing : 3.2.1
- python-dateutil : 2.9.0.post0
- six : 1.17.0

### パスの設定
「**Common/PathManager.py**」の```CCFINDERSW_PATH```の値を解析結果を保存したいフォルダのパスに設定してください。  
また、「**CCFinderSW/CCFinderSWData.py**」の```CCFINDERSW_JAVA_PATH```の値をCCFinderの実行ファイルの「**CCFinderSW-1.0/lib/CCFinderSW-1.0.jar**」につながるパスに設定してください。

## 使い方
### 解析対象グループのフォルダを作成
以下のコマンドを実行することで、**解析対象グループの結果を保管するフォルダ**と**データセットのURLを記述するテキストファイル**が生成されます。  
```python3 Initializer.py 解析対象グループ名```  
#### 実行例
```python3 Initializer.py Unity```というコマンドを実行すると、以下のようなフォルダとファイルが生成される。  
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

## フォルダ構成
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