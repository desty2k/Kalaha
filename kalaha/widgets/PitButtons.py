from qtpy.QtCore import Slot
from qtpy.QtWidgets import QPushButton, QSizePolicy
from kalaha.stylesheets import *


class PitButton(QPushButton):

    def __init__(self, index, parent):
        super(PitButton, self).__init__(parent)
        self.index = index
        self.initial_stylesheet = None
        font = self.font()
        font.setPointSize(20)
        self.setFont(font)
        sizepolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.setSizePolicy(sizepolicy)

    @Slot(str)
    def setStyleSheet(self, style_sheet: str) -> None:
        if self.initial_stylesheet is None:
            self.initial_stylesheet = style_sheet
        super(PitButton, self).setStyleSheet(style_sheet)

    @Slot()
    def reset_stylesheet(self):
        self.setStyleSheet(self.initial_stylesheet)


class BaseButton(PitButton):

    def __init__(self, index, parent):
        super(BaseButton, self).__init__(index, parent)
        self.setMaximumWidth(300)


class PlayerPitButton(PitButton):

    def __init__(self, index, parent):
        super(PlayerPitButton, self).__init__(index, parent)
        self.setStyleSheet(PLAYER_PIT_STYLESHEET)


class PlayerBaseButton(BaseButton):

    def __init__(self, index, parent):
        super(PlayerBaseButton, self).__init__(index, parent)
        self.setStyleSheet(PLAYER_BASE_STYLESHEET)


class OpponentPitButton(PitButton):

    def __init__(self, index, parent):
        super(OpponentPitButton, self).__init__(index, parent)
        self.setStyleSheet(OPPONENT_PIT_STYLESHEET)


class OpponentBaseButton(BaseButton):

    def __init__(self, index, parent):
        super(OpponentBaseButton, self).__init__(index, parent)
        self.setStyleSheet(OPPONENT_BASE_STYLESHEET)
