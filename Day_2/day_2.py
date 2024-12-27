import sys
import os

def help_page():
    print("\nPROGRAM USAGE:\n"
          "NAME"
          "\tday_2.py - Reindeeer nuclear powerplant puzzle solution"
          "SYNOPSIS"
          "\tday_2.py + [INPUT FILE PATH]")

def is_txt():
    path_tuple = os.path.splitext(sys.argv[1])
    return path_tuple[1].lower() == "txt" or path_tuple[1] == ""

def cli():
    if not 1 < len(sys.argv) < 3:
        print("** Improper usage of program! **")
        help_page()
        exit()
    else:
        if is_txt():
            try:
                open(sys.argv[1], 'r').close()
            except FileExistsError:
                print("** Specified path is not correct! **")
                help_page()
                exit()
        else:
            print("** Specified file is not a \"txt\" file! **")
            help_page()
            exit()
    
    return sys.argv[1]

def parse_str(str):
    num_list, num_str = [], []
    last, i = len(str) - 1, 0

    while i <= last:
        if str[i] in (" ", "\n", "\t"):
            if str[i - 1] == " ":
                i += 1
                continue
            num_list.append(int("".join(num_str)))
            num_str.clear()
        else:
            num_str.append(str[i])
            if i == last:
                num_list.append(int("".join(num_str)))
                num_str.clear()
        i += 1
    
    return num_list

def is_safe(num_list):
    prev_diff = num_list[1] - num_list[0]
    safe = 0

    for i in range(1, len(num_list)):
        curr_diff = num_list[i] - num_list[i - 1]

        if abs(curr_diff) < 4:
            if curr_diff < 0 and prev_diff < 0:
                safe = 1
            elif curr_diff > 0 and prev_diff > 0:
                safe = 1
            else:
                return 0
        else:
            return 0

        prev_diff = curr_diff

    return safe

def parse_input(path):
    file = open(path, 'r')
    safe_cnt = 0

    line = file.readline()
    while line:
        if is_safe(parse_str(line)):
            safe_cnt += 1
        line = file.readline()
    
    return safe_cnt

def main():
    path = cli()
    print("Num of safe reports:", parse_input(path))

main()  