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

    @Slot(Board)
    def update_board(self, board: Board):
        self.reset_style_sheets()
        for pit in self.pits:
            pit.setText(str(board.board[pit.index]))

    @Slot(Board, Player)
    def setup_board(self, board: Board, player: Player):
        self.clear_board()

        opponent = board.get_opponent(player)
        # in loop add pits
        for i in player.allowed_pits:
            pit = PlayerPitButton(i, self)
            self.pits.append(pit)
            self.player_one_pits_layout.addWidget(pit)
        # add base
        self.player_one_base = PlayerBaseButton(player.base_pit, self)
        self.pits.append(self.player_one_base)

        # add opponent pits
        for i in opponent.allowed_pits[::-1]:
            pit = OpponentPitButton(i, self)
            self.pits.append(pit)
            self.player_two_pits_layout.addWidget(pit)
        # add opponent base
        self.player_two_base = OpponentBaseButton(opponent.base_pit, self)
        self.pits.append(self.player_two_base)

        for pit in self.pits:
            pit.clicked.connect(self.on_pit_clicked)

        self.update_board(board)
        self.logger.debug(f"Board setup done. Pits indexes are: {[pit.index for pit in self.pits]}")

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
