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


class WindowManager:
    def __init__(self):
        self.active = True
        self.menus = ("Game", "Analysis", "Engines")
        self.tab = 0

        self.analysis_session = 0
        self.analysis_eng = ""
        self.analysis_info = {}
        self.analysis_in_progress = False
        self.analysis_load_eng = Button()
        self.analysis_start = Button()
        self.analysis_stop = Button()

        self.board = Board()

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

    def analyze(self, eng_path):
        self.analysis_info = {"depth": 0, "nodes": 0, "nps": 0, "score": None, "time": 0}
        self.analysis_in_progress = True

        start_move_num = self.board.move_num
        session = self.analysis_session
        engine = chess.engine.SimpleEngine.popen_uci(eng_path)
        if "Threads" in engine.options:
            engine.configure({"Threads": CORES})
        restart = False
        with engine.analysis(self.board.view_board) as analysis:
            keys = ("depth", "nodes", "nps", "time")
            for info in analysis:
                for key in keys:
                    if key in info:
                        self.analysis_info[key] = info[key]
                if "score" in info:
                    self.analysis_info["score"] = int(str(info["score"].pov(chess.WHITE))) / 100

                if not self.active or self.analysis_session != session:
                    restart = False
                    break
                if self.board.move_num != start_move_num:
                    restart = True
                    break

        engine.quit()
        self.analysis_in_progress = False
        if restart:
            threading.Thread(target=self.analyze, args=(eng_path,)).start()

    def draw(self, surface, events):
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
        self.board.draw(surface, events, board_loc, board_size)

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
            self.analysis_load_eng.draw(surface, events, (menu_loc[0]+25, menu_loc[1]+tab_height+25), (150, 35), "Load Engine")
            self.analysis_start.draw(surface, events, (menu_loc[0]+25, menu_loc[1]+tab_height+70), (150, 35), "Start Analysis")
            self.analysis_stop.draw(surface, events, (menu_loc[0]+25, menu_loc[1]+tab_height+115), (150, 35), "Stop Analysis")
            centered_text(surface, (menu_loc[0]+200, menu_loc[1]+tab_height+42), BLACK, FONT_SMALL, self.analysis_eng, cx=False)

            if self.analysis_load_eng.clicked(events) and not self.analysis_in_progress:
                settings = load_settings()
                kwargs = {"initialdir": settings["analysis_eng_path"]} if "analysis_eng_path" in settings else {}
                path = askopenfilename(title="Select Engine", **kwargs)
                if isinstance(path, str) and os.path.isfile(path):
                    path = os.path.realpath(path)
                    self.analysis_eng = path
                    settings["analysis_eng_path"] = os.path.dirname(path)
                    save_settings(settings)
            if self.analysis_start.clicked(events) and not self.analysis_in_progress and os.path.isfile(self.analysis_eng):
                threading.Thread(target=self.analyze, args=(self.analysis_eng,)).start()
            if self.analysis_stop.clicked(events) and self.analysis_in_progress:
                self.analysis_session += 1

            text = "Analysis in progress" if self.analysis_in_progress else "Analysis not in progress"
            centered_text(surface, (menu_loc[0]+25, menu_loc[1]+225), BLACK, FONT_MED, text, cx=False)
            info = (
                ("Depth", "depth"),
                ("Nodes", "nodes"),
                ("Nodes per second", "nps"),
                ("Time", "time"),
                ("Score", "score"),
            )
            for i, (text, key) in enumerate(info):
                if key in self.analysis_info:
                    key_info = self.analysis_info[key]
                    text = text + ": "
                    text += self.nodes_text(key_info) if "Nodes" in text else str(key_info)
                    y = menu_loc[1] + 275 + 25*i
                    centered_text(surface, (menu_loc[0]+25, y), BLACK, FONT_SMALL, text, cx=False)
