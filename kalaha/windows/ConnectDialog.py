from qtpy.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QSpinBox
from qtpy.QtCore import Slot

from qrainbowstyle.windows import FramelessWindow
from qrainbowstyle.widgets import WaitingSpinner


class ConnectDialog(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.widget = QWidget(self)
        self.widget_layout = QFormLayout(self.widget)
        self.widget.setLayout(self.widget_layout)
        self.addContentWidget(self.widget)

        self.server_address_edit = QLineEdit(self.widget)
        self.widget_layout.addRow("Address", self.server_address_edit)

        self.server_port_edit = QSpinBox(self.widget)
        self.server_port_edit.setRange(1, 65535)
        self.widget_layout.addRow("Port", self.server_port_edit)

        self.connect_button = QPushButton("Connect")
        self.widget_layout.addRow(self.connect_button)

        self.exit_button = QPushButton("Exit")
        self.widget_layout.addRow(self.exit_button)

        self.spinner = WaitingSpinner(self, centerOnParent=True,
                                      roundness=70.0,
                                      fade=70.0, radius=50.0, lines=12,
                                      line_length=20.0, line_width=5.0)
        self.widget_layout.addWidget(self.spinner)

    @Slot(str, int)
    def on_failed_to_connect(self, host: str, port: int):
        self.spinner.start()

