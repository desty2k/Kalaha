from qtpy.QtWidgets import QWidget, QLineEdit, QPushButton, QFormLayout, QSpinBox, QLabel
from qtpy.QtCore import Slot, Signal

from kalaha.models import Board


class CreateBoardWidget(QWidget):
    create_board = Signal(Board)

    def __init__(self, parent):
        super().__init__(parent)
        self.widget_layout = QFormLayout(self)
        self.setLayout(self.widget_layout)

        self.create_label = QLabel("Board", self)
        self.widget_layout.addRow(self.create_label)

        self.pits_count_edit = QSpinBox(self)
        self.pits_count_edit.setRange(1, 100)
        self.pits_count_edit.setValue(6)
        self.pits_count_edit.setToolTip("Number of pits for each player (excluding the base)")
        self.widget_layout.addRow("Pits", self.pits_count_edit)

        self.stones_count_edit = QSpinBox(self)
        self.stones_count_edit.setRange(1, 100)
        self.stones_count_edit.setValue(5)
        self.stones_count_edit.setToolTip("Number of stones in each pit")
        self.widget_layout.addRow("Stones", self.stones_count_edit)

        self.turn_timeout_edit = QSpinBox(self)
        self.turn_timeout_edit.setRange(0, 99)
        self.turn_timeout_edit.setSuffix("s")
        self.turn_timeout_edit.setToolTip("Time in seconds, 0 means no timeout")
        self.widget_layout.addRow("Timeout", self.turn_timeout_edit)

        self.pin_edit = QLineEdit(self)
        self.pin_edit.setToolTip("Pin to use for the game, leave empty to create open game")
        self.widget_layout.addRow("Pin", self.pin_edit)

        self.create_button = QPushButton("Create", self)
        self.create_button.clicked.connect(self.on_board_create_clicked)
        self.widget_layout.addRow(self.create_button)

        self.back_button = QPushButton("Back", self)
        self.widget_layout.addRow(self.back_button)

    @Slot()
    def on_board_create_clicked(self):
        board = Board(self.pits_count_edit.value(), self.stones_count_edit.value(),
                      timeout=self.turn_timeout_edit.value(), pin=self.pin_edit.text())
        self.create_board.emit(board)
