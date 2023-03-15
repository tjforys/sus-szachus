from dataclasses import dataclass
from enum import Enum

import pygame
import math


class PieceType(Enum):
    PAWN = 0
    ROOK = 1
    KNIGHT = 2
    BISHOP = 3
    QUEEN = 4
    KING = 5


class ColorType(Enum):
    WHITE = 0
    BLACK = 1


@dataclass
class Figura:
    x: int
    y: int
    type: PieceType
    color: ColorType


def display_position():
    position = pygame.mouse.get_pos()
    font2 = pygame.font.SysFont('arial', 30)
    text_surface = font2.render(str(position), False, (0, 0, 0))
    screen.blit(text_surface, (300, 50))


def rysowanie_gridu():
    screen.fill((122, 71, 34))
    for i in range(64):
        if (i // 8) % 2 == 0:
            if i % 2 == 0:
                pygame.draw.rect(screen, (219, 210, 125),
                                 pygame.Rect(border_width + (i % 8) * tile_size, border_width + i // 8 * tile_size,
                                             tile_size, tile_size))
            else:
                pygame.draw.rect(screen, (255, 0, 0),
                                 pygame.Rect(border_width + (i % 8) * tile_size, border_width + i // 8 * tile_size,
                                             tile_size, tile_size))
        else:
            if i % 2 == 1:
                pygame.draw.rect(screen, (219, 210, 125),
                                 pygame.Rect(border_width + (i % 8) * tile_size, border_width + i // 8 * tile_size,
                                             tile_size, tile_size))
            else:
                pygame.draw.rect(screen, (255, 0, 0),
                                 pygame.Rect(border_width + (i % 8) * tile_size, border_width + i // 8 * tile_size,
                                             tile_size, tile_size))
    for i in range(9):
        pygame.draw.line(screen, (0, 0, 0), (border_width + i * (width - (border_width * 2)) / 8, border_width),
                         (border_width + i * (width - (border_width * 2)) / 8, height - border_width))
        pygame.draw.line(screen, (0, 0, 0), (border_width, border_width + i * (width - (border_width * 2)) / 8),
                         (width - border_width, border_width + i * (width - (border_width * 2)) / 8))
    for i in range(8):
        font2 = pygame.font.SysFont('arial', 40)
        text_surface = font2.render((rows[i]), False, (0, 0, 0))
        text_width = text_surface.get_rect().width
        text_height = text_surface.get_rect().height
        screen.blit(text_surface, (
            border_width / 2 - text_width / 2, border_width + tile_size / 2 + tile_size * (i) - text_height / 2))

        text_surface = font2.render((columns[i]), False, (0, 0, 0))
        text_width = text_surface.get_rect().width
        text_height = text_surface.get_rect().height
        screen.blit(text_surface, (border_width + tile_size / 2 + tile_size * (i) - text_width / 2, height -
                                   border_width / 2 - text_height / 2))


def rysowanie_figur():
    for i in game_pieces:
        if i.type is PieceType.KING:
            text = 'K'
        if i.type is PieceType.QUEEN:
            text = 'Q'
        if i.type is PieceType.BISHOP:
            text = 'B'
        if i.type is PieceType.ROOK:
            text = 'R'
        if i.type is PieceType.KNIGHT:
            text = 'N'
        if i.type is PieceType.PAWN:
            text = 'P'
        if i.color is ColorType.WHITE:
            color = (255, 255, 255)
        else:
            color = (0, 0, 0)

        font2 = pygame.font.SysFont('arial', 50)
        text_surface = font2.render(text, False,
                                    color)
        text_width = text_surface.get_rect().width
        text_height = text_surface.get_rect().height
        screen.blit(text_surface, (border_width + tile_size / 2 + tile_size * (i.x - 1) - text_width / 2,
                                   height - border_width - tile_size / 2 - tile_size * (i.y - 1) - text_height / 2))


def mouse_tile_check():
    global tile_x
    global tile_y
    position = pygame.mouse.get_pos()
    if position[0] > border_width and position[0] < width - border_width and position[1] > border_width and position[
        1] < height - border_width:
        tile_x = int((position[0] - border_width) // tile_size + 1)
        tile_y = int(8 - (position[1] - border_width) // tile_size)
        font2 = pygame.font.SysFont('arial', 30)
        text_surface = font2.render(str(tile_x) + ' ' + str(tile_y), False, (0, 0, 0))
        screen.blit(text_surface, (width - 300, 50))


def piece_movement(piece):
    global movelist
    global true_movelist
    movelist = []
    true_movelist = []
    if piece.type is PieceType.BISHOP:
        movement_bishop(piece.x, piece.y, piece)
    if piece.type is PieceType.PAWN:
        if piece.color is ColorType.WHITE and piece.y == 7:
            pass
    if piece.type is PieceType.KNIGHT:
        movelist = [[tile_x - 2, tile_y - 1], [tile_x - 2, tile_y + 1], [tile_x + 1, tile_y - 2],
                    [tile_x + 1, tile_y + 2], [tile_x + 2, tile_y - 1], [tile_x + 2, tile_y + 1],
                    [tile_x - 1, tile_y - 2], [tile_x - 1, tile_y + 2]]
        if piece.color is ColorType.WHITE:
            for i in movelist:

                if i in white_pieces_coordinates or (i[0] < 1 or i[0] > 8 or i[1] < 1 or i[1] > 8):
                    continue
                true_movelist.append(i)
        elif piece.color is ColorType.BLACK:
            for i in movelist:

                if i in black_pieces_coordinates or (i[0] < 1 or i[0] > 8 or i[1] < 1 or i[1] > 8):
                    continue
                true_movelist.append(i)
                print(true_movelist)


    print(true_movelist)
def movement_bishop(x,y, piece):
    global true_movelist
    global movelist
    for i in range(7):
        coords=[x+i+1, y+i+1]
        if coords[0] >= 1 and coords[0] <= 8 and coords[1] >= 1 and coords[1] <= 8:
            if piece.color is ColorType.BLACK:
                if coords in black_pieces_coordinates:
                    break
                elif  coords in white_pieces_coordinates:
                    movelist.append(coords)
                    break
            if piece.color is ColorType.WHITE:
                if coords in white_pieces_coordinates:
                    break
                elif  coords in black_pieces_coordinates:
                    movelist.append(coords)
                    break
            movelist.append(coords)
    for i in range(7):
        coords = [x + (-1*(i+1)) , y + i + 1]
        if coords[0] >= 1 and coords[0] <= 8 and coords[1] >= 1 and coords[1] <= 8:
            if piece.color is ColorType.BLACK:
                if coords in black_pieces_coordinates:
                    break
                elif coords in white_pieces_coordinates:
                    movelist.append(coords)
                    break
            if piece.color is ColorType.WHITE:
                if coords in white_pieces_coordinates:
                    break
                elif coords in black_pieces_coordinates:
                    movelist.append(coords)
                    break
            movelist.append(coords)
    for i in range(7):
        coords =[x + i + 1, y + (-1*(i+1))]
        if coords[0] >= 1 and coords[0] <= 8 and coords[1] >= 1 and coords[1] <= 8:
            if piece.color is ColorType.BLACK:
                if coords in black_pieces_coordinates:
                    break
                elif coords in white_pieces_coordinates:
                    movelist.append(coords)
                    break
            if piece.color is ColorType.WHITE:
                if coords in white_pieces_coordinates:
                    break
                elif coords in black_pieces_coordinates:
                    movelist.append(coords)
                    break
            movelist.append(coords)
    for i in range(7):
        coords = [x + (-1*(i+1)), y +(-1*(i+1))]
        if coords[0] >= 1 and coords[0] <= 8 and coords[1] >= 1 and coords[1] <= 8:
            if piece.color is ColorType.BLACK:
                if coords in black_pieces_coordinates:
                    break
                elif coords in white_pieces_coordinates:
                    movelist.append(coords)
                    break
            if piece.color is ColorType.WHITE:
                if coords in white_pieces_coordinates:
                    break
                elif coords in black_pieces_coordinates:
                    movelist.append(coords)
                    break
            movelist.append(coords)
    true_movelist=movelist
    print(true_movelist)

    print (movelist)

def rysowanie_ruchow():
    for i in true_movelist:
        pygame.draw.circle(screen, (0, 0, 0), (border_width + tile_size * (i[0] - 1) + tile_size / 2,
                                               border_width + width - tile_size * (i[1] + 1) + tile_size / 2 - 9), 12)


pygame.init()

king_white = Figura(x=5, y=1, type=PieceType.KING, color=ColorType.WHITE)
queen_white = Figura(x=4, y=1, type=PieceType.QUEEN, color=ColorType.WHITE)
rooks_white = [Figura(x=1, y=1, type=PieceType.ROOK, color=ColorType.WHITE),
               Figura(x=8, y=1, type=PieceType.ROOK, color=ColorType.WHITE)]
bishops_white = [Figura(x=3, y=1, type=PieceType.BISHOP, color=ColorType.WHITE),
                 Figura(x=6, y=1, type=PieceType.BISHOP, color=ColorType.WHITE)]
knights_white = [Figura(x=2, y=1, type=PieceType.KNIGHT, color=ColorType.WHITE),
                 Figura(x=7, y=1, type=PieceType.KNIGHT, color=ColorType.WHITE)]
king_black = Figura(x=5, y=8, type=PieceType.KING, color=ColorType.BLACK)
queen_black = Figura(x=4, y=8, type=PieceType.QUEEN, color=ColorType.BLACK)
rooks_black = [Figura(x=1, y=8, type=PieceType.ROOK, color=ColorType.BLACK),
               Figura(x=8, y=8, type=PieceType.ROOK, color=ColorType.BLACK)]
bishops_black = [Figura(x=3, y=8, type=PieceType.BISHOP, color=ColorType.BLACK),
                 Figura(x=6, y=8, type=PieceType.BISHOP, color=ColorType.BLACK)]
knights_black = [Figura(x=2, y=8, type=PieceType.KNIGHT, color=ColorType.BLACK),
                 Figura(x=7, y=8, type=PieceType.KNIGHT, color=ColorType.BLACK)]
pawns_white = []
game_pieces = [king_white, queen_white, rooks_white[0], rooks_white[1], bishops_white[0], bishops_white[1],
               knights_white[0], knights_white[1], king_black, queen_black, rooks_black[0], rooks_black[1],
               bishops_black[0], bishops_black[1],
               knights_black[0], knights_black[1]]

for i in range(8):
    game_pieces.append(Figura(x=i + 1, y=2, type=PieceType.PAWN, color=ColorType.WHITE))
    game_pieces.append(Figura(x=i + 1, y=7, type=PieceType.PAWN, color=ColorType.BLACK))
pieces_coordinates = []

print(pieces_coordinates)
true_movelist = []
tile_x = 1
tile_y = 1
movelist = []
border_width = 50
width = 796
height = 796
rows = list('87654321')
columns = list('abcdefgh')
tile_size = (width - 2 * border_width) / 8
# Set up the drawing window
white_pieces_coordinates = []
black_pieces_coordinates = []
for i in game_pieces:
    if i.color is ColorType.WHITE:
        white_pieces_coordinates.append([i.x, i.y])
    else:
        black_pieces_coordinates.append([i.x, i.y])
print(white_pieces_coordinates)
print(black_pieces_coordinates)
screen = pygame.display.set_mode([width, height])
selection = False
print(pieces_coordinates)
# Run until the user asks to quit
running = True
while running:
    white_pieces_coordinates = []
    black_pieces_coordinates = []
    for i in game_pieces:
        if i.color is ColorType.WHITE:
            white_pieces_coordinates.append([i.x, i.y])
        else:
            black_pieces_coordinates.append([i.x, i.y])
        pieces_coordinates.append([i.x, i.y])
    # Did the user click the window close button?

    # Fill the background with white

    rysowanie_gridu()
    rysowanie_figur()
    display_position()
    mouse_tile_check()
    # Flip the display

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in game_pieces:

                if i.x == tile_x and i.y == tile_y and selection == False and [tile_x, tile_y] in pieces_coordinates:
                    piece_movement(i)
                    mark = i
                    selection = True
            if [tile_x, tile_y] in true_movelist:
                for a in game_pieces:
                    if tile_x == a.x and tile_y == a.y:
                        game_pieces.remove(a)
                mark.x = tile_x
                mark.y = tile_y
                true_movelist = []
                selection = False
    rysowanie_ruchow()
    pygame.display.flip()
# Done! Time to quit.
pygame.quit()

print("ussususususu")