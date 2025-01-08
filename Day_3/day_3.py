import subprocess
import sys
import os

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

def get_num(idx, line, digits):
    num, i = "", 0

    while line[idx].isdigit() and i < digits and idx < len(line):
        if line[idx] == ",":
            break
        num += line[idx]
        idx += 1
        i += 1

    if num:
        try:
            num = int(num)
            return num, idx
        except ValueError:
            return None, i
            
    else:
        return None, i

def parse_line(line):
    do, i, end = 1, 0, len(line)
    max_digit = 3
    results = []

    while i < end:
        num1, num2 = 0, 0

        if do and (i + 4) < end and line[i:i+4] == "mul(":
            i += 4

            num1, i = get_num(i, line, max_digit)
            if num1 is not None:
                if i < end and line[i] == ",":
                    i += 1
                    # while i < end and line[i].isspace():
                    #     i += 1
                    num2, i = get_num(i, line, max_digit)
                    print(f"{num2}")
                    if num2 is not None:
                        if i < end and line[i] == ")":
                            print(f"{num1} * {num2}")
                            results.append(num1 * num2)

        elif (i + 6) < end and line[i:i+7] == "don't()":
            i += 6
            do = 0
        elif (i + 3) < end and line[i:i+4] == "do()":
            i += 3
            do = 1

        i += 1
    
    return sum(results)

def read_input(path):
    file = open(path, 'r')
    results = []

    line = file.readline()
    while line:
        results.append(parse_line(line))
        line = file.readline()

    file.close()
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

