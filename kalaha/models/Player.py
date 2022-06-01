from qtpy.QtCore import Slot
from QtPyNetwork.model import Client


class Player(Client):

    def __init__(self, server, id, ip, port):
        super(Player, self).__init__(server, id, ip, port)
        self.base_pit: int = None
        self.allowed_pits: list[int] = None

    @Slot(dict)
    def write(self, message: dict):
        self.server().write(self, message)

    @Slot(dict, list, int)
    def setup_board(self, board, allowed_pits, player_number):
        self.write({"event": "setup_board",
                    "allowed_pits": allowed_pits,
                    "player_number": player_number,
                    "board": board})

    @Slot(int)
    def board_joined(self, id: int):
        self.write({"event": "board_joined", "id": id})

    @Slot(list, bool)
    def available_boards(self, boards: list[dict], can_create: bool):
        self.write({"event": "available_boards", "boards": boards,
                    "can_create": can_create})

    def error(self, message):
        self.write({"event": "error", "error": message})

    @Slot()
    def opponent_not_connected(self):
        self.write({"event": "opponent_not_connected"})

    @Slot()
    def opponent_disconnected(self):
        self.write({"event": "opponent_disconnected"})

    @Slot()
    def opponent_connected(self):
        self.write({"event": "opponent_connected"})

    @Slot(bool, str, int)
    def your_move(self, value, timeout, text=None):
        self.write({"event": "your_move", "value": value, "text": text, "timeout": timeout})

    @Slot(str)
    def invalid_move(self, move):
        self.write({"event": "invalid_move", "error": move})

    @Slot(dict)
    def update_board(self, board):
        self.write({"event": "update_board", "board": board})

    # game results
    @Slot()
    def you_won(self):
        self.write({"event": "you_won"})

    @Slot()
    def you_lost(self):
        self.write({"event": "you_lost"})

    @Slot()
    def you_tied(self):
        self.write({"event": "you_tied"})

    @Slot()
    def board_left(self):
        self.write({"event": "board_left"})

    @Slot()
    def turn_timeout(self):
        self.write({"event": "turn_timeout"})

    @Slot()
    def safe_serialize(self) -> dict:
        return {
            "id": 0,
            "ip": "127.0.0.1",
            "port": 12345,
            "base_pit": self.base_pit,
            "allowed_pits": self.allowed_pits,
        }

    @staticmethod
    def deserialize(data: dict):
        player = Player(None, data["id"], data["ip"], data["port"])
        player.base_pit = data["base_pit"]
        player.allowed_pits = data["allowed_pits"]
        return player
