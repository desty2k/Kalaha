from qtpy.QtCore import Slot

from kalaha.models import Algorithm


class CMaximax(Algorithm):
    available_options = {"minimax_depth": {"type": int, "default": 4, "min": 0, "max": 100, "value": 4},
                         "iterative_deepening": {"type": bool, "default": False, "value": False}}

    def __init__(self):
        super(CMaximax, self).__init__()

    @Slot(list, int)
    def run(self, board: list[int], maximizing_player: int) -> None:
        import CMaximax
        minimax_depth = self.options.get("minimax_depth").get("value")
        iterative_deepening = self.options.get("iterative_deepening").get("value")
        return CMaximax.run(board, maximizing_player, minimax_depth, iterative_deepening)

    @Slot()
    def stop(self) -> None:
        pass

    @Slot()
    def is_available(self) -> bool:
        try:
            import CMaximax
            return True
        except ImportError:
            return False
