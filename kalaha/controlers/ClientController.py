from qtpy.QtCore import QObject, Slot, Qt
from qtpy.QtWidgets import QApplication

from kalaha.windows import BoardWindow
from kalaha.network import KalahaClient
from .AutoPlayerController import AutoPlayerController
from .ConnectController import ConnectController


class ClientController(QObject):

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.board_window = BoardWindow()
        # self.connect_window = ConnectDialog(self.board_window)
        self.client = KalahaClient()
        self.board_window.closed.connect(self.close)
        self.client.closed.connect(QApplication.quit)

        # client server connection events
        self.client.app_error.connect(self.board_window.show_info_dialog)
        self.client.disconnected.connect(lambda: self.board_window.show_info_dialog("Connection lost!"))
        # self.client.connected.connect(self.board_window.on_client_connected)
        # self.client.failed_to_connect.connect(self.board_window.on_failed_to_connect)

        # opponent events
        self.client.opponent_connected.connect(self.board_window.on_opponent_connected)
        self.client.opponent_disconnected.connect(self.on_opponent_disconnected)
        self.client.opponent_not_connected.connect(lambda: self.board_window.show_info_dialog("Opponent not connected!"))

        # board updates
        self.client.board_joined.connect(self.board_window.on_board_joined)
        self.client.invalid_move.connect(self.board_window.show_warning_dialog)
        self.client.update_board.connect(self.board_window.board_widget.update_board)
        self.client.setup_board.connect(self.board_window.on_setup_board)
        self.client.your_move.connect(self.on_your_move)
        self.client.timer.timeout.connect(self.on_turn_timer_timeout)
        self.board_window.board_widget.pit_clicked.connect(self.on_pit_clicked)

        # game results
        self.client.you_won.connect(lambda: self.board_window.on_game_result("You won!"))
        self.client.you_lost.connect(lambda: self.board_window.on_game_result("You lost!"))
        self.client.you_tied.connect(lambda: self.board_window.on_game_result("Draw!"))

        # board join/create events
        self.client.available_boards.connect(self.board_window.join_widget.set_available_boards)
        self.board_window.join_widget.join_board.connect(self.client.join_board)
        self.board_window.create_widget.create_board.connect(self.client.create_board)
        self.board_window.join_widget.refresh_button.clicked.connect(self.client.get_boards)

        self.connection_controller = ConnectController(self.config, self.board_window)
        self.connection_controller.window.closeClicked.connect(QApplication.quit)
        self.connection_controller.connect_clicked.connect(self.client.start)
        self.client.connected.connect(self.on_client_connected)
        self.client.failed_to_connect.connect(self.connection_controller.window.on_failed_to_connect)

        self.auto_player_controller = AutoPlayerController(self.config, self.board_window)
        self.auto_player_controller.auto_player_enabled.connect(lambda value: self.on_your_move(value, 0, ""))
        self.auto_player_controller.make_move.connect(self.client.make_move)
        self.auto_player_controller.make_move.connect(lambda pit: self.board_window.board_widget.highlight_pit(False, pit))
        self.auto_player_controller.highlight_pit.connect(self.board_window.board_widget.highlight_pit)
        self.board_window.auto_player_action.triggered.connect(self.auto_player_controller.window.show)

    @Slot(bool, int, str)
    def on_your_move(self, your_move: bool, turn_timeout: int, message: str):
        if turn_timeout > 0:
            self.client.timeout = turn_timeout
            self.client.timer.start(1000)
        if self.auto_player_controller.auto_player is not None:
            if self.client.my_move:
                self.auto_player_controller.auto_player.calculate_move(self.client.board, self.client.player_number)
        else:
            self.board_window.on_your_move(your_move, turn_timeout, message)

    @Slot()
    def on_turn_timer_timeout(self):
        self.client.timeout -= 1
        self.board_window.info_widget.set_timeout(self.client.timeout)
        if self.client.timeout == 0:
            self.client.timer.stop()

    @Slot()
    def on_opponent_disconnected(self):
        self.client.get_boards()
        self.board_window.on_opponent_disconnected()

    @Slot(int)
    def on_pit_clicked(self, pit_id: int):
        if self.auto_player_controller.auto_player is not None:
            self.board_window.show_info_dialog("Auto player is active!")
        else:
            self.client.make_move(pit_id)

    @Slot(str, int)
    def on_client_connected(self, ip: str, port: int):
        # self.board_window.on_client_connected(ip, port)
        self.connection_controller.window.hide()
        self.board_window.join_widget.show()
        self.board_window.show()

    @Slot(str, int)
    def start(self, ip: str, port: int):
        # self.client.start(ip, port)
        self.connection_controller.window.show()
        # self.board_window.status_widget.show()
        # self.board_window.show()

    @Slot()
    def close(self):
        self.connection_controller.window.close()
        self.auto_player_controller.window.close()
        self.client.close()
