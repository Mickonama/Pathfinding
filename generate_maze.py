import random
import sys
import threading
from time import sleep

import pygame

from pygame import draw_py, surface
from pygame.color import Color

sys.setrecursionlimit(1000000)
threading.stack_size(2**27)

N = 200 * 2 + 1
M = 200 * 2 + 1

HEIGHT = N * (1000 // N)
WIDTH = M * (1000 // N)
gap = HEIGHT // N

CELL_UNVISITED = 1
CELL_VISITED = 2
WALL = 3


def move(cell):
    shuffler = list()
    if cell[0] > 1:
        shuffler.append((cell[0] - 2, cell[1], cell[0] - 1, cell[1]))

    if cell[0] < N - 2:
        shuffler.append((cell[0] + 2, cell[1], cell[0] + 1, cell[1]))

    if cell[1] > 1:
        shuffler.append((cell[0], cell[1] - 2, cell[0], cell[1] - 1))

    if cell[1] < M - 2:
        shuffler.append((cell[0], cell[1] + 2, cell[0], cell[1] + 1))
    return shuffler


def dfs(cell=(1, 1, 1, 1)):
    table[cell[0]][cell[1]] = CELL_VISITED
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    shuffler = move(cell)

    random.shuffle(shuffler)
    for i in shuffler:
        if table[i[0]][i[1]] == CELL_UNVISITED:
            table[i[2]][i[3]] = CELL_VISITED
            pygame.draw.rect(screen, Color('black'), (cell[0] * gap, cell[1] * gap, gap, gap))
            pygame.draw.rect(screen, Color('black'), (i[2] * gap, i[3] * gap, gap, gap))
            pygame.draw.rect(screen, Color('red'), (i[0] * gap, i[1] * gap, gap, gap))
            pygame.display.update()
            # sleep(.05)
            dfs(i)
            pygame.draw.rect(screen, Color('black'), (i[0] * gap, i[1] * gap, gap, gap))
            # pygame.draw.rect(screen, Color('red'), (i[2] * gap, i[3] * gap, gap, gap))
            # pygame.display.update()
            # sleep(.05)
            # pygame.draw.rect(screen, Color('black'), (i[2] * gap, i[3] * gap, gap, gap))
            pygame.draw.rect(screen, Color('red'), (cell[0] * gap, cell[1] * gap, gap, gap))
            pygame.display.update()
            # sleep(.05)



def alt_dfs():
    stack = list()
    stack.append((1, 1, 1, 1))
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        current_cell = stack.pop()
        if table[current_cell[0]][current_cell[1]] == CELL_UNVISITED:
            table[current_cell[0]][current_cell[1]] = CELL_VISITED
            # sleep(0.01)
            shuffler = move(current_cell)
            random.shuffle(shuffler)
            for k in shuffler:
                if table[k[0]][k[1]] == CELL_UNVISITED:
                    table[k[2]][k[3]] = CELL_VISITED
                    pygame.draw.rect(screen, Color('black'), (current_cell[0] * gap, current_cell[1] * gap, gap, gap))
                    pygame.draw.rect(screen, Color('black'), (k[2] * gap, k[3] * gap, gap, gap))
                    pygame.display.update()
                    # sleep(0.5)
                    stack.append(k)
        # sleep(0.01)
    print("RESULT")


if __name__ == '__main__':

    pygame.init()
    screen: surface.Surface = pygame.display.set_mode(size=(HEIGHT, WIDTH))
    table = [[CELL_UNVISITED for i in range(M)] for j in range(N)]
    for i in range(N):
        for j in range(M):
            if i % 2 == 0 or j % 2 == 0:
                pygame.draw.rect(screen, Color('white'), (i * gap, j * gap, gap, gap))
                table[i][j] = WALL
    pygame.display.update()
    dfs_thread = threading.Thread(target=dfs)
    if N > 100:
        dfs_thread.start()
        dfs_thread.join()
    else:
        dfs()
    print('RESULT')
    table[1][1] = 0
    with open('maze_input.txt', 'w') as f:
        for i in range(N):
            output = ""
            for j in range(M):
                output += str(table[i][j]) + " "
            output += '\n'
            f.write(output)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
