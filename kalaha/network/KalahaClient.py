from qtpy.QtCore import Slot, Signal, QTimer
from QtPyNetwork.client import TCPClient

from kalaha.models import Board, Player

import json
import logging


class KalahaClient(TCPClient):
    # board changing / errors signals
    app_error = Signal(str)
    available_boards = Signal(list, bool)
    invalid_move = Signal(str)
    your_move = Signal(bool, int, str)
    board_joined = Signal(int)
    board_left = Signal()
    setup_board = Signal(Board, Player)
    update_board = Signal(Board)
    turn_timeout = Signal()

    # oponent status
    opponent_connected = Signal()
    opponent_disconnected = Signal()
    opponent_not_connected = Signal()

    # game result
    game_result = Signal(str)

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

        self.my_move: bool = False
        self.board: Board = None
        self.player: int = None

        self.timer = QTimer()
        self.timeout = 0

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
                value = message.get("value")
                timeout = message.get("timeout")
                self.my_move = value
                self.timeout = timeout
                self.your_move.emit(value, timeout, message.get("text"))
            case "available_boards":
                self.available_boards.emit([Board.deserialize(board) for board in message.get("boards")],
                                           message.get("can_create"))
            case "board_joined":
                self.board_joined.emit(int(message.get("id")))
            case "board_left":
                self.board_left.emit()
            case "setup_board":
                board = Board.deserialize(message.get("board"))
                player_number = message.get("player_number")
                player = board.player_one if player_number == 0 else board.player_two
                self.player = player_number
                self.board = board
                self.setup_board.emit(board, player)
            case "update_board":
                board = Board.deserialize(message.get("board"))
                self.board = board
                self.update_board.emit(board)
            case "you_won":
                self.timer.stop()
                self.get_boards()
                self.game_result.emit("You won!")
            case "you_lost":
                self.timer.stop()
                self.get_boards()
                self.game_result.emit("You lost!")
            case "you_tied":
                self.timer.stop()
                self.get_boards()
                self.game_result.emit("You tied!")
            case "opponent_connected":
                self.opponent_connected.emit()
            case "opponent_disconnected":
                self.timer.stop()
                self.board = None
                self.player = None
                self.get_boards()
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

    @Slot()
    def leave_board(self):
        """Leave current board"""
        self.write({"event": "leave_board"})
