import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import numpy as np
import subprocess
import sys
from time import time

vertices = (
    (1.5, -1.5, -1.5),
    (1.5, 1.5, -1.5),
    (-1.5, 1.5, -1.5),
    (-1.5, -1.5, -1.5),
    (1.5, -1.5, 1.5),
    (1.5, 1.5, 1.5),
    (-1.5, -1.5, 1.5),
    (-1.5, 1.5, 1.5)
    )

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
    )


def draw_text(position, text_string, size, color_):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text_string, True, color_, (0, 0, 0, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)


def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def draw_grid_y():
    draw_cube()
    glPushMatrix()
    for i in range(3):
        glTranslatef(0.0, 3, 0.0)
        draw_cube()
    glPopMatrix()
    glPushMatrix()
    for i in range(4):
        glTranslatef(0.0, -3, 0.0)
        draw_cube()
    glPopMatrix()


def draw_grid():
    draw_grid_y()
    glPushMatrix()
    for i in range(3):
        glTranslatef(3.0, 0.0, 0.0)
        draw_grid_y()
    glPopMatrix()
    glPushMatrix()
    for i in range(4):
        glTranslatef(-3.0, 0.0, 0.0)
        draw_grid_y()
    glPopMatrix()


def draw_move(selected_cube):
    glPushMatrix()
    glTranslatef((selected_cube[0] - 4) * 3, (selected_cube[1] - 4) * 3, 0)
    glBegin(GL_QUADS)
    glVertex3f(1.5, 1.5, -1.5)
    glVertex3f(-1.5, 1.5, -1.5)
    glVertex3f(-1.5, -1.5, -1.5)
    glVertex3f(1.5, -1.5, -1.5)
    glEnd()
    glPopMatrix()


def draw_reaction(cubes):
    glColor3f(1, .8, .1)
    for cube in cubes:
        draw_move(cube)


def draw_sphere(radius, is_red):
    points = np.zeros((105, 105, 3))
    stack = 20
    slices = 20
    for i in range(stack+1):
        h = radius*math.sin(float((i/stack))*(math.pi/2))
        r = radius*math.cos(float((i/stack))*(math.pi/2))
        for j in range(slices+1):
            points[i][j][0] = r*math.cos(float((j/slices))*2*math.pi)
            points[i][j][1] = r*math.sin(float((j/slices))*2*math.pi)
            points[i][j][2] = h
    for i in range(stack):
        glColor3f(is_red*(i+stack)/(2*stack), (1-is_red)*i/stack, 0)
        for j in range(slices):
            glBegin(GL_QUADS)
            glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])
            glVertex3f(points[i][j+1][0], points[i][j+1][1], points[i][j+1][2])
            glVertex3f(points[i+1][j+1][0], points[i+1][j+1][1], points[i+1][j+1][2])
            glVertex3f(points[i+1][j][0], points[i+1][j][1], points[i+1][j][2])
            glVertex3f(points[i][j][0], points[i][j][1], -points[i][j][2])
            glVertex3f(points[i][j+1][0], points[i][j+1][1], -points[i][j+1][2])
            glVertex3f(points[i+1][j+1][0], points[i+1][j+1][1], -points[i+1][j+1][2])
            glVertex3f(points[i+1][j][0], points[i+1][j][1], -points[i+1][j][2])
            glEnd()


def draw_spheres():
    global grid, angles
    sphere_color = {'R': 1, 'G': 0}
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != 'No':
                glPushMatrix()
                glTranslatef((i - 4)*3, (j - 4)*3, 0)

                glRotatef(angles[i][j], 0, 0, 1)
                angles[i][j] = (angles[i][j] + 5) % 360

                if grid[i][j][1] == '1':
                    draw_sphere(.7, sphere_color[grid[i][j][0]])

                elif grid[i][j][1] == '2':

                    glPushMatrix()
                    glTranslatef(-.3, 0, 0)
                    draw_sphere(.6, sphere_color[grid[i][j][0]])
                    glPopMatrix()

                    glPushMatrix()
                    glTranslatef(.3, 0, 0)
                    draw_sphere(.6, sphere_color[grid[i][j][0]])
                    glPopMatrix()

                elif grid[i][j][1] == '3':

                    glPushMatrix()
                    glTranslatef(-.3, -.2, 0)
                    draw_sphere(.6, sphere_color[grid[i][j][0]])
                    glPopMatrix()

                    glPushMatrix()
                    glTranslatef(.3, -.2, 0)
                    draw_sphere(.6, sphere_color[grid[i][j][0]])
                    glPopMatrix()

                    glPushMatrix()
                    glTranslatef(0, .2, 0)
                    draw_sphere(.6, sphere_color[grid[i][j][0]])
                    glPopMatrix()

                elif grid[i][j][1] >= '4':

                    glPushMatrix()
                    glTranslatef(-.3, -.2, 0)
                    draw_sphere(.6, sphere_color[grid[i][j][0]])
                    glPopMatrix()

                    glPushMatrix()
                    glTranslatef(.3, -.2, 0)
                    draw_sphere(.6, sphere_color[grid[i][j][0]])
                    glPopMatrix()

                    glPushMatrix()
                    glTranslatef(.3, .2, 0)
                    draw_sphere(.6, sphere_color[grid[i][j][0]])
                    glPopMatrix()

                    glPushMatrix()
                    glTranslatef(-.3, .2, 0)
                    draw_sphere(.6, sphere_color[grid[i][j][0]])
                    glPopMatrix()
                glPopMatrix()


