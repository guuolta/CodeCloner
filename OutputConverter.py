import os

OUTPUT_FILE_PATH = '/Users/ogurayuuki/Documents/CCFinderSW-1.0/lib/outputtxt_ccfsw.txt'

START_SUORCE_FILES = "#source_files"
START_CLONE_SETS = "#clone_sets"

SOURCEFILE_DATASET_COUNT = 4
ID_INDEX = 0
FILE_PATH_INDEX = 3

CLONE_SPLIT_SYMBOL = ":"

def main():
    source_files_dict = output_to_dictionary(OUTPUT_FILE_PATH)
    update_clone_sets(OUTPUT_FILE_PATH, source_files_dict)

def output_to_dictionary(file_path):
    source_dict = {}

    contents = read_file(file_path)

    source_files_started = False

    for line in contents:
        if line.startswith(START_CLONE_SETS):
            break

        if not source_files_started and line.startswith(START_SUORCE_FILES):
            source_files_started = True
            continue

        if not source_files_started:
            continue

        parts = line.split()
        if len(parts) >= SOURCEFILE_DATASET_COUNT:
            index = parts[ID_INDEX]
            file_path = parts[FILE_PATH_INDEX]
            file_name = os.path.basename(file_path)

            source_dict[index] = file_name

    return source_dict

def update_clone_sets(file_path, source_dict):
    updated_lines = []

    contents = read_file(file_path)

    clone_sets_started = False

    for line in contents:
        if not clone_sets_started and line.startswith(START_CLONE_SETS):
            clone_sets_started = True
            updated_lines.append(line)
            continue

        if not clone_sets_started:
            updated_lines.append(line)
            continue

        parts = line.split(CLONE_SPLIT_SYMBOL)
        if len(parts) > 1:
            key = parts[0].strip()
            if key in source_dict:
                updated_lines.append(source_dict[key] + CLONE_SPLIT_SYMBOL + parts[1])
            else:
                updated_lines.append("\n")
                updated_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(updated_lines)

def read_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        return f.readlines()

main()