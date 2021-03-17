#
#  Hammerhead
#  Chess GUI written in Python.
#  Copyright Megalodon Chess 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import os
import pygame
pygame.init()

PARENT = os.path.dirname(os.path.realpath(__file__))
IMG_DIR = os.path.join(PARENT, "images")

FPS = 60
IMAGES = {}

FONT_SMALL = pygame.font.SysFont("arial", 14)
FONT_MED = pygame.font.SysFont("arial", 24)
FONT_LARGE = pygame.font.SysFont("arial", 36)

BLACK = (0, 0, 0)
GRAY_DARK = (64, 64, 64)
GRAY = (128, 128, 128)
GRAY_LIGHT = (192, 192, 192)
WHITE = (255, 255, 255)

TAB_SEL = (220, 190, 130)
TAB_DESEL = (200, 170, 110)

BOARD_WHITE = (220, 220, 210)
BOARD_WHITE_SELECT = (240, 240, 200)
BOARD_WHITE_MARK = (190, 190, 180)
BOARD_BLACK = (100, 140, 80)
BOARD_BLACK_SELECT = (140, 180, 80)
BOARD_BLACK_MARK = (70, 120, 50)
BOARD_HIGHLIGHT = (0, 0, 0, 100)

for f in os.listdir(IMG_DIR):
    path = os.path.join(IMG_DIR, f)
    img = pygame.image.load(path)
    if f[0] in ("b", "w") and len(f.split(".")[0]) == 2:
        key = f[1].upper() if f[0] == "w" else f[1].lower()
    else:
        key = f.split(".")[0]
    IMAGES[key] = img
