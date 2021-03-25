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
from elements import Button, centered_text
from board import Board
from analyze import Analysis
pygame.init()


class WindowManager:
    def __init__(self):
        self.active = True
        self.menus = ("Game", "Analysis", "Engines")
        self.tab = 0

        self.board = Board()
        self.analysis = Analysis()

    def draw(self, surface, events, force_redraw=False):
        # Split surface into sections
        width, height = surface.get_size()
        mx, my = pygame.mouse.get_pos()
        clicked = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
                break

        board_size = min(width, height) - 100
        board_loc = (50, 50)
        menu_size = (width-board_size-150, height-100)
        menu_loc = (board_size+100, 50)

        # Board
        self.board.draw(surface, events, board_loc, board_size, force_redraw)

        # Tabs
        tab_size = menu_size[0] / len(self.menus)
        tab_margin = 0
        tab_height = 25

        for i, tab in enumerate(self.menus):
            col = TAB_SEL if i == self.tab else TAB_DESEL
            loc = (menu_loc[0] + tab_size*i + tab_margin, menu_loc[1])
            size = (tab_size - 2*tab_margin, tab_height)
            if loc[0] <= mx <= loc[0]+size[0] and loc[1] <= my <= loc[1]+size[1]:
                col = TAB_SEL
                if clicked:
                    self.tab = i

            pygame.draw.rect(surface, col, (*loc, *size), border_top_left_radius=5, border_top_right_radius=5)
            centered_text(surface, (loc[0]+size[0]//2, loc[1]+size[1]//2), BLACK, FONT_SMALL, tab)
        pygame.draw.rect(surface, TAB_SEL, (menu_loc[0], menu_loc[1]+tab_height, menu_size[0], menu_size[1]-tab_height))

        if self.menus[self.tab] == "Analysis":
            self.analysis.draw(surface, events, (menu_loc[0]+25, menu_loc[1]+25+tab_height), menu_size, self)
