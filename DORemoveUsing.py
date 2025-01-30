import os
import shutil
import subprocess
import sys
from RemoveUsing import main as remove_using

DATASET_PATH = os.path.expanduser('~/Documents/CCFinderSW-1.0/Datasets')
PYTHON_FILES_PATH = os.path.expanduser('~/Documents/CCFinderSW-1.0/python')
REMOVE_USING_PROJECT_PATH = os.path.expanduser('~/Documents/CCFinderSW-1.0/RemoveUsingFiles')

def main():
    for dataset in os.listdir(DATASET_PATH):
        print(dataset)
        dataset_path = os.path.join(DATASET_PATH, dataset)
        pyhon_path = os.path.join(PYTHON_FILES_PATH,'RemoveUsing.py')

        if os.path.isdir(dataset_path):
            remove_using(dataset_path)


main()
#remove_using(sys.argv[1])