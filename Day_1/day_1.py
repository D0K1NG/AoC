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
    path = "/home/teo/Documents/VS_py_projekti/AoC/Day_1/input"

    list1, list2 = get_input(path)
    tot_distance = calc_distance(list1, list2)

    print(f"Total distance is: {tot_distance}")

main()