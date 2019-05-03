import time
import random
import sys

grid_size = 8


def read_file(player_color):
    with open("shared_file.txt") as f:
        lines = f.readlines()
    if len(lines) == 0:
        return None
    if lines[0].strip('\n') == str(player_color):
        temp_grid = []
        for line in lines[1:]:
            temp_grid.append(line.strip('\n').split(" ")[:-1])
        return temp_grid
    return None


def read_file_2():
    temp_grid = []
    for i in range(grid_size):
        line = input().split(' ')
        temp_grid.append(line[:-1])
    return temp_grid


def select_move(grid, player_color):
    while True:
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        if grid[x][y] == 'No' or grid[x][y][0] == player_color:
            return x, y


def write_move(move):
    str_to_write = '0\n' + str(move[0]) + " " + str(move[1])
    with open("shared_file.txt", 'w') as f:
        f.write(str_to_write)


def main():
    player_color = sys.argv[1]
    
    is_start = ""
    while is_start != "start":
        is_start = input()
    while True:
        while True:
            # grid = read_file(player_color)
            grid = read_file_2()
            if grid is not None:
                break
            time.sleep(.01)
        move = select_move(grid, player_color)
        # write_move(move)
        print(move[0], move[1])


if __name__ == "__main__":
    main()
