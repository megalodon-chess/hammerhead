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

import threading
import pygame
import chess
import chess.engine
from constants import *


class Board:
    def __init__(self):
        self.board = chess.Board()   # Current position
        self.view_board = None       # Current viewed position

        self.move_num = 0            # Current position is startpos with this many moves
        self.flipped = False

        self.thread_id = 0           # Analysis thread ends when this value changes
        self.analysis_info = None

        self.push(chess.Move.from_uci("e2e4"))
        self.push(chess.Move.from_uci("e7e5"))
        self.push(chess.Move.from_uci("g1f3"))
        self.push(chess.Move.from_uci("b8c6"))

    def analyze(self, eng_path):
        thread_id = self.thread_id
        engine = chess.engine.SimpleEngine.popen_uci(eng_path)
        with engine.analysis(self.view_board) as analysis:
            for info in analysis:
                print(info)
                if self.thread_id != thread_id:
                    break

    def set_view(self):
        self.view_board = chess.Board()
        movect = 0
        while movect < self.move_num:
            self.view_board.push(self.board.move_stack[movect])
            movect += 1

    def push(self, move):
        self.thread_id += 1
        if self.move_num == len(self.board.move_stack):
            self.move_num += 1
        self.board.push(move)
        self.set_view()

    def draw(self, events, size):
        sq_size = int(size / 8)
        surf = pygame.Surface((sq_size*8, sq_size*8), pygame.SRCALPHA)
        self.update(events)
        if self.view_board is None:
            self.set_view()

        # Squares
        for x in range(8):
            for y in range(8):
                loc = (x*sq_size, y*sq_size)
                col = BOARD_WHITE if (x+y) % 2 == 0 else BOARD_BLACK
                pygame.draw.rect(surf, col, (*loc, sq_size+1, sq_size+1))

        if len(self.view_board.move_stack) > 0:
            prev_move = self.view_board.move_stack[-1]
            squares = (prev_move.from_square, prev_move.to_square)
            for sq in squares:
                x = sq % 8
                y = 7 - (sq // 8)
                loc = (x*sq_size, y*sq_size)
                col = BOARD_WHITE_SELECT if (x+y) % 2 == 0 else BOARD_BLACK_SELECT
                pygame.draw.rect(surf, col, (*loc, sq_size+1, sq_size+1))

        # Pieces
        for x in range(8):
            for y in range(8):
                loc = (x*sq_size, y*sq_size)
                piece = self.view_board.piece_at(x + 8*(7-y))
                if piece is not None:
                    img = IMAGES[piece.symbol()]
                    img = pygame.transform.scale(img, (sq_size, sq_size))
                    if self.flipped:
                        img = pygame.transform.rotate(img, 180)
                    surf.blit(img, loc)

        if self.flipped:
            surf = pygame.transform.rotate(surf, 180)
        return surf

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.flipped = not self.flipped
                elif event.key == pygame.K_LEFT:
                    self.move_num = max(self.move_num-1, 0)
                    self.set_view()
                elif event.key == pygame.K_RIGHT:
                    self.move_num = min(self.move_num+1, len(self.board.move_stack))
                    self.set_view()
