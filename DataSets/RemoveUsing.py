import os
import sys

sys.path.append(os.path.abspath('../'))
from Common import FileManager as FileManager

USING = 'using'

def remove_using_in_file(source_file):
    ''' ファイル内のusingを削除する '''

    contents = FileManager.read_file(source_file)
    remove_using_contents = _remove_using(contents)

    FileManager.write_file(source_file, remove_using_contents)

def _remove_using(contents):
    ''' ファイルないのusingを削除する

    contents: ファイルの全行のリスト'''

    return [line for line in contents if USING not in line.strip()]