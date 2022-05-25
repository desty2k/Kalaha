from qtpy.QtCore import QObject, Signal, Slot

from kalaha.windows import ConnectDialog


class ConnectController(QObject):
    connect_clicked = Signal(str, int)

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config

        self.window = ConnectDialog(parent)
        self.window.server_address_edit.setText(self.config.host)
        self.window.server_port_edit.setValue(self.config.port)
        self.window.connect_button.clicked.connect(self.on_connect_button_clicked)

    @Slot()
    def on_connect_button_clicked(self):
        host = self.window.server_address_edit.text()
        port = self.window.server_port_edit.value()
        self.window.spinner.start()
        self.connect_clicked.emit(host, port)

    # @Slot(str, int)
    # def on_failed_to_connect(self, host: str, port: int):
    #     self.window.spinner.stop()

        # self.show_info_dialog("Failed to connect!")