grid = None
angles = None


def read_move():
    with open("shared_file.txt") as f:
        lines = f.readlines()
    f.close()
    if len(lines)<2:
        return None
    if lines[0].strip('\n') == '0':
        if lines[0].strip('\n') == '0':
            return lines[1].strip('\n').split()
    return None
   

def check_validity(values):
    global cur_player, players, invalid_move

    if len(values) != 2:
        invalid_move = True
        return False

    if not values[0].isdigit() or not values[1].isdigit():
        invalid_move = True
        return False

    values = [int(value) for value in values]
    if values[0] >= 8 or values[1] >= 8:
        invalid_move = True
        return False
    if grid[values[0]][values[1]][0] == players[1 - cur_player]:
        invalid_move = True
        return False
    return True


def check_reaction(selected_cube):
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    count = 0
    for dir in dirs:
        temp = np.array(selected_cube) + np.array(dir)
        if temp[0] > -1 and temp[0] < 8 and temp[1] > -1 and temp[1] < 8:
            count += 1
    return count


def update_grid(selected_cube):
    global grid, cur_player, players, grid_updated, cubes_to_update
    x = selected_cube[0]
    y = selected_cube[1]
    if grid[x][y] == 'No':
        grid[x][y] = players[cur_player] + '1'
    else:
        atom_count = int(grid[x][y][1])
        if check_reaction(selected_cube) == atom_count + 1:
            cubes_to_update.append(selected_cube)
        grid[x][y] = players[cur_player] + str(int(grid[x][y][1])+1)
    grid_updated = True


def reaction(selected_cube):
    global grid, players, cur_player, cubes_to_update
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    x = selected_cube[0]
    y = selected_cube[1]
    atom_count = int(grid[x][y][1])
    react_count = check_reaction(selected_cube)
    if react_count == atom_count:
        grid[x][y] = "No"
    else:
        count = atom_count - react_count
        if count >= react_count:
            cubes_to_update.append(selected_cube)
        grid[x][y] = players[cur_player] + str(count)
    for dir in dirs:
        temp = np.array(selected_cube) + np.array(dir)
        if temp[0] > -1 and temp[0] < 8 and temp[1] > -1 and temp[1] < 8:
            update_grid(temp)


def write_grid():
    global cur_player, grid
    str_to_write = players[cur_player] + '\n'
    for i in grid:
        for j in i:
            str_to_write += j + " "
        str_to_write += '\n'
    with open("shared_file.txt", 'w') as f:
        f.write(str_to_write[:-1])



def write_grid_2():
    global cur_player, grid, p1
    # str_to_write = players[cur_player] + '\n'
    str_to_write = ""
    for i in grid:
        for j in i:
            str_to_write += j + " "
        str_to_write += '\n'
    print(str_to_write, file=p1.stdin, flush=True, end="")


def check_winner():
    global move_count, grid, invalid_move, cur_player, too_much_time
    if invalid_move:
        return 1 - cur_player
    if too_much_time:
        return 1 - cur_player
    if move_count <= 2:
        return -1
    green = False
    red = False
    if 'G1' in grid or 'G2' in grid or 'G3' in grid or 'G4' in grid or 'G5' in grid:
        green = True
    if 'R1' in grid or 'R2' in grid or 'R3' in grid or 'R4' in grid or 'R5' in grid:
        red = True
    if green and not red:
        return 1
    if red and not green:
        return 0
    return -1


