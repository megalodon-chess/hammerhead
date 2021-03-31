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

import os
import threading
import pygame
import chess
import chess.engine
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from constants import *
from elements import Button, centered_text
from board import Board
pygame.init()
Tk().withdraw()


class Analysis:
    def __init__(self):
        self.session = 0
        self.eng = ""
        self.info = {}
        self.in_progress = False
        self.load_eng = Button()
        self.start = Button()
        self.stop = Button()

    def nodes_text(self, num):
        if num < 10**5:
            suffix = ""
        elif 10**5 <= num < 10**8:
            suffix = "k"
            num = int(num/10**3)
        elif 10**8 <= num:
            suffix = "m"
            num = int(num/10**6)
        string = suffix
        count = 0
        for digit in reversed(str(num)):
            string = digit + string
            if count % 3 == 2:
                string = "," + string
            count += 1
        if string.startswith(","):
            string = string[1:]
        return string

    def analyze(self, eng_path, wm):
        self.info = {"depth": 0, "nodes": 0, "nps": 0, "score": None, "time": 0}
        self.in_progress = True

        start_move_num = wm.board.move_num
        session = self.session
        engine = chess.engine.SimpleEngine.popen_uci(eng_path)
        if "Threads" in engine.options:
            engine.configure({"Threads": CORES})
        restart = False
        with engine.analysis(wm.board.view_board) as analysis:
            keys = ("depth", "nodes", "nps", "time")
            for info in analysis:
                for key in keys:
                    if key in info:
                        self.info[key] = info[key]
                if "score" in info:
                    self.info["score"] = int(str(info["score"].pov(chess.WHITE))) / 100

                if not wm.active or self.session != session:
                    restart = False
                    break
                if wm.board.move_num != start_move_num:
                    restart = True
                    break

        engine.quit()
        self.in_progress = False
        if restart:
            threading.Thread(target=self.analyze, args=(eng_path,)).start()

    def draw(self, surface, events, loc, size, wm):
        self.load_eng.draw(surface, events, (loc[0]+25, loc[1]+25), (150, 35), "Load Engine")
        self.start.draw(surface, events, (loc[0]+25, loc[1]+70), (150, 35), "Start Analysis")
        self.stop.draw(surface, events, (loc[0]+25, loc[1]+115), (150, 35), "Stop Analysis")
        centered_text(surface, (loc[0]+200, loc[1]+42), BLACK, FONT_SMALL, self.eng, cx=False)

        if self.load_eng.clicked(events) and not self.in_progress:
            settings = load_settings()
            kwargs = {"initialdir": settings["eng_path"]} if "eng_path" in settings else {}
            path = askopenfilename(title="Select Engine", **kwargs)
            if isinstance(path, str) and os.path.isfile(path):
                path = os.path.realpath(path)
                self.eng = path
                settings["eng_path"] = os.path.dirname(path)
                save_settings(settings)
        if self.start.clicked(events) and not self.in_progress and os.path.isfile(self.eng):
            threading.Thread(target=self.analyze, args=(self.eng, wm)).start()
        if self.stop.clicked(events) and self.in_progress:
            self.session += 1

        text = "Analysis in progress" if self.in_progress else "Analysis not in progress"
        centered_text(surface, (loc[0]+25, loc[1]+225), BLACK, FONT_MED, text, cx=False)
        info = (
            ("Depth", "depth"),
            ("Nodes", "nodes"),
            ("Nodes per second", "nps"),
            ("Time", "time"),
            ("Score", "score"),
        )
        for i, (text, key) in enumerate(info):
            if key in self.info:
                key_info = self.info[key]
                text = text + ": "
                text += self.nodes_text(key_info) if "Nodes" in text else str(key_info)
                y = loc[1] + 275 + 25*i
                centered_text(surface, (loc[0]+25, y), BLACK, FONT_SMALL, text, cx=False)
