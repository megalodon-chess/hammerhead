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
import chess
from constants import *


class Board:
    def __init__(self):
        self.board = chess.Board()   # Current position
        self.view_board = None       # Current viewed position

        self.move_num = 0            # Current position is startpos with this many moves
        self.flipped = False

    def set_view(self):
        self.view_board = chess.Board()
        for move in self.board.move_stack[:self.move_num+1]:
            self.view_board.push(move)

    def push(self, move):
        if self.move_num == len(self.board.move_stack):
            self.move_num += 1
        self.board.push(move)
        self.set_view()

    def draw(self, events, size):
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        sq_size = size / 8

        for x in range(8):
            for y in range(8):
                loc = (x*sq_size, y*sq_size)
                col = BOARD_WHITE if (x+y) % 2 == 0 else BOARD_BLACK
                pygame.draw.rect(surf, col, (*loc, sq_size+1, sq_size+1))

        return surf
