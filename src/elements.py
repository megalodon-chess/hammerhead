#
#  Hammerhead
#  Chess GUI written in Python.
#  Copyright the Megalodon developers
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
pygame.init()


def centered_text(surf, loc, col, font, text, cx=True, cy=True):
    text_surf = font.render(text, 1, col)
    loc = list(loc)
    if cx:
        loc[0] -= text_surf.get_width()//2
    if cy:
        loc[1] -= text_surf.get_height()//2
    surf.blit(text_surf, loc)


class Button:
    def __init__(self):
        self.prev_loc = (0, 0)
        self.prev_size = (0, 0)

    def hovered(self):
        mouse = pygame.mouse.get_pos()
        if self.prev_loc[0] <= mouse[0] <= self.prev_loc[0]+self.prev_size[0]:
            if self.prev_loc[1] <= mouse[1] <= self.prev_loc[1]+self.prev_size[1]:
                return True
        return False

    def clicked(self, events):
        if self.hovered():
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return True
        return False

    def draw(self, surface, events, loc, size, text):
        self.prev_loc = loc
        self.prev_size = size

        color = (GRAY_DARK if self.clicked(events) else WHITE) if self.hovered() else GRAY_LIGHT
        pygame.draw.rect(surface, color, (*loc, *size))
        pygame.draw.rect(surface, WHITE, (*loc, *size), 2)
        centered_text(surface, (loc[0]+size[0]//2, loc[1]+size[1]//2), BLACK, FONT_MED, text)
