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

def get_vertical_lines(lines):
    vert_lines, vert_line = [], []

    for cols in range(0, len(lines[0])):
        for rows in range(0 ,len(lines)):
            vert_line.append(lines[rows][cols])
        vert_lines.append("".join(vert_line))
        vert_line = []

    return vert_lines

def get_left_diag_lines(lines):
    rows, cols = len(lines), len(lines[0])
    diag_line, diag_lines = [], []
    i, row, col = 0, 0, 0
    limit = cols - 1 - (rows - 1)

    # Get the triangle before first full diagonal line:
    for i in range(rows - 1, 0, -1):
        row = i
        col = cols - 1
        while row < rows and col > limit:
            diag_line.append(lines[row][col])
            row += 1
            col -= 1

        limit -= 1

        diag_lines.append("".join(diag_line))
        diag_line = []

    # Get the rest of the diagonal lines
    for i in range(cols - 1, -1, -1):
        row = 0
        col = i
        while row < rows and col >= 0:
            if lines[row][col] == "\n":
                col -= 1
                row += 1
                continue
            diag_line.append(lines[row][col])
            row += 1
            col -= 1

        if diag_line:
            diag_lines.append("".join(diag_line))
        diag_line = []
    
    return diag_lines

def get_right_diag_lines(lines):
    rows, cols = len(lines), len(lines[0])
    diag_line, diag_lines = [], []
    i, row, col = 0, 0, 0
    limit = 1

    # Get the triangle before first full diagonal line:
    for i in range(rows - 1, 0, -1):
        row = i
        col = 0
        while row < rows and col < limit:
            diag_line.append(lines[row][col])
            row += 1
            col += 1

        limit += 1

        diag_lines.append("".join(diag_line))
        diag_line = []

    # Get the rest of the diagonal lines
    for i in range(0, cols):
        row = 0
        col = i
        while row < rows and col < cols:
            if lines[row][col] == "\n":
                col += 1
                row += 1
                continue
            diag_line.append(lines[row][col])
            row += 1
            col += 1

        if diag_line:
            diag_lines.append("".join(diag_line))
        diag_line = []
    
    return diag_lines

def cnt_xmas(lines):
    last_row = len(lines)
    row, col, cnt = 0, 0, 0

    while row < last_row:
        last_col = len(lines[row])
        col = 0
        while col < last_col:
            if (col + 3) < last_col and lines[row][col:col+4].lower() in ("xmas", "samx"):
                col += 3
                cnt += 1
            # if u have overlapping (i.ex. "xmasmax"):
            elif (col + 2) < last_col and lines[row][col-1:col+3].lower() in ("xmas", "samx"):
                col += 2
                cnt += 1
            col+= 1
        row += 1

    return cnt

def read_input(path):
    file = open(path, 'r')

    horiz_lines = []

    line = file.readline()
    while line:
        horiz_lines.append(line.strip())
        line = file.readline()

    lines = [horiz_lines, get_vertical_lines(horiz_lines),
             get_right_diag_lines(horiz_lines), get_left_diag_lines(horiz_lines)]
    res = sum([cnt_xmas(line_type) for line_type in lines])

    file.close()
    return res

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