from qtpy.QtWidgets import QWidget, QHBoxLayout, QLabel, QLCDNumber, QSizePolicy, QSpacerItem, QPushButton
from qtpy.QtCore import Slot, Qt


class InfoWidget(QWidget):
    def __init__(self, parent):
        super(InfoWidget, self).__init__(parent)
        font = self.font()
        font.setPointSize(11)

        self.widget_layout = QHBoxLayout(self)
        self.setLayout(self.widget_layout)
        self.widget_layout.setContentsMargins(25, 11, 25, 25)

        self.lcd_widget = QLCDNumber(self)
        self.lcd_widget.setDigitCount(2)
        self.lcd_widget.display(0)
        self.widget_layout.addWidget(self.lcd_widget)

        self.turn_label = QLabel(self)
        self.turn_label.setFont(font)
        self.turn_label.setText("Waiting for opponent...")
        self.turn_label.setAlignment(Qt.AlignCenter)
        self.widget_layout.addWidget(self.turn_label)

        self.spacer_right = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.widget_layout.addItem(self.spacer_right)

        self.leave_button = QPushButton("Leave", self)
        self.leave_button.setMinimumSize(100, 50)
        font = self.leave_button.font()
        font.setPointSize(11)
        self.leave_button.setFont(font)
        self.widget_layout.addWidget(self.leave_button)

    @Slot(str)
    def set_player_turn(self, message: str):
        self.turn_label.setText(message)

    @Slot(int)
    def set_timeout(self, time: int):
        self.lcd_widget.display(time)
