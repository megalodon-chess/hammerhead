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

import pygame
from constants import *
from wm import WindowManager
pygame.init()


def main():
    width, height = 1280, 720
    prev_width, prev_height = 1280, 720

    pygame.display.set_caption("Hammerhead Chess GUI")
    surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    winman = WindowManager()

    while True:
        clock.tick(FPS)
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                winman.active = False
                pygame.quit()
                return
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
            elif event.type == pygame.ACTIVEEVENT and (width, height) != (prev_width, prev_height):
                surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                prev_width = width
                prev_height = height

        surface.fill(BLACK)
        winman.draw(surface, events)


main()
