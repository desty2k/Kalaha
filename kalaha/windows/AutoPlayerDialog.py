from qtpy.QtWidgets import QWidget, QFormLayout

from qrainbowstyle.windows import (FramelessWindow)


class AutoPlayerDialog(FramelessWindow):

    def __init__(self, parent):
        super(AutoPlayerDialog, self).__init__(parent)
        self.content_widget = QWidget(self)
        self.widget_layout = QFormLayout(self.content_widget)
        self.content_widget.setLayout(self.widget_layout)




