import copy

from qtpy.QtCore import QObject, Signal, Slot, QDateTime, QThread


class Algorithm(QObject):
    """Base class for all Kalaha algorithms."""
    calculate_move = Signal(list, int, int)
    make_move = Signal(int)
    available_options = {}

    def __init__(self):
        super(Algorithm, self).__init__()
        self.options = copy.deepcopy(self.available_options)
        self.calculate_move.connect(self.start)

    @Slot(list, int, int)
    def start(self, board: list[int], maximizing_player: int, auto_play_delay: int) -> None:
        start_time = QDateTime.currentSecsSinceEpoch()
        move = self.run(board, maximizing_player)
        if auto_play_delay > 0:
            if QDateTime.currentSecsSinceEpoch() - start_time < auto_play_delay:
                QThread.sleep(auto_play_delay - (QDateTime.currentSecsSinceEpoch() - start_time))
        self.make_move.emit(move)

    @Slot(list, int)
    def run(self, board: list[int], maximizing_player: int) -> None:
        raise NotImplementedError("Algorithm.run() must be implemented.")

    @Slot()
    def stop(self) -> None:
        raise NotImplementedError("Algorithm.stop() must be implemented.")

    @Slot()
    def is_available(self) -> bool:
        raise NotImplementedError("Algorithm.is_available() must be implemented.")
