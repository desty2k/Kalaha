from qtpy.QtCore import Slot, Signal
from QtPyNetwork.client import QThreadedClient

from kalaha.models import Board

import json
import logging


class KalahaClient(QThreadedClient):
    # board changing / errors signals
    app_error = Signal(str)
    available_boards = Signal(list, bool)
    invalid_move = Signal(str)
    your_move = Signal(bool, int, str)
    board_joined = Signal(int)
    setup_board = Signal(Board, list, int)
    update_board = Signal(Board)
    turn_timeout = Signal()

    # oponent status
    opponent_connected = Signal()
    opponent_disconnected = Signal()
    opponent_not_connected = Signal()

    # game result
    you_won = Signal()
    you_lost = Signal()
    you_tied = Signal()

    def __init__(self):
        super(KalahaClient, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    @Slot(bytes)
    def on_message(self, data: bytes):
        """Handle messages from server"""
        try:
            message = json.loads(data)
            event = message.get("event")
            self.logger.debug("Received message: {}".format(message))
        except Exception as e:
            self.logger.error(f"Failed to deserialize data '{data}': {e}")
            return

        match event:
            case "error":
                self.app_error.emit(message.get("error"))
            case "invalid_move":
                self.invalid_move.emit(message.get("error"))
            case "turn_timeout":
                self.turn_timeout.emit()
            case "your_move":
                self.your_move.emit(message.get("value"), message.get("timeout"), message.get("text"))
            case "available_boards":
                self.available_boards.emit([Board.deserialize(board) for board in message.get("boards")],
                                           message.get("can_create"))
            case "board_joined":
                self.board_joined.emit(int(message.get("id")))
            case "setup_board":
                self.setup_board.emit(Board.deserialize(message.get("board")), message.get("allowed_pits_range"),
                                      message.get("player_number"))
            case "update_board":
                board = Board.deserialize(message.get("board"))
                self.update_board.emit(board)
            case "you_won":
                self.you_won.emit()
            case "you_lost":
                self.you_lost.emit()
            case "you_tied":
                self.you_tied.emit()
            case "opponent_connected":
                self.opponent_connected.emit()
            case "opponent_disconnected":
                self.opponent_disconnected.emit()
            case "opponent_not_connected":
                self.opponent_not_connected.emit()
            case _:
                pass

    @Slot(dict)
    def write(self, message: dict):
        """Write message to server"""
        data = json.dumps(message).encode()
        super().write(data)

    @Slot(int)
    def make_move(self, pit_index: int):
        """Send index of pit from which to move stones"""
        self.write({"event": "move", "pit_index": pit_index})

    @Slot(Board, str)
    def join_board(self, board: Board, pin: str):
        """Join board with given pin"""
        self.write({"event": "join_board", "id": board.id, "pin": pin})

    @Slot(Board)
    def create_board(self, board: Board):
        """Create new board"""
        self.write({"event": "create_board", "board": board.serialize()})

    @Slot()
    def get_boards(self):
        """Get list of available boards"""
        self.write({"event": "get_boards"})
