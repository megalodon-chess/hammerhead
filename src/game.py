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
from elements import Button, centered_text


class Game:
    def __init__(self):
        self.new_game = Button()
        self.turn = True
        
        # Path to engines
        self.white = None
        self.black = None

        # (white, black) in 0.1 seconds
        self.time = (0, 0)

    def draw(self, surface, events, loc, size, wm):
        self.new_game.draw(surface, events, (loc[0]+size[0]*2/3-50, loc[1]), (size[0]/3, size[1]/12), "New Game")

        if self.new_game.clicked(events):
            wm.board.reset()

        whr = self.time[0]//36000
        whr_secs = whr*36000
        wmn = (self.time[0]-whr_secs)//600
        wsc = (self.time[0]-whr_secs-wmn*600)/10
        if wsc.is_integer():
            wsc = int(wsc)

        bhr = self.time[1]//36000
        bhr_secs = bhr*36000
        bmn = (self.time[1]-bhr_secs)//600
        bsc = (self.time[1]-bhr_secs-bmn*600)/10
        if bsc.is_integer():
            bsc = int(bsc)

        wtime = f"{whr+':' if whr else ''}{wmn}:{wsc}"
        btime = f"{bhr+':' if bhr else ''}{bmn}:{bsc}"

        centered_text(surface, loc, BLACK, FONT_MED, wtime)
        centered_text(surface, (loc[0], loc[1]+50), BLACK, FONT_MED, btime)
