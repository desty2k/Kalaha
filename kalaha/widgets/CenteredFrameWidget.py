from qtpy.QtCore import Slot, Qt
from qtpy.QtWidgets import QWidget, QGridLayout, QSpacerItem, QSizePolicy, QVBoxLayout, QFrame

from qrainbowstyle import getCurrentPalette

import string

FRAME_STYLESHEET = string.Template(
    """
FrameWidget {
    border-width: 2px;
    border-radius: 3px;
    border-color: $COLOR_ACCENT_3;
}
"""
)


class FrameWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet(FRAME_STYLESHEET.substitute(COLOR_ACCENT_3=getCurrentPalette().COLOR_ACCENT_3))


class CenteredFrameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)
        self.grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding), 2, 1, 1, 1)
        self.grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 2, 1, 1)
        self.grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 0, 1, 1)
        self.grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding), 0, 1, 1, 1)

        self.framed_widget = FrameWidget(self)
        self.framed_widget_layout = QVBoxLayout(self.framed_widget)
        self.framed_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.framed_widget_layout.setSpacing(0)

        self.grid_layout.addWidget(self.framed_widget, 1, 1, 1, 1)

    @Slot(QWidget)
    def set_center_widget(self, widget):
        self.framed_widget_layout.addWidget(widget)
