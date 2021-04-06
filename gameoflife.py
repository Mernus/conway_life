import pygame
from constraints import FPS, HEIGHT, HEIGHT_PER_TILE, RESOLUTION, TILE_SIZE, WIDTH, WIDTH_PER_TILE
from copy import deepcopy


def initialize():
    """
    Инициализируем сам pygame, поверхность для отображения, стартовое заполнение и базовый маззив для новых заполнений.

    :return:
    :rtype:
    """
    pygame.init()
    surface = pygame.display.set_mode(RESOLUTION)

    # Будем юзать это для отрисовки новых состояний поля, по дефолту заполняем нулями
    base_field = [[0 for _ in range(WIDTH_PER_TILE)] for _ in range(HEIGHT_PER_TILE)]
    # Это стартовое состояние поля
    start_field = [[1 if j < (WIDTH_PER_TILE - i) // 3 or i > HEIGHT_PER_TILE // 2 + 30
                    else 0
                    for i in range(WIDTH_PER_TILE)] for j in range(HEIGHT_PER_TILE)]

    return surface, pygame.time.Clock(), base_field, start_field


def check_cell(field_state, cell_x, cell_y):
    """
    Узнаем кол-во активных полей вокруг точки с переданными координатами на текущем поле.

    :param field_state:
    :type field_state:
    :param cell_x:
    :type cell_x:
    :param cell_y:
    :type cell_y:
    :return:
    :rtype:
    """
    count = 0  # счётчик для количества активных точек вокруг переданной
    # проверяем активность тайлов в квадрате 3х3 вокруг точки
    for j in range(cell_y - 1, cell_y + 2):
        for i in range(cell_x - 1, cell_x + 2):
            if field_state[j][i]:
                count += 1

    # если у нас активна сама точка, то должны быть 2 или 3 точки активные вокруг неё
    if field_state[cell_y][cell_x]:
        return count == 3 or count == 4

    # в противном случае, чтобы точка стала активной, вокруг неё должны быть ровно 3 активные точки
    return count == 3


def fill_surface(surface):
    """
    Подготавливаем поверхность. Красим саму поверхность, отрисовываем сетку, ловим евент выхода из приложения.

    :param surface:
    :type surface:
    :return:
    :rtype:
    """
    surface.fill(pygame.Color('Gainsboro'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    for x in range(0, WIDTH, TILE_SIZE):
        pygame.draw.line(surface, pygame.Color('DarkSlateGray'), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILE_SIZE):
        pygame.draw.line(surface, pygame.Color('DarkSlateGray'), (0, y), (WIDTH, y))


if __name__ == '__main__':
    board_surface, clock, next_field_state, current_field_state = initialize()
    while True:
        fill_surface(board_surface)

        for i in range(1, WIDTH_PER_TILE - 1):
            for j in range(1, HEIGHT_PER_TILE - 1):
                if current_field_state[j][i]:
                    pygame.draw.rect(board_surface, pygame.Color('IndianRed'),
                                     (i * TILE_SIZE + 2, j * TILE_SIZE + 2, TILE_SIZE - 2, TILE_SIZE - 2))
                next_field_state[j][i] = check_cell(current_field_state, i, j)

        current_field_state = deepcopy(next_field_state)

        pygame.display.flip()
        clock.tick(FPS)
