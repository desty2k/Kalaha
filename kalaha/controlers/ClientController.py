from qtpy.QtCore import QObject, Slot, Qt
from qtpy.QtWidgets import QApplication

from kalaha.windows import BoardWindow
from kalaha.network import KalahaClient
from .AutoPlayerController import AutoPlayerController


class ClientController(QObject):

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.board_window = BoardWindow()
        self.client = KalahaClient()
        self.board_window.closed.connect(self.close)
        self.client.closed.connect(QApplication.quit)

        # opponent events
        self.client.opponent_connected.connect(self.board_window.on_opponent_connected)
        self.client.opponent_disconnected.connect(lambda: self.board_window.
                                                  show_leave_board_messagebox("Opponent disconnected!"))
        self.client.opponent_not_connected.connect(lambda: self.board_window.how_info_dialog("Opponent not connected!"))

        # board updates
        self.client.board_joined.connect(self.board_window.on_board_joined)
        self.client.board_left.connect(lambda: self.board_window.show_leave_board_messagebox("You left the board!"))
        self.client.invalid_move.connect(self.board_window.show_warning_dialog)
        self.client.update_board.connect(self.board_window.board_widget.update_board)
        self.client.setup_board.connect(self.board_window.on_setup_board)
        self.client.your_move.connect(self.on_your_move)
        self.client.timer.timeout.connect(self.on_turn_timer_timeout)
        self.board_window.board_widget.pit_clicked.connect(self.on_pit_clicked)

        # game results
        self.client.game_result.connect(self.board_window.show_leave_board_messagebox)

        # board join/leave/create events
        self.client.available_boards.connect(self.board_window.join_widget.set_available_boards)
        self.board_window.join_widget.join_board.connect(self.client.join_board)
        self.board_window.create_widget.create_board.connect(self.client.create_board)
        self.board_window.join_widget.refresh_button.clicked.connect(self.client.get_boards)
        self.board_window.info_widget.leave_button.clicked.connect(self.client.leave_board)

        # connecting to server
        self.board_window.connect_widget.connect_clicked.connect(self.client.start)
        self.board_window.connect_widget.exit_button.clicked.connect(self.close)
        self.client.connected.connect(self.on_client_connected)
        self.client.app_error.connect(self.board_window.show_info_dialog)
        self.client.disconnected.connect(self.board_window.on_client_disconnected)
        self.client.failed_to_connect.connect(self.board_window.connect_widget.on_failed_to_connect)

        # auto player
        self.auto_player_controller = AutoPlayerController(self.config, self.board_window)
        self.auto_player_controller.auto_player_enabled.connect(self.on_auto_player_enabled)
        self.auto_player_controller.make_move.connect(self.client.make_move)
        self.auto_player_controller.highlight_pit.connect(self.board_window.board_widget.highlight_pit)
        self.board_window.auto_player_action.triggered.connect(self.auto_player_controller.window.show)

    @Slot(bool)
    def on_auto_player_enabled(self, value):
        if value and self.client.my_move:
            self.auto_player_controller.auto_player.calculate_move(self.client.board, self.client.player)

    @Slot(bool, int, str)
    def on_your_move(self, your_move: bool, turn_timeout: int, message: str):
        if turn_timeout > 0:
            self.client.timeout = turn_timeout
            self.client.timer.start(1000)
        if self.auto_player_controller.is_auto_player_enabled() and self.client.my_move:
            self.auto_player_controller.auto_player.calculate_move(self.client.board, self.client.player)
        self.board_window.on_your_move(your_move, turn_timeout, message)

    @Slot()
    def on_turn_timer_timeout(self):
        self.client.timeout -= 1
        self.board_window.info_widget.set_timeout(self.client.timeout)
        if self.client.timeout == 0:
            self.client.timer.stop()

    @Slot(int)
    def on_pit_clicked(self, pit_id: int):
        if self.auto_player_controller.is_auto_move_enabled():
            self.board_window.show_info_dialog("Auto move is active!")
        else:
            self.client.make_move(pit_id)

    @Slot(str, int)
    def on_client_connected(self, ip: str, port: int):
        self.board_window.connect_widget.hide()
        self.board_window.join_widget.show()
        self.board_window.show()

    @Slot(str, int)
    def start(self, ip: str, port: int):
        self.board_window.connect_widget.set_ip_port(ip, port)
        self.board_window.connect_widget.show()
        self.board_window.show()

    @Slot()
    def close(self):
        self.auto_player_controller.window.close()
        self.client.close()
