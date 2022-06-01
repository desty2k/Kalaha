from qtpy.QtWidgets import QLineEdit, QFormLayout, QSpinBox, QPushButton, QWidget, QDialogButtonBox, QSpacerItem, QSizePolicy
from qtpy.QtCore import Slot, Signal, Qt
from qrainbowstyle.widgets import WaitingSpinner
from qrainbowstyle.windows import FramelessCriticalMessageBox

from .CenteredFrameWidget import CenteredFrameWidget


class ConnectServerWidget(CenteredFrameWidget):
    connect_clicked = Signal(str, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.message_box = None
        self.widget = QWidget(self)
        self.widget_layout = QFormLayout(self.widget)
        self.widget.setLayout(self.widget_layout)
        self.set_center_widget(self.widget)

        self.server_address_edit = QLineEdit(self.widget)
        self.widget_layout.addRow("Address", self.server_address_edit)

        self.server_port_edit = QSpinBox(self.widget)
        self.server_port_edit.setRange(1, 65535)
        self.widget_layout.addRow("Port", self.server_port_edit)

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.on_connect_button_clicked)
        self.widget_layout.addRow(self.connect_button)

        self.exit_button = QPushButton("Exit")
        self.widget_layout.addRow(self.exit_button)

        self.spinner = WaitingSpinner(self, centerOnParent=True, disableParentWhenSpinning=True,
                                      modality=Qt.WindowModality.WindowModal, roundness=70.0,
                                      fade=70.0, radius=50.0, lines=12,
                                      line_length=20.0, line_width=5.0)

    @Slot(str, int)
    def set_ip_port(self, ip: str, port: int):
        self.server_address_edit.setText(ip)
        self.server_port_edit.setValue(port)

    @Slot()
    def on_connect_button_clicked(self):
        if self.message_box is not None:
            self.message_box.close()
        self.connect_clicked.emit(self.server_address_edit.text(),
                                  self.server_port_edit.value())
        self.spinner.start()

    @Slot()
    def on_failed_to_connect(self):
        self.spinner.stop()
        self.message_box = FramelessCriticalMessageBox(self)
        self.message_box.setText("Failed to connect to server")
        self.message_box.setStandardButtons(QDialogButtonBox.Ok)
        self.message_box.button(QDialogButtonBox.Ok).clicked.connect(self.message_box.close)
        self.message_box.show()
