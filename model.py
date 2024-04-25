import pygame
import os
import math

"""
Tato metoda vrátí velikost (width, height), aby zůstal zachovaný poměr stran, width je požadovaná šířka
"""


def getNewSizeByHeight(picture, height):
    new_size = (picture.get_width() / picture.get_height(), 1)
    return (math.floor(new_size[0] * height), math.floor(new_size[1] * height))


def getNewSizeByWidth(picture, width):
    new_size = (1, picture.get_height() / picture.get_width())
    return (math.floor(new_size[0] * width), math.floor(new_size[1] * width))


"""
BARVY
"""
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (190, 190, 190)
GRAY = (42, 42, 42)
BLACK = (0, 0, 0)
TRANSPARENT = (255, 255, 255, 128)

# Počet řádků a sloupců
count_of_rows, count_of_cols = 9, 16

NOT_USABLE_NODES = ["aa", "ba", "ca", "da", "ac", "ad", "bc", "bd", "cc", "cd", "dc", "dd", "af", "ag", "bf", "bg",
                    "df", "dg", "ef", "eg", "gf", "gg", "hf", "hg",
                    "aj", "ak", "bj", "bk", "dj", "dk", "ej", "ek", "gj", "gk", "hj", "hk", "an", "ao", "bn", "bo",
                    "dn", "do", "en", "eo", "gn", "go", "hn", "ho", "fp", "gp", "hp", "ip"]

SPEED_OF_PEOPLES = 4

# Písmena, která lze používat v identifikaci uzlu
letters = {
    'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8,
    'i': 9, 'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16,
    'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24,
    'y': 25, 'z': 26, 'A': 27, 'B': 28, 'C': 29, 'D': 30, 'E': 31, 'F': 32

}

# Předchozí a následující písmeno jednotlivých písmen
prev_next_letter = {
    'a': [None, 'b'], 'b': ['a', 'c'], 'c': ['b', 'd'], 'd': ['c', 'e'], 'e': ['d', 'f'], 'f': ['e', 'g'],
    'g': ['f', 'h'], 'h': ['g', 'i'],
    'i': ['h', 'j'], 'j': ['i', 'k'], 'k': ['j', 'l'], 'l': ['k', 'm'], 'm': ['l', 'n'], 'n': ['m', 'o'],
    'o': ['n', 'p'], 'p': ['o', 'q'],
    'q': ['p', 'r'], 'r': ['q', 's'], 's': ['r', 't'], 't': ['s', 'u'], 'u': ['t', 'v'], 'v': ['u', 'w'],
    'w': ['v', 'x'], 'x': ['w', 'y'],
    'y': ['x', 'z'], 'z': ['y', 'A'], 'A': ['z', 'B'], 'B': ['A', 'C'], 'C': ['B', 'D'], 'D': ['C', 'E'],
    'E': ['D', 'F'], 'F': ['E', None]
}

running = True
clock = pygame.time.Clock()

FPS = 60
WIDTH = 1280
HEIGHT = 720

pygame.font.init()  #načtení fontu

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A star algoritmus 2")

SCREEN.fill(YELLOW)

LEFT_CORNER = 248
RIGHT_CORNER = 210



#Šířka obdélníku
FLOOR_NODES_WIDTH = WIDTH - LEFT_CORNER - RIGHT_CORNER
side_width = FLOOR_NODES_WIDTH // count_of_cols

#Výška menu ve hře
MENU_HEIGHT = WIDTH // 6

#Obrázky
RED_CIRCLE = pygame.image.load(os.path.join('images', 'red_circle.png'))
RED_CIRCLE = pygame.transform.scale(RED_CIRCLE, (side_width // 2, side_width // 2))
FLOOR = pygame.image.load(os.path.join('images', 'floor.png'))
FLOOR = pygame.transform.scale(FLOOR, (WIDTH, HEIGHT - MENU_HEIGHT))

TOP_FLOOR = pygame.mask.from_surface(FLOOR).get_bounding_rects()[0].top
FLOOR_MEDIAN = (WIDTH - LEFT_CORNER - RIGHT_CORNER) // 2

#Výška obdélníku/uzlu
FLOOR_NODES_HEIGHT = HEIGHT - TOP_FLOOR - MENU_HEIGHT
side_height = FLOOR_NODES_HEIGHT // count_of_rows

#Textové Fonty
textFont = pygame.font.SysFont("cambria", side_height // 2)

rectangle = pygame.Rect(FLOOR_MEDIAN-100, TOP_FLOOR, 200, 200)

"""
1) Vykreslit podlahu v prostoru

2) Po kliknutí získáme podlahové souřadnice ze screenových
3) Zjistíme ve kterém uzlu v grafu se kliknutá pozice nachází (fun_inv(podlahové souřadnice))
4) Provedeme A* Star Algoritmus, budeme procházet přes středy prostorových uzlů
"""
