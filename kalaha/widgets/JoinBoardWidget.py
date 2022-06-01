from qtpy.QtWidgets import QWidget, QLabel, QPushButton, QFormLayout, QComboBox, QLineEdit, QStyle
from qtpy.QtCore import Slot, Signal

from kalaha.models import Board
from .CenteredFrameWidget import CenteredFrameWidget


class JoinBoardWidget(CenteredFrameWidget):
    join_board = Signal(Board, str)

    def __init__(self, parent):
        super().__init__(parent)
        self.boards = []
        self.widget = QWidget(self)
        self.widget_layout = QFormLayout(self.widget)
        self.widget.setLayout(self.widget_layout)
        self.set_center_widget(self.widget)

        self.join_label = QLabel("Select board", self)
        self.widget_layout.addRow(self.join_label)

        self.boards_combo = QComboBox(self)
        self.widget_layout.addRow(self.boards_combo)

        self.pin_edit = QLineEdit(self)
        self.widget_layout.addRow("Pin", self.pin_edit)

        self.refresh_button = QPushButton("Refresh", self)
        self.widget_layout.addRow(self.refresh_button)

        self.join_button = QPushButton("Join", self)
        self.join_button.clicked.connect(self.on_join_button_clicked)
        self.widget_layout.addRow(self.join_button)

        self.create_button = QPushButton("Create board", self)
        self.widget_layout.addRow(self.create_button)

    @Slot(list, bool)
    def set_available_boards(self, boards: list[Board], can_create: bool):
        self.create_button.setEnabled(can_create)
        self.boards_combo.clear()
        self.boards = boards
        for board in self.boards:
            player_count = len([p for p in [board.player_one, board.player_two] if p is not None])
            pixmap = QStyle.SP_DialogNoButton if player_count == 2 else QStyle.SP_DialogYesButton
            icon = self.style().standardIcon(pixmap)
            self.boards_combo.addItem(icon, f"{player_count}/2 - ID {board.id} - size {board.board_size} - "
                                            f"stones {board.stones_count} - {'Secured' if board.pin else 'Unsecured'}",
                                      board)

    @Slot()
    def on_join_button_clicked(self):
        board: Board = self.boards_combo.currentData()
        self.join_board.emit(board, self.pin_edit.text())

    @Slot(int)
    def on_board_selection_changed(self, index: int):
        board: Board = self.boards_combo.itemData(index)
        self.pin_edit.setEnabled(board.pin is True)
