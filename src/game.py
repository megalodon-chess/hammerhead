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
        self.time = [0, 0]

    def set_time(self, wt=None, bt=None):
        """
        Set the time for the given side in seconds.
        """
        if wt is not None:
            self.time[0] = wt
        if bt is not None:
            self.time[1] = bt

    def reset(self, wm):
        self.turn = True
        self.time = [0, 0]
        wm.board.reset()

    def draw(self, surface, events, loc, size, wm):
        self.new_game.draw(surface, events, (loc[0]+size[0]*2/3-50, loc[1]), (size[0]/3, size[1]/12), "New Game")

        if self.new_game.clicked(events):
            self.reset(wm)

        # Get white times
        whr = self.time[0]//36000
        whr_secs = whr*36000
        wmn = (self.time[0]-whr_secs)//600
        wsc = (self.time[0]-whr_secs-wmn*600)/10
        if wsc.is_integer():
            wsc = int(wsc)

        # Get black times
        bhr = self.time[1]//36000
        bhr_secs = bhr*36000
        bmn = (self.time[1]-bhr_secs)//600
        bsc = (self.time[1]-bhr_secs-bmn*600)/10
        if bsc.is_integer():
            bsc = int(bsc)

        # Convert times into string
        wtime = f"{str(whr)+':' if whr else ''}{'0'+str(wmn) if wmn < 10 else wmn}:{'0'+str(wsc) if wsc < 10 else wsc}"
        btime = f"{str(bhr)+':' if bhr else ''}{'0'+str(bmn) if bmn < 10 else bmn}:{'0'+str(bsc) if bsc < 10 else bsc}"

        # Get engine name
        wname = self.white.split("/")[-1] if self.white is not None else "N/A"
        bname = self.black.split("/")[-1] if self.black is not None else "N/A"

        # Draw engine name
        wtxt = FONT_MED.render(wname, 1, BLACK)
        btxt = FONT_MED.render(bname, 1, BLACK)
        surface.blit(wtxt, (loc[0], loc[1]+5+9))
        surface.blit(btxt, (loc[0], loc[1]+5+46+9))

        # Get longest engine name
        longest = max(wtxt.get_width(), btxt.get_width())

        # Draw color
        pygame.draw.rect(surface, WHITE, (loc[0]+longest+15, loc[1]+5+9, wtxt.get_height(), wtxt.get_height()))
        pygame.draw.rect(surface, BLACK, (loc[0]+longest+15, loc[1]+5+46+9, btxt.get_height(), btxt.get_height()))

        # Draw time
        pygame.draw.rect(surface, TIME_BOX, (loc[0]+75+longest, loc[1]+5, 100, 36))
        pygame.draw.rect(surface, BLACK,    (loc[0]+75+longest, loc[1]+5, 100, 36), 3)
        pygame.draw.rect(surface, TIME_BOX, (loc[0]+75+longest, loc[1]+5+36+10, 100, 36))
        pygame.draw.rect(surface, BLACK,    (loc[0]+75+longest, loc[1]+5+36+10, 100, 36), 3)
        centered_text(surface, (loc[0]+75+longest+50, loc[1]+5+18), BLACK, FONT_MED, wtime)
        centered_text(surface, (loc[0]+75+longest+50, loc[1]+5+36+10+18), BLACK, FONT_MED, wtime)
