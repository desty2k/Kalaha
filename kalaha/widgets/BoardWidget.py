from qtpy.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from qtpy.QtCore import Signal, Slot

import logging

from kalaha.models import Board, Player
from kalaha.stylesheets import *
from kalaha.widgets.PitButtons import (PlayerPitButton, PlayerBaseButton,
                                       OpponentBaseButton, OpponentPitButton, PitButton)


class BoardWidget(QWidget):
    pit_clicked = Signal(int)

    def __init__(self, parent):
        super(BoardWidget, self).__init__(parent)
        self.logger = logging.getLogger(self.__class__.__name__)

        self.pits: list[PitButton] = []
        self.player_one_base = None
        self.player_two_base = None

        self.widget_layout = QHBoxLayout(self)
        self.widget_layout.setContentsMargins(25, 25, 25, 0)
        self.setLayout(self.widget_layout)

        self.pits_widget = QWidget(self)
        self.pits_layout = QVBoxLayout(self.pits_widget)
        self.pits_layout.setContentsMargins(11, 0, 11, 0)
        self.pits_widget.setLayout(self.pits_layout)

        self.player_one_pits_widget = QWidget(self.pits_widget)
        self.player_one_pits_layout = QHBoxLayout(self.player_one_pits_widget)
        self.player_one_pits_layout.setContentsMargins(11, 11, 11, 0)
        self.player_one_pits_widget.setLayout(self.player_one_pits_layout)

        self.player_two_pits_widget = QWidget(self.pits_widget)
        self.player_two_pits_layout = QHBoxLayout(self.player_two_pits_widget)
        self.player_two_pits_layout.setContentsMargins(11, 0, 11, 11)
        self.player_two_pits_widget.setLayout(self.player_two_pits_layout)

        self.pits_layout.addWidget(self.player_two_pits_widget)
        self.pits_layout.addWidget(self.player_one_pits_widget)

    @Slot()
    def clear_board(self):
        """Removes all pits from the board."""
        for pit in self.pits:
            pit.setParent(None)
            pit.deleteLater()
        self.pits = []

    # @Slot(int)
    # def set_board_size(self, size: int):
    #     """Generates new board with the given size."""
    #     self.clear_board()
    #     for i in range(size):
    #         pit = PitButton(i, self.player_one_pits_widget)
    #         self.pits.append(pit)
    #         self.player_one_pits_layout.addWidget(pit)
    #
    #     self.player_one_base = BaseButton(size, self)
    #     self.pits.append(self.player_one_base)
    #
    #     for i in range(size):
    #         pit = PitButton(size + i + 1, self.player_two_pits_widget)
    #         self.pits.append(pit)
    #         self.player_two_pits_layout.insertWidget(0, pit)
    #
    #     self.player_two_base = BaseButton(size + size + 1, self)
    #     self.pits.append(self.player_two_base)
    #
    #     self.widget_layout.addWidget(self.player_two_base)
    #     self.widget_layout.addWidget(self.pits_widget)
    #     self.widget_layout.addWidget(self.player_one_base)

    # @Slot(Board, list)
    # def setup_board(self, board: Board, allowed_pits: list[int]):
    #     """Sets up the board with the given board model."""
    #     self.set_board(board)
    #     for pit_index in allowed_pits:
    #         self.pits[pit_index].setStyleSheet(PLAYER_PIT_STYLESHEET)
    #     self.pits[max(allowed_pits) + 1].setStyleSheet(PLAYER_BASE_STYLESHEET)

    # @Slot(Board)
    # def set_board(self, board: Board):
    #     self.logger.debug(f"Setting board: {board.board}")
    #     if len(self.pits) != 0 and len(board.board) != len(self.pits):
    #         raise ValueError("Pit count does not match")
    #     else:
    #         self.set_board_size(board.board_size)
    #         self.update_board(board)
    #         self.logger.debug(f"Done! Pits indexes are: {[pit.index for pit in self.pits]}")
    #         for pit in self.pits:
    #             pit.clicked.connect(self.on_pit_clicked)

    @Slot(Board)
    def update_board(self, board: Board):
        self.reset_style_sheets()
        for pit in self.pits:
            pit.setText(str(board.board[pit.index]))

        # for i in range(len(board.board)):
        #     self.pits[i].setText(str(board.board[i]))

    @Slot(Board, Player)
    def setup_board(self, board: Board, player: Player):
        self.clear_board()
        # add pits
        for i in player.allowed_pits:
            pit = PlayerPitButton(i, self)
            self.pits.append(pit)
            self.player_one_pits_layout.addWidget(pit)
        # add base
        self.player_one_base = PlayerBaseButton(player.base_pit, self)
        self.pits.append(self.player_one_base)
        self.player_one_pits_layout.addWidget(self.player_one_base)
        # add opponent pits
        opponent = board.get_opponent(player)
        for i in opponent.allowed_pits:
            pit = OpponentPitButton(i, self)
            self.pits.append(pit)
            self.player_two_pits_layout.addWidget(pit)
        # add opponent base
        self.player_two_base = OpponentBaseButton(opponent.base_pit, self)
        self.pits.append(self.player_two_base)
        self.player_two_pits_layout.addWidget(self.player_two_base)
        self.update_board(board)
        self.logger.debug(f"Done! Pits indexes are: {[pit.index for pit in self.pits]}")
        for pit in self.pits:
            pit.clicked.connect(self.on_pit_clicked)

        self.widget_layout.addWidget(self.player_two_base)
        self.widget_layout.addWidget(self.pits_widget)
        self.widget_layout.addWidget(self.player_one_base)

    @Slot()
    def reset_style_sheets(self):
        for pit in self.pits:
            pit.reset_stylesheet()

    @Slot()
    def on_pit_clicked(self):
        pit: PitButton = self.sender()
        self.pit_clicked.emit(pit.index)

    @Slot(bool, int)
    def highlight_pit(self, value: bool, pit_index: int):
        for pit in self.pits:
            if pit.index == pit_index:
                pit.setStyleSheet(HIGHLIGHTED_PIT_STYLESHEET if value else PLAYER_PIT_STYLESHEET)
