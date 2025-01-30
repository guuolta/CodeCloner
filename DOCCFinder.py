import os
import subprocess

REMOVE_USING_PROJECT_PATH = os.path.expanduser("~/Documents/CCFinderSW-1.0/GameMaker/CppFiles")
SCRIPT_PATH = os.path.expanduser("~/Documents/CCFinderSW-1.0/GameMaker/Command/CCFinderSW.sh")

def main():
    for dataset in os.listdir(REMOVE_USING_PROJECT_PATH):
        print(dataset)
        subprocess.run([SCRIPT_PATH, dataset], cwd=os.path.dirname(SCRIPT_PATH))

main()