from qtpy.QtWidgets import (QDialogButtonBox, QMenu, QWidgetAction, QAction)
from qtpy.QtCore import Slot, QTimer, QThread, Signal
from qrainbowstyle.windows import (FramelessWindow, FramelessWarningMessageBox, FramelessInformationMessageBox,
                                   FramelessCriticalMessageBox)
from qrainbowstyle.widgets import StylePickerHorizontal

import logging

from kalaha.models import Board, AutoPlayer
from kalaha.widgets import BoardWidget, InfoWidget, StatusWidget, JoinBoardWidget, CreateBoardWidget


class BoardWindow(FramelessWindow):
    closed = Signal()

    def __init__(self, parent=None):
        super(BoardWindow, self).__init__(parent)
        self.logger = logging.getLogger(self.__class__.__name__)

        self.player_number = 0
        self.auto_player_worker: AutoPlayer = None
        self.auto_player_thread: QThread = None
        self.timeout = 0
        self.board = []

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timer_timeout)

        # windows
        self.message_box = None

        # main widgets
        self.status_widget = StatusWidget(self)
        self.status_widget.set_status("Connecting to server...")
        self.addContentWidget(self.status_widget)

        self.board_widget = BoardWidget(self)
        self.board_widget.hide()
        self.addContentWidget(self.board_widget)

        self.info_widget = InfoWidget(self)
        self.info_widget.hide()
        self.addContentWidget(self.info_widget)

        self.join_widget = JoinBoardWidget(self)
        self.join_widget.create_button.clicked.connect(self.set_board_create_visible)
        self.join_widget.hide()
        self.addContentWidget(self.join_widget)

        self.create_widget = CreateBoardWidget(self)
        self.create_widget.back_button.clicked.connect(self.set_board_create_visible)
        self.create_widget.hide()
        self.addContentWidget(self.create_widget)

        # other widgets
        self.menu = QMenu(self)
        self.style_picker_action = QWidgetAction(self.menu)
        self.style_picker = StylePickerHorizontal(self)
        self.style_picker_action.setDefaultWidget(self.style_picker)

        self.auto_player_action = QAction("Autoplayer", self.menu)
        self.menu.addAction(self.auto_player_action)

        self.menu.addAction(self.style_picker_action)
        self.menu.setTitle("Options")
        self.addMenu(self.menu)

    @Slot(str, int)
    def on_client_connected(self, host: str, port: int):
        self.status_widget.hide()
        self.join_widget.show()
        self.status_widget.set_status("Waiting for opponent...")

    @Slot(str, int)
    def on_failed_to_connect(self, host: str, port: int):
        self.show_info_dialog("Failed to connect!")
        self.status_widget.set_status(f"Failed to connect to {host}:{port}")

    @Slot()
    def on_opponent_connected(self):
        self.create_widget.hide()
        self.join_widget.hide()
        self.status_widget.hide()
        self.board_widget.show()
        self.info_widget.show()

    @Slot()
    def on_opponent_disconnected(self):
        self.timer.stop()
        self.logger.debug("Opponent disconnected!")
        if self.message_box:
            self.message_box.close()
        self.board_widget.setEnabled(False)
        self.message_box = FramelessCriticalMessageBox(self)
        self.message_box.setStandardButtons(QDialogButtonBox.Ok)
        self.message_box.button(QDialogButtonBox.Ok).clicked.connect(self.close)
        self.message_box.setText("Opponent disconnected! Click OK to close.")
        self.message_box.show()

    @Slot()
    def set_board_create_visible(self):
        if self.join_widget.isVisible():
            self.join_widget.hide()
            self.create_widget.show()
        else:
            self.create_widget.hide()
            self.join_widget.show()

    @Slot(int)
    def on_board_joined(self, id: int):
        self.join_widget.hide()
        self.create_widget.hide()
        self.status_widget.show()

    # Board events
    @Slot(Board, list, int)
    def on_setup_board(self, board, allowed_pits, player_number):
        """
        Set up the board and pits
        """
        self.board = board.board
        self.player_number = player_number
        self.info_widget.set_player_number(player_number + 1)
        self.board_widget.setup_board(board, allowed_pits)

    @Slot(Board)
    def on_update_board(self, board: Board):
        """
        Update board widget with new values
        """
        self.board = board.board
        self.board_widget.update_pits(board)

    @Slot(bool, int, str)
    def on_your_move(self, your_move: bool, timeout: int, message: str):
        self.info_widget.set_timeout(timeout)
        self.info_widget.set_player_turn(message)
        if timeout > 0:
            self.timeout = timeout
            self.timer.start(1000)

        if your_move and self.auto_player_action.isChecked():
            self.auto_player_worker.calculate_move.emit(self.board, self.player_number)
        self.show_info_dialog(message)

    @Slot(str)
    def on_invalid_move(self, message: str):
        self.logger.debug(f"Invalid move: {message}")
        if self.message_box:
            self.message_box.close()
        self.message_box = FramelessWarningMessageBox(self)
        self.message_box.setStandardButtons(QDialogButtonBox.Ok)
        self.message_box.button(QDialogButtonBox.Ok).clicked.connect(self.message_box.close)
        self.message_box.setText(message)
        self.message_box.show()

    @Slot(str)
    def on_game_result(self, message):
        self.timer.stop()
        self.info_widget.set_player_turn(message)
        self.auto_player_action.setChecked(False)
        self.show_info_dialog(message)

    @Slot()
    def on_turn_timeout(self):
        if self.auto_player_worker:
            self.auto_player_worker.stop.emit()

    @Slot(bool, int, int, bool, bool)
    def setup_auto_play(self, auto_play: bool, auto_play_delay: int,
                        minimax_depth: int, no_alpha_beta: bool, iterative_deepening: bool):
        self.info_widget.set_auto_play_options(auto_play, minimax_depth, auto_play_delay,
                                               no_alpha_beta, iterative_deepening)
        self.auto_player_action.setChecked(auto_play)

        self.auto_player_worker = AutoPlayer(minimax_depth, auto_play_delay,
                                             no_alpha_beta, iterative_deepening)
        self.auto_player_thread = QThread()
        self.auto_player_thread.moveToThread(QThread.currentThread())
        self.auto_player_worker.moveToThread(self.auto_player_thread)
        self.auto_player_worker.finished.connect(self.auto_player_thread.quit)
        self.auto_player_worker.make_move.connect(self.client.make_move)

        if auto_play:
            self.auto_player_thread.start()
        else:
            self.info_widget.set_auto_play_options_visible(False)

    @Slot()
    def on_timer_timeout(self):
        self.timeout -= 1
        self.info_widget.set_timeout(self.timeout)
        if self.timeout == 0:
            self.timer.stop()

    # Dialogs to show messages
    @Slot(str)
    def show_info_dialog(self, message: str):
        if self.message_box:
            self.message_box.close()
        self.message_box = FramelessInformationMessageBox(self)
        self.message_box.setStandardButtons(QDialogButtonBox.Ok)
        self.message_box.button(QDialogButtonBox.Ok).clicked.connect(self.message_box.close)
        self.message_box.setText(message)
        self.message_box.show()

    @Slot()
    def close(self):
        """
        Close the window and message box if it is open.
        Disconnect from the server and wait for the thread to finish.
        If auto player is running, stop it and wait for the thread to finish.
        """
        if self.message_box is not None:
            self.message_box.close()
        if self.auto_player_thread:
            self.auto_player_thread.quit()
            self.auto_player_thread.wait()
        super().close()
        self.closed.emit()
