import sys
import os

def help_page():
    print("\nPROGRAM USAGE:\n"
          "NAME\n"
          "\tday_2.py - Reindeeer nuclear powerplant puzzle solution\n"
          "SYNOPSIS\n"
          "\tday_2.py + [INPUT FILE PATH] + [TOLERANCE]\n"
          "\n\ttolerance - number of not safe values to be tolerated\n")

def is_txt():
    path_tuple = os.path.splitext(sys.argv[1])
    return path_tuple[1].lower() == "txt" or path_tuple[1] == ""

def cli():
    if not 1 < len(sys.argv) < 4:
        print("** Improper usage of program! **")
        help_page()
        exit()
    else:
        if is_txt():
            try:
                open(sys.argv[1], 'r').close()
                tolerance = int(sys.argv[2])
            except FileExistsError:
                print("** Specified path is not correct! **")
                help_page()
                exit()
            except ValueError:
                print("** Tolerance needs to be an integer! **")
                help_page()
                exit()
        else:
            print("** Specified file is not a \"txt\" file! **")
            help_page()
            exit()
    
    return sys.argv[1], tolerance

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

def determine_bias(ok_signs):
    # determines bias of the number list
    # and makes a list of correct signs
    if sum(ok_signs) > 0:
        ascending = 1
    else:
        ascending = 0

    return ascending

def sign_condition(num_list):
    signs = []

    for i in range(1, len(num_list)):
        diff = num_list[i] - num_list[i - 1]

        if diff > 0:
            signs.append(1)
        elif diff < 0:
            signs.append(-1)
        else:
            signs.append(0)

    return determine_bias(signs)

def is_safe(num_list, tolerance, tolerated, ascending):
    end = len(num_list) - 1
    start = 1

    if tolerated > tolerance:
        return False

    for i in range(start, end):
        diff = num_list[i] - num_list[i - 1]
        nxt_diff = num_list[i + 1] - num_list[i]
        num = num_list[i]

        if ascending:
            if 0 < diff < 4 and 0 < nxt_diff < 4:
                continue
            elif not 0 < diff < 4 and not 0 < nxt_diff < 4:
                num_list.pop(i)
            elif 0 < diff < 4 and not 0 < nxt_diff < 4:
                if i < (end - 1) and num_list[i + 2] == num_list[i]:
                       num_list.pop(i)
                else:
                    num_list.pop(i + 1)
            else:
                num_list.pop(i - 1)
        else:
            if -4 < diff < 0 and -4 < nxt_diff < 0:
                continue
            elif not -4 < diff < 0 and not -4 < nxt_diff < 0:
                num_list.pop(i)
            elif -4 < diff < 0 and not (-4 < nxt_diff < 0):
                if i < (end - 1) and num_list[i + 2] == num_list[i]:
                    num_list.pop(i)
                else:
                    num_list.pop(i + 1)
            else:
                num_list.pop(i - 1)

        return is_safe(num_list, tolerance, tolerated + 1, ascending)
    
    return True

def read_input(path, tolerance):
    file = open(path, 'r')
    safe_cnt = 0

    line = file.readline()
    while line:
        num_list = parse_str(line)
        ascending = sign_condition(num_list)

        if is_safe(num_list.copy(), tolerance, 0, ascending):
            safe_cnt += 1
        line = file.readline()
    
    file.close()
    
    return safe_cnt

def main():
    path, tolerance = cli()
    print("Num of safe reports:", read_input(path, tolerance))

main()
