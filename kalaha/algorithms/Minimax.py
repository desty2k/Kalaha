from qtpy.QtCore import Slot

from kalaha.models import Algorithm, Node

import random


class Minimax(Algorithm):
    available_options = {"minimax_depth": {"type": int, "default": 4, "min": 0, "max": 100, "value": 4},
                         "iterative_deepening": {"type": bool, "default": False, "value": False},
                         "alpha_beta_pruning": {"type": bool, "default": False, "value": False}}

    def __init__(self):
        super(Minimax, self).__init__()

    @Slot(list, int)
    def run(self, board: list[int], maximizing_player: int) -> int:
        minimax_depth = self.options.get("minimax_depth").get("value")
        iterative_deepening = self.options.get("iterative_deepening").get("value")
        alpha_beta_pruning = self.options.get("alpha_beta_pruning").get("value")

        node = Node(board, maximizing_player)
        if minimax_depth > 0:
            if iterative_deepening:
                util, index = self.__calculate_iterative_deepening(node, maximizing_player,
                                                                   alpha_beta_pruning, minimax_depth)
            else:
                util, index = self.__calculate_minimax(node, maximizing_player, alpha_beta_pruning,
                                                       float("-inf"), float("+inf"), minimax_depth)
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
    def __calculate_iterative_deepening(self, root: Node, maximizing_player: int,
                                        alpha_beta: bool, minimax_depth: int) -> (int, int):
        best_util = float("-inf")
        best_index = -1
        for depth in range(1, minimax_depth + 1):
            util, index = self.__calculate_minimax(root, maximizing_player, alpha_beta,
                                                   float("-inf"), float("+inf"), depth)
            if util > best_util:
                best_util = util
                best_index = index
        return best_util, best_index

    @Slot(Node, int, int)
    def __calculate_minimax(self, node: Node, maximizing_player: int, alpha_beta: bool,
                            alpha: float, beta: float, depth: int) -> (int, int):
        if node.game_over or depth == 0:
            return (node.board[int(len(node.board) / (2 - maximizing_player)) - 1] -
                    node.board[int(len(node.board) / (2 - ((maximizing_player + 1) % 2))) - 1], -1)

        for pit_index in node.player_ranges[node.player]:
            if pit_index not in node.children and node.board[pit_index] != 0:
                child = node.copy()
                child.make_move(pit_index)
                node.children[pit_index] = child

        best_index = -1
        if node.player == maximizing_player:
            best_util = float("-inf")
            for i, child in node.children.items():
                util = self.__calculate_minimax(child, maximizing_player, alpha_beta, alpha, beta, depth - 1)[0]
                if util >= best_util:
                    best_util = util
                    best_index = i
                alpha = max(alpha, util)
                if alpha_beta and beta <= alpha:
                    break
            return best_util, best_index

        else:
            best_util = float("+inf")
            for i, child in node.children.items():
                util = self.__calculate_minimax(child, maximizing_player, alpha_beta, alpha, beta, depth - 1)[0]
                if util <= best_util:
                    best_util = util
                    best_index = i
                beta = min(beta, util)
                if alpha_beta and beta <= alpha:
                    break
            return best_util, best_index
