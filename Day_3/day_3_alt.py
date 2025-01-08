import subprocess
import sys
import os
import re

def help_page():
    print("\nPROGRAM USAGE:\n"
        "NAME\n"
        "\tday_3.py - solving corrupted input in order to get multiplication result\n"
        "SYNOPSIS\n"
        "\tday_3.py + -p + [INPUT FILE PATH]\n")

def is_txt(alt_path=None):
    if alt_path is None:
        path_tuple = os.path.splitext(sys.argv[1])
        return path_tuple[1].lower() == "txt" or path_tuple[1] == ""
    else:
        alt_path = os.path.splitext(alt_path)
        return alt_path[1].lower() == "txt" or alt_path[1] == ""
    
def is_accessible(alt_path=None):
    if alt_path is None:
        path = sys.argv[1]
    else:
        path = alt_path

    try:
        open(path, 'r').close()
        return True
    except FileNotFoundError:
        return False

def try_bash():
    command = ["bash", "-c", "readlink -f input"]
    result = subprocess.run(command, text=True, capture_output=True)

    if result.returncode == 0:
        path = result.stdout.strip()
        if is_txt(alt_path=path) and is_accessible(alt_path=path):
            return path
    
    return None

def cli():
    if len(sys.argv) != 2:
        print("** Improper usage of the command! **")
        help_page()
    else:
        if is_txt():
            if is_accessible():
                return sys.argv[1]
            else:
                help_page()
                print("** specified file can not be opened! **")
        else:
            help_page()
            print("** File needs to be a \"txt\" file! **")

    return None

def search_line(line):
    mult_regex = r"mul\((\d{1,3}),(\d{1,3})\)"
    dont_regex = r"don't\(\)"
    do_regex = r"do\(\)"
    result, idx, do = 0, 0, 1
    switch = 0
    
    while idx < len(line):
        mult_match = re.search(mult_regex, line[idx:])
        dont_match = re.search(dont_regex, line[idx:])
        do_match = re.search(do_regex, line[idx:])

        matches = [mult_match, dont_match, do_match]
        if not any(matches):
            break
        indexes = [i.end() if i else float('inf') for i in matches]
        switch = indexes.index(min(indexes))

        if switch == 0 and do:
            result += int(mult_match.group(1)) * int(mult_match.group(2))
        elif switch == 1:
            do = 0
        elif switch == 2:
            do = 1
        idx += min(indexes)

    return result

def read_input(path):
    results = []

    file = open(path, 'r')
    line = file.readline()

    while line:
        results.append(search_line(line))
        line = file.readline()

    return sum(results)

def main():
    
    if len(sys.argv) > 1:
        path = cli()
    else:
        path = try_bash()

    if path is None:
        print("**Could not find the \"input\" file")
        return
    
    print("Result is: ", read_input(path))

main()