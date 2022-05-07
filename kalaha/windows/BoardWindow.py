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
        self.board_widget.setEnabled(True)
        self.board_widget.show()
        self.info_widget.show()

    @Slot()
    def on_opponent_disconnected(self):
        if self.message_box:
            self.message_box.close()
        self.board_widget.setEnabled(False)
        self.message_box = FramelessCriticalMessageBox(self)
        self.message_box.setStandardButtons(QDialogButtonBox.Ok)
        self.message_box.button(QDialogButtonBox.Ok).clicked.connect(self.message_box.close)
        self.message_box.button(QDialogButtonBox.Ok).clicked.connect(self.board_widget.hide)
        self.message_box.button(QDialogButtonBox.Ok).clicked.connect(self.info_widget.hide)
        self.message_box.button(QDialogButtonBox.Ok).clicked.connect(self.join_widget.show)
        self.message_box.setText("Opponent disconnected! Click OK to return to menu.")
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
        self.info_widget.set_player_number(player_number + 1)
        self.board_widget.setup_board(board, allowed_pits)

    @Slot(bool, int, str)
    def on_your_move(self, your_move: bool, timeout: int, message: str):
        self.info_widget.set_timeout(timeout)
        self.info_widget.set_player_turn(message)
        self.show_info_dialog(message)

    @Slot(str)
    def on_game_result(self, message):
        self.info_widget.set_player_turn(message)
        self.auto_player_action.setChecked(False)
        self.show_info_dialog(message)

    # Dialogs to show messages
    @Slot(str)
    def show_info_dialog(self, message: str):
        self.logger.debug("Info dialog: " + message)
        if self.message_box:
            self.message_box.close()
        self.message_box = FramelessInformationMessageBox(self)
        self.message_box.setStandardButtons(QDialogButtonBox.Ok)
        self.message_box.button(QDialogButtonBox.Ok).clicked.connect(self.message_box.close)
        self.message_box.setText(message)
        self.message_box.show()

    @Slot(str)
    def show_warning_dialog(self, message: str):
        self.logger.debug("Warning dialog: " + message)
        if self.message_box:
            self.message_box.close()
        self.message_box = FramelessWarningMessageBox(self)
        self.message_box.setStandardButtons(QDialogButtonBox.Ok)
        self.message_box.button(QDialogButtonBox.Ok).clicked.connect(self.message_box.close)
        self.message_box.setText(message)
        self.message_box.show()

    @Slot()
    def close(self):
        if self.message_box is not None:
            self.message_box.close()
        super().close()
        self.closed.emit()
