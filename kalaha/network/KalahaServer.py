from QtPyNetwork.server import QBalancedServer
from qtpy.QtCore import Signal, Slot, QObject

import json
import logging

from kalaha.models import Player, Board


class KalahaServer(QBalancedServer):

    def __init__(self, config, parent=None):
        super(KalahaServer, self).__init__(parent)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.set_device_model(Player)
        self.boards = [Board(10, 2, 5, id=-1, pin="1"), Board(20, 3, 100, id=-2)]
        self.config = config
        self.next_board_id = 1

    @Slot(str, int)
    def start(self, ip: str, port: int):
        """Start server."""
        self.logger.info(f"Starting Kalaha server on {ip}:{port}")
        return super(KalahaServer, self).start(ip, port)

    @Slot(Player, Board)
    def create_board(self, player, board):
        """Create a new board and connect player (creator) to it"""
        if self.config.max_boards == len(self.boards):
            player.error(f"Reached limit of available boards ({self.config.max_boards}).")
        else:
            # check if board created by player has valid parameters
            # TODO: pass upper limits as parameters or environment variables
            if not self.config.min_board <= board.board_size <= self.config.max_board:
                player.error(f"Invalid board size (must be between "
                             f"{self.config.min_board} and {self.config.max_board}).")
            elif not self.config.min_stones <= board.stones_count <= self.config.max_stones:
                player.error(f"Invalid number of stones (must be between "
                             f"{self.config.min_stones} and {self.config.max_stones}).")
            elif not self.config.min_timeout <= board.timeout <= self.config.max_timeout:
                player.error(f"Invalid turn timeout (must be between "
                             f"{self.config.min_timeout} and {self.config.max_timeout}).")
            else:
                board.default()
                board.id = self.next_board_id
                self.next_board_id += 1

                board.connect_player(player)
                self.boards.append(board)
                self.logger.debug(f"board {board.id} created (size {board.board_size}, "
                                  f"stones {board.stones_count}, timeout {board.timeout}, pin '{board.pin}')")

    @Slot(Player, str, int)
    def on_connected(self, player: Player, ip: str, port: int):
        """When a player connects, send them the list of boards."""
        player.available_boards([board.safe_serialize() for board in self.boards],
                                self.config.max_boards != len(self.boards))

    @Slot(Player)
    def on_disconnected(self, player: Player) -> None:
        """Check if player was connected to any board.
        If so, notify their opponent and remove board.
        """
        board = self.get_board_by_player(player)
        if board:
            board.timer.stop()
            opponent = board.get_opponent(player)
            if opponent is not None and opponent.is_connected():
                opponent.opponent_disconnected()
            else:
                self.boards.remove(board)
                self.logger.info(f"Board {board.id} removed")

    @Slot(Player, bytes)
    def on_message(self, player: Player, data: bytes) -> None:
        """Handle messages from client."""
        try:
            message = json.loads(data)
            event = message.get("event")
            self.logger.debug(f"P{player.id()}: Received message: {message}")
        except Exception as e:
            self.logger.error(f"P{player.id()}: Failed to deserialize data '{data}': {e}")
            return
        match event:
            case "move":
                board = self.get_board_by_player(player)
                if board is not None:
                    board.make_move(player, message.get("pit_index"))
                else:
                    player.error("You are not connected to any board.")
            case "join_board":
                board = self.get_board_by_player(player)
                if board is not None:
                    player.error(f"Already connected to board {board.id}")
                    return
                id = int(message.get("id"))
                for board in self.boards:
                    if board.id == id:
                        if board.pin is None or board.pin == message.get("pin"):
                            board.connect_player(player)
                        else:
                            player.error("Invalid pin code")
                        return
                player.error(f"Board {id} does not exists")
            case "create_board":
                self.create_board(player, Board.deserialize(message.get("board")))
            case "get_boards":
                player.available_boards([board.safe_serialize() for board in self.boards],
                                        self.max_boards != len(self.boards))

    @Slot(Player)
    def get_board_by_player(self, player: Player) -> Board:
        """Get board by player."""
        for board in self.boards:
            if player is board.player_one or player is board.player_two:
                return board

    @Slot(Player, dict)
    def write(self, player: Player, data: dict):
        """Send data to client."""
        data = json.dumps(data).encode()
        super().write(player, data)

    @Slot(dict)
    def write_all(self, data: dict):
        """Send data to all players."""
        for player in self.get_devices():
            self.write(player, data)
