from qtpy.QtCore import Slot

from kalaha.models import Algorithm

import random


class Node:
    def __init__(self, board: list[int], player):
        super(Node, self).__init__()
        self.board = board
        self.player = player
        self.game_over = False
        self.children: dict[int, Node] = {}
        self.player_ranges = (range(0, len(board) // 2 - 1), range(len(board) // 2, len(board) - 1))

    __slots__ = ("board", "player", "player_ranges", "game_over", "children")


# methods are outside of the class to reduce memory usage
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


class Minimax(Algorithm):

    def __init__(self):
        super(Minimax, self).__init__()

    @Slot(list, int, dict)
    def run(self, board: list[int], maximizing_player: int, kwargs: dict) -> int:
        minimax_depth = kwargs.get("minimax_depth", 4)
        iterative_deepening = kwargs.get("iterative_deepening", False)
        alpha_beta = kwargs.get("alpha_beta", False)

        node = Node(board, maximizing_player)
        if minimax_depth > 0:
            if iterative_deepening:
                util, index = self.__iterative_minimax(node, maximizing_player, minimax_depth, alpha_beta)
            else:
                util, index = self.__minimax(node, maximizing_player, float("-inf"),
                                             float("+inf"), minimax_depth, alpha_beta)
        else:
            index = random.choice([i for i in node.player_ranges[maximizing_player] if board[i] > 0])
        return index

    @Slot()
    def stop(self) -> None:
        pass

    @Slot()
    def is_available(self) -> bool:
        return True

    @Slot(Node, int, float, float, int)
    def __iterative_minimax(self, root: Node, maximizing_player: int, minimax_depth: int, alpha_beta: bool) -> (int, int):
        best_util = float("-inf")
        best_index = -1
        for depth in range(1, minimax_depth + 1):
            util, index = self.__minimax(root, maximizing_player, float("-inf"), float("+inf"), depth, alpha_beta)
            if util > best_util:
                best_util = util
                best_index = index
        return best_util, best_index

    @Slot(Node, int, int)
    def __minimax(self, node: Node, maximizing_player: int, alpha: float,
                  beta: float, depth: int, alpha_beta: bool) -> (int, int):
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
                eval = self.__minimax(child, maximizing_player, alpha, beta, depth - 1, alpha_beta)[0]
                if eval >= max_value:
                    max_value = eval
                    best_index = i
                alpha = max(alpha, eval)
                if alpha_beta and beta <= alpha:
                    break
            return max_value, best_index

        else:
            min_value = float("+inf")
            for i, child in node.children.items():
                eval = self.__minimax(child, maximizing_player, alpha, beta, depth - 1, alpha_beta)[0]
                if eval <= min_value:
                    min_value = eval
                    best_index = i
                beta = min(beta, eval)
                if alpha_beta and beta <= alpha:
                    break
            return min_value, best_index
