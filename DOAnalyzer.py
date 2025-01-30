
import os
import subprocess

PYTHON_ANALYZER_PATH = os.path.expanduser("~/Documents/CCFinderSW-1.0/Python/Analyzer")
OUTPUT_PATH = os.path.expanduser("~/Documents/CCFinderSW-1.0/GameMaker/Outputs")

def main():
    for output in os.listdir(OUTPUT_PATH):
        if output.endswith('.txt'):
            run_analyzer(os.path.join(OUTPUT_PATH, output))

def run_analyzer(path):
    subprocess.run(['python3', os.path.join(PYTHON_ANALYZER_PATH, 'Analyzer.py'), path])

main()