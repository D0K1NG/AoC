import sys
import os

def help_page():
    print("\nPROGRAM USAGE:\n"
          "NAME\n"
          "\tday_1.py - first task of AoC (find similarity and total distance)\n"
          "SYNOPSIS\n"
          "\tday_1.py [FILE PATH TO \".txt\" FILE]\n")

def is_txt(path):
    path_tuple = os.path.splitext(path)
    return path_tuple[1].lower() == "txt" or path_tuple[1] == ""

def cli():
    if len(sys.argv) > 2 or len(sys.argv) < 2:
        print("** Incorect number of arguments! **")
        help_page()
        exit()
    else:
        if is_txt(sys.argv[1]):
            try:
                open(sys.argv[1], 'r').close()
            except FileNotFoundError:
                print("** Specified file path is not correct! **")
                help_page()
                exit()
        else:
            print("** Specified file is not a \"txt\" file! **")
            help_page()
            exit()

    return sys.argv[1]

def get_IDs(line):
    space_seen = 0
    num1, num2 = [], []
    for char in line:
        if char == " ":
            space_seen = 1
        elif not space_seen:
            num1.append(char)
        else:
            num2.append(char)
    try:
        num1 = int("".join(num1))
        num2 = int("".join(num2))
    except ValueError:
        print("** Input can not be converted to integer values! **")
    return num1, num2

def get_input(path):
    left_list, right_list = [], []
    input = open(path, 'r')

    line = input.readline()
    while line:
        num1, num2 = get_IDs(line)
        left_list.append(num1)
        right_list.append(num2)
        line = input.readline()
    
    return left_list, right_list

def calc_similarity(left_list, right_list):
    tot_similarity, cnt, i = 0, 0, 0

    for num in left_list:
        cnt, i = 0, 0
        while i < len(right_list):
            if right_list[i] == num:
                cnt += 1
                right_list.pop(i)
            else:
                i += 1
        tot_similarity += cnt * num

    return tot_similarity


def find_minimum(list):
    minimum = list[0]
    idx = 0
    
    for i in range(0, len(list)):
        if list[i] < minimum:
            minimum = list[i]
            idx = i

    list.pop(idx)
    return minimum


def calc_distance(left_list, right_list):
    total_distance = 0

    if len(left_list) != len(right_list):
        print("** Length of lists is not the same! **")
        exit()

    while left_list:
        minl = find_minimum(left_list)
        minr = find_minimum(right_list)

        total_distance += abs(minl - minr)
    
    return total_distance    

def main():
    path = cli()
    left_list, right_list= get_input(path)
    tot_distance = calc_distance(left_list.copy(), right_list.copy())
    tot_similarity = calc_similarity(left_list.copy(), right_list.copy())

    print(f"Total distance is: {tot_distance}\n"
          f"Total similarity is: {tot_similarity}")

main()  
