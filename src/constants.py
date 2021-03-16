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

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

for f in os.listdir(IMG_DIR):
    path = os.path.join(IMG_DIR, f)
    img = pygame.image.load(path)
    if f[0] in ("b", "w") and len(f.split(".")[0]) == 2:
        key = f[1].upper() if f[0] == "w" else f[1].lower()
    else:
        key = f.split(".")[0]
    IMAGES[key] = img
