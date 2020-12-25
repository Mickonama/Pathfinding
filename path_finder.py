import sys
from collections import deque
from queue import PriorityQueue
from random import random
from time import sleep

import pygame
from pygame import surface
from pygame.color import Color

from generate_maze import HEIGHT, WIDTH, gap
from maze_cell import Cell

with open('maze_input.txt', 'r') as f:
    table = [[int(x) for x in line.split()] for line in f]
    N = len(table)
    M = len(table[0])

goal = (N - 2, M - 2) # BOTH NUMBERS HAVE TO BE ODD

CELL_VISITED = 1
CELL_UNVISITED = 2
WALL = 3


def evaluate(cell: Cell):
    return abs(cell.pos[0] - goal[0]) + abs(cell.pos[1] - goal[1])


def move(current_cell: Cell):
    shuffler = list()
    if current_cell.pos[0] > 0:
        shuffler.append(Cell((current_cell.pos[0] - 1, current_cell.pos[1]), current_cell, current_cell.level + 1))

    if current_cell.pos[0] < N - 1:
        shuffler.append(Cell((current_cell.pos[0] + 1, current_cell.pos[1]), current_cell, current_cell.level + 1))

    if current_cell.pos[1] > 0:
        shuffler.append(Cell((current_cell.pos[0], current_cell.pos[1] - 1), current_cell, current_cell.level + 1))

    if current_cell.pos[1] < M - 1:
        shuffler.append(Cell((current_cell.pos[0], current_cell.pos[1] + 1), current_cell, current_cell.level + 1))
    return shuffler


def trace_back(cell):
    if cell is None:
        return
    while cell is not None:
        pygame.draw.rect(screen, Color('blue'), (cell.pos[0] * gap, cell.pos[1] * gap, gap, gap))
        pygame.display.update()
        # sleep(0.01)
        print(cell)
        cell = cell.parent


def dfs(cell: Cell, randomize=False):
    stack = list()
    closed = []
    stack.append(cell)
    current_cell = cell
    while current_cell.pos != goal and stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        current_cell = stack.pop()
        if current_cell not in closed:
            closed.append(current_cell)
            pygame.draw.rect(screen, Color('red'), (current_cell.pos[0] * gap, current_cell.pos[1] * gap, gap, gap))
            pygame.display.update()
            # sleep(0.01)
            shuffler = move(current_cell)
            if randomize:
                random.shuffle(shuffler)
            for k in shuffler:
                if table[k.pos[0]][k.pos[1]] == CELL_UNVISITED:
                    stack.append(k)
        pygame.draw.rect(screen, Color('lightgreen'), (current_cell.pos[0] * gap, current_cell.pos[1] * gap, gap, gap))
        pygame.display.update()
        # sleep(0.01)
    trace_back(current_cell)
    print("RESULT")


def bfs(cell: Cell):
    search = deque()
    closed = []
    search.appendleft(cell)
    current_cell = cell
    while current_cell.pos != goal and search:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        current_cell = search.pop()
        if current_cell not in closed:
            closed.append(current_cell)
            pygame.draw.rect(screen, Color('red'), (current_cell.pos[0] * gap, current_cell.pos[1] * gap, gap, gap))
            pygame.display.update()
            # sleep(0.01)
            shuffler = move(current_cell)

            for k in shuffler:
                if table[k.pos[0]][k.pos[1]] == CELL_UNVISITED:
                    search.appendleft(k)
                    pygame.draw.rect(screen, Color('lightgreen'),
                                     (current_cell.pos[0] * gap, current_cell.pos[1] * gap, gap, gap))
            pygame.display.update()
            # sleep(0.01)
    trace_back(current_cell)
    print("RESULT")


def best_first(cell: Cell):
    search = list()
    closed = []
    search.append(cell)
    current_cell = cell
    while current_cell.pos != goal and search:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        current_cell = search.pop()
        if current_cell not in closed:
            closed.append(current_cell)
            pygame.draw.rect(screen, Color('red'), (current_cell.pos[0] * gap, current_cell.pos[1] * gap, gap, gap))
            pygame.display.update()
            # sleep(0.01)
            shuffler = move(current_cell)
            for k in shuffler:
                if table[k.pos[0]][k.pos[1]] == CELL_UNVISITED:
                    search.append(k)
            search.sort(key=lambda x: evaluate(x), reverse=True)
        pygame.draw.rect(screen, Color('lightgreen'), (current_cell.pos[0] * gap, current_cell.pos[1] * gap, gap, gap))
        pygame.display.update()
        # sleep(0.01)
    trace_back(current_cell)
    print("RESULT")


def a_star(cell: Cell):
    search = list()
    closed = []
    search.append(cell)
    current_cell = cell
    while current_cell.pos != goal and search:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        current_cell = search.pop()
        if current_cell not in closed:
            closed.append(current_cell)
            pygame.draw.rect(screen, Color('red'), (current_cell.pos[0] * gap, current_cell.pos[1] * gap, gap, gap))
            pygame.display.update()
            # sleep(0.01)
            shuffler = move(current_cell)
            for k in shuffler:
                if table[k.pos[0]][k.pos[1]] == CELL_UNVISITED:
                    search.append(k)
            search.sort(key=lambda x: evaluate(x) + x.level, reverse=True)
        pygame.draw.rect(screen, Color('lightgreen'), (current_cell.pos[0] * gap, current_cell.pos[1] * gap, gap, gap))
        pygame.display.update()
        # sleep(0.01)
    trace_back(current_cell)
    print("RESULT")


if __name__ == '__main__':
    pygame.init()
    screen: surface.Surface = pygame.display.set_mode(size=(HEIGHT, WIDTH))
    for i in range(N):
        for j in range(M):
            if table[i][j] == WALL:
                pygame.draw.rect(screen, Color('white'), (i * gap, j * gap, gap, gap))
    pygame.draw.rect(screen, Color('blue'), (goal[0] * gap, goal[1] * gap, gap, gap))
    pygame.display.update()
    a_star(Cell((1, 1)))
    # a comment
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
