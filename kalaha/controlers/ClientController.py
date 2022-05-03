from qtpy.QtCore import QObject, Slot, Qt
from qtpy.QtWidgets import QApplication

from kalaha.windows import BoardWindow
from kalaha.network import KalahaClient


class ClientController(QObject):

    def __init__(self):
        super().__init__()

        self.window = BoardWindow()
        self.client = KalahaClient()
        self.window.closed.connect(self.client.close, Qt.QueuedConnection)
        self.client.closed.connect(QApplication.quit, Qt.QueuedConnection)

        # client server connection events
        self.client.app_error.connect(self.window.show_info_dialog)
        self.client.disconnected.connect(lambda: self.window.show_info_dialog("Connection lost!"))
        self.client.connected.connect(self.window.on_client_connected)
        self.client.failed_to_connect.connect(self.window.on_failed_to_connect)

        # opponent events
        self.client.opponent_connected.connect(self.window.on_opponent_connected)
        self.client.opponent_disconnected.connect(self.window.on_opponent_disconnected)
        self.client.opponent_not_connected.connect(lambda: self.window.show_info_dialog("Opponent not connected!"))

        # board updates
        self.client.board_joined.connect(self.window.on_board_joined)
        self.client.invalid_move.connect(self.window.on_invalid_move)
        self.client.update_board.connect(self.window.on_update_board)
        self.client.setup_board.connect(self.window.on_setup_board)
        self.client.your_move.connect(self.window.on_your_move)
        self.client.turn_timeout.connect(self.window.on_turn_timeout)
        self.window.board_widget.pit_clicked.connect(self.client.make_move)

        # game results
        self.client.you_won.connect(lambda: self.window.on_game_result("You won!"))
        self.client.you_lost.connect(lambda: self.window.on_game_result("You lost!"))
        self.client.you_tied.connect(lambda: self.window.on_game_result("Draw!"))

        # board join/create events
        self.client.available_boards.connect(self.window.join_widget.set_available_boards)
        self.window.join_widget.join_board.connect(self.client.join_board)
        self.window.create_widget.create_board.connect(self.client.create_board)

    @Slot(str, int)
    def start(self, ip: str, port: int):
        self.client.start(ip, port)
        self.window.status_widget.show()
        self.window.show()
