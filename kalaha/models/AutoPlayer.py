"""
This module contains the AutoPlayer class.
Object is instantiated once per game and it is kept in separate thread.
When it is player turn, client emits calculate_move signal,
what makes AutoPlayer calculate the best move and send it to the main thread
using make_move signal.
"""

from qtpy.QtCore import QObject, Slot, Signal, QThread, QDateTime

import random
import logging

_CMINIMAX_IMPORTED = True
try:
    import CMinimax

    logging.debug("Using C++ AutoPlayer")
except ImportError:
    _CMINIMAX_IMPORTED = False
    logging.debug("Using Python AutoPlayer")


class Node:
    def __init__(self, board: list[int], player):
        super(Node, self).__init__()
        self.board = board
        self.player = player
        self.game_over = False
        self.children: dict[int, Node] = {}
        self.player_ranges = (range(0, len(board) // 2 - 1), range(len(board) // 2, len(board) - 1))
    __slots__ = ("board", "player", "player_ranges", "game_over", "children")


# methods are outside of the class to reduce
def copy(self) -> 'Node':
    node = Node(self.board.copy(), self.player)
    node.game_over = self.game_over
    node.player_ranges = self.player_ranges
    return node


def make_move(self, pit_index):
    # pick stones from selected pit and place them in the next player's pits
    stones = self.board[pit_index]
    self.board[pit_index] = 0
    for i in range(stones):
        pit_index = (pit_index + 1) % len(self.board)
        self.board[pit_index] += 1

    # last stone in player's base, do not change player
    if pit_index != (len(self.board) // (2 - self.player)) - 1:
        # stealing stones
        if self.board[pit_index] == 1:
            opposite_hole_index = len(self.board) - 2 - pit_index
            if pit_index in self.player_ranges[self.player]:
                self.board[(len(self.board) // (2 - self.player)) - 1] += self.board[opposite_hole_index]
                self.board[opposite_hole_index] = 0
        self.player = (self.player + 1) % 2

    # check if game is over
    if any(sum([self.board[index] for index in self.player_ranges[player]]) == 0 for player in (0, 1)):
        for player in (0, 1):
            self.board[(len(self.board) // (2 - player)) - 1] += sum(
                [self.board[i] for i in self.player_ranges[player]])
            for i in self.player_ranges[player]:
                self.board[i] = 0
        self.game_over = True


class AutoPlayer(QObject):
    make_move = Signal(int)
    stop = Signal()
    finished = Signal()
    calculate_move = Signal(list, int)

    def __init__(self, minimax_depth: int, auto_play_delay: int, no_alpha_beta: bool, iterative_deepening: bool):
        super(AutoPlayer, self).__init__()
        self.minimax_depth = minimax_depth
        self.auto_play_delay = auto_play_delay
        self.no_alpha_beta = no_alpha_beta
        self.iterative_deepening = iterative_deepening
        self.stopped = False

        self.calculate_move.connect(self.on_calculate_move)
        # hack to stop thread from outside
        self.stop.connect(self._stop)

    @Slot(list, int)
    def on_calculate_move(self, board: list[int], maximizing_player: int):
        start_time = QDateTime.currentSecsSinceEpoch()

        if _CMINIMAX_IMPORTED:
            index = CMinimax.run(board, maximizing_player, self.minimax_depth,
                                 not self.no_alpha_beta, self.iterative_deepening)
        else:
            node = Node(board, maximizing_player)
            if self.minimax_depth > 0:
                if self.iterative_deepening:
                    util, index = self._iterative_minimax(node, maximizing_player)
                else:
                    util, index = self._minimax(node, maximizing_player, float("-inf"),
                                                float("+inf"), self.minimax_depth)
            else:
                index = random.choice([i for i in node.player_ranges[maximizing_player] if board[i] > 0])

        if self.auto_play_delay > 0:
            if QDateTime.currentSecsSinceEpoch() - start_time < self.auto_play_delay:
                QThread.sleep(self.auto_play_delay - (QDateTime.currentSecsSinceEpoch() - start_time))

        if self.stopped:
            self.stopped = False
        else:
            if index != -1:
                self.make_move.emit(index)

    @Slot(Node, int, float, float, int)
    def _iterative_minimax(self, root: Node, maximizing_player: int) -> (int, int):
        best_util = float("-inf")
        best_index = -1
        for depth in range(1, self.minimax_depth + 1):
            util, index = self._minimax(root, maximizing_player, float("-inf"), float("+inf"), depth)
            if index != -1 and util > best_util:
                best_util = util
                best_index = index
        return best_util, best_index

    @Slot()
    def _stop(self) -> None:
        self.stopped = True

    @Slot(Node, int, int)
    def _minimax(self, node: Node, maximizing_player: int, alpha: float, beta: float, depth: int):
        if self.stopped is True:
            return 0, -1
        if node.game_over or depth == 0:
            return (node.board[int(len(node.board) / (2 - maximizing_player)) - 1] -
                    node.board[int(len(node.board) / (2 - ((maximizing_player + 1) % 2))) - 1], -1)

        for pit_index in node.player_ranges[node.player]:
            if pit_index not in node.children and node.board[pit_index] != 0:
                child = copy(node)
                make_move(child, pit_index)
                node.children[pit_index] = child

        best_index = -1
        if node.player == maximizing_player:
            max_value = float("-inf")
            for i, child in node.children.items():
                eval = self._minimax(child, maximizing_player, alpha, beta, depth - 1)[0]
                if eval >= max_value:
                    max_value = eval
                    best_index = i
                alpha = max(alpha, eval)
                if not self.no_alpha_beta and beta <= alpha:
                    break
            return max_value, best_index

        else:
            min_value = float("+inf")
            for i, child in node.children.items():
                eval = self._minimax(child, maximizing_player, alpha, beta, depth - 1)[0]
                if eval <= min_value:
                    min_value = eval
                    best_index = i
                beta = min(beta, eval)
                if not self.no_alpha_beta and beta <= alpha:
                    break
            return min_value, best_index
