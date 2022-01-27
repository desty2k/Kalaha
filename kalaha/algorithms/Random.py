from qtpy.QtCore import Slot

from kalaha.models import Algorithm, Node

import random


class Random(Algorithm):
    description = "Chose random, not empty pit"

    def __init__(self):
        super(Random, self).__init__()

    @Slot(list, int)
    def run(self, board: list[int], maximizing_player: int) -> None:
        node = Node(board, maximizing_player)
        index = random.choice([i for i in node.player_ranges[maximizing_player] if board[i] > 0])
        return index

    @Slot()
    def stop(self) -> None:
        return None

    @Slot()
    def is_available(self):
        return True
