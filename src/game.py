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
import chess
from elements import Button


class Game:
    def __init__(self):
        self.new_game = Button()
        
        # Path to engines
        self.white = None
        self.black = None

        # (white, black)
        self.time = (0, 0)

    def draw(self, surface, events, loc, size, wm):
        self.new_game.draw(surface, events, (loc[0]+size[0]*2/3-50, loc[1]), (size[0]/3, size[1]/12), "New Game")

        if self.new_game.clicked(events):
            wm.board.reset()