cur_player = None
players = ['R', 'G']
cubes_to_update = None
grid_updated = None
move_count = None
move_read = None
invalid_move = None
move_speed = None
is_over = None
p1 = None
too_much_time = False
start_time = 0
has_start = None

def init():
    global grid, angles, cur_player, cubes_to_update, grid_updated, move_count, move_read, invalid_move, move_speed, p1, start_time, is_over, has_start
    pygame.init()
    display = (800, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 80.0)
    grid = np.full((8, 8), 'No')
    cubes_to_update = []
    angles = np.zeros((8, 8))
    cur_player = 0
    grid_updated = False
    move_count = 0
    move_read = False
    invalid_move = False
    move_speed = int(sys.argv[1])
    p1 = subprocess.Popen(['java','playerOne', 'G'], stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                          universal_newlines=True, bufsize=1)
    print('start', file=p1.stdin, flush=True)
    write_grid()
    start_time = time()
    is_over = True
    has_start = False


def display_grid():
    global is_over, grid, cur_player, players, cubes_to_update, grid_updated, move_count, move_read, invalid_move, \
        move_count, too_much_time, start_time, has_start
    glColor3f(1, 0, 0)
    glTranslatef(0.0, 0.0, -45)
    # cur_player = 0
    while True:

        if not is_over and len(cubes_to_update) > 0:
            draw_reaction(cubes_to_update)
            temp = cubes_to_update.copy()
            cubes_to_update.clear()
            for update in temp:
                reaction(update)
            pygame.time.wait(move_speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    is_over = not is_over
                    if move_count == 0:
                        has_start = True


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if not is_over and not move_read:
            if cur_player == 1:
                selected_cube = p1.stdout.readline().strip('\n').split(" ")
            else:
                while read_move() is None:
                    continue
                selected_cube = read_move()
            end_time = time()
            time_taken = end_time - start_time
            hours, rest = divmod(time_taken,3600)
            minutes, seconds = divmod(rest, 60)
            print(seconds)
            if seconds > 6:
                is_over = True
                too_much_time = True
            move_read = True
            move_count += 1
            if check_validity(selected_cube):
                selected_cube = [int(i) for i in selected_cube]
                update_grid(selected_cube)
                pygame.time.wait(move_speed)
                glColor3f(.6, .6, .6)
                draw_move(selected_cube)
            else:
                invalid_move = True
        if not is_over:
            draw_reaction(cubes_to_update)
        if not is_over and grid_updated and len(cubes_to_update) == 0:  
            cur_player = 1 - cur_player
            
            if cur_player == 1:
                print("Writing in console")
                write_grid_2()
            else:
                print("Writing in file")
                write_grid() 
            start_time = time()
            grid_updated = False
            move_read = False

        draw_text((-5, 5.0, 30.0), "CHAIN REACTION", 32, (120, 120, 220, 255))
        draw_text((-5, 5.5, 30.0), "CSE Fest 2019 - AI Contest", 24, (120, 120, 220, 255))

        if cur_player == 0:
            draw_text((-5, 4, 30.0), "Player 1's move", 24, (250, 10, 10, 255))
        else:
            draw_text((-5, 4, 30.0), "Player 2's move", 24, (10, 250, 10, 255))
        glColor3f(1-cur_player, cur_player, 0)
        draw_grid()
        draw_spheres()
        if not has_start:
            draw_text((-2, 1, 30.0), "Semi Final 1", 56, (120, 120, 220, 255))
            # draw_text((-3, 1, 30.0), "Third Place Playoff", 56, (120, 120, 220, 255))
            # draw_text((-2, 1, 30.0), "THE FINAL", 56, (120, 120, 220, 255))

            draw_text((-6, 0, 30.0), "Lonely_Bot vs Night_Before_Submission", 56, (120, 120, 220, 255))
            # draw_text((-5, 0, 30.0), "Wasted_Potential vs Megatron747", 56, (120, 120, 220, 255))

        if invalid_move:
            draw_text((-4, 1, 30.0), "Invalid Move by Player" + str(cur_player+1), 64, (120, 120, 220, 255))
            is_over = True
        if too_much_time:
            draw_text((-4.5, 1, 30.0), "Too much time taken by Player"  + str(cur_player+1), 64, (120, 120, 220, 255))
            is_over = True
        if check_winner() != -1:
            draw_text((-2.5, 0, 30.0), "Player " + str(check_winner()+1)+" Wins", 64, (120, 120, 220, 255))
            is_over = True
            print(move_count)
           
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    init()
    display_grid()
