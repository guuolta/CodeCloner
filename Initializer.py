''' ツールを使うための初期設定 '''

import sys
from Formater import CreateFolderFormat as CreateFolderFormat

def Initialize(engine_name):
    ''' ツールを使うための初期設定 '''

    CreateFolderFormat.create_folder(engine_name)
    CreateFolderFormat.create_file(engine_name)

Initialize(sys.argv[1])