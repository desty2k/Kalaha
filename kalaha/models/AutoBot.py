from qtpy.QtCore import QObject, Signal, Slot, QThread

from .Player import Player
from .Board import Board


class CMinimaxWorker(QObject):
    move_calculated = Signal(int)

    def __init__(self):
        super().__init__()

    @Slot(Board, Player)
    def run(self, board: Board, maximizing_player: int,
            minimax_depth: int, alpha_beta_pruning: bool, iterative_deepening: bool):
        import CMinimax
        pit = CMinimax.run(board.board, maximizing_player, minimax_depth, alpha_beta_pruning, iterative_deepening)
        self.move_calculated.emit(pit)


class AutoPlayer(QObject):
    move_calculated = Signal(int)

    def __init__(self, minimax_depth: int, alpha_beta_pruning: bool, iterative_deepening: bool):
        super(AutoPlayer, self).__init__()
        self.minimax_depth = minimax_depth
        self.alpha_beta_pruning = alpha_beta_pruning
        self.iterative_deepening = iterative_deepening

        self.worker = None
        self.thread = QThread()
        self.disposed_workers = []

    @Slot(Board, int)
    def calculate_move(self, board: Board, maximizing_player: int):
        import CMinimax
        pit = CMinimax.run(board.board, maximizing_player, self.minimax_depth,
                           self.alpha_beta_pruning, self.iterative_deepening)
        self.move_calculated.emit(pit)
        # if self.worker is not None:
        #     self.disposed_workers.append(self.worker)
        #
        # self.worker = CMinimaxWorker()
        # self.worker.move_calculated.connect(self.on_move_calculated)
        # self.worker.moveToThread(self.thread)
        # self.thread.start()
        #
        # if self.worker is None:
        #     self.worker = CMinimaxWorker()
        #     self.worker.moveToThread(self.thread)
        #     self.thread.start()
        # else:

    # @Slot(int)
    # def on_move_calculated(self, move: int):
    #     if self.sender() not in self.disposed_workers

    @staticmethod
    def is_available() -> bool:
        try:
            import CMinimax
            return True
        except ImportError:
            return False
