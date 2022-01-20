from qtpy.QtCore import Slot

from kalaha.models import Algorithm


class CMinimax(Algorithm):

    def __init__(self):
        super(CMinimax, self).__init__()

    @Slot(list, int, dict)
    def run(self, board: list[int], maximizing_player: int, kwargs: dict) -> None:
        import CMinimax
        return CMinimax.run(board, maximizing_player, kwargs.get("minimax_depth", 4),
                            kwargs.get("alpha_beta", True), kwargs.get("iterative_deepening", False))

    @Slot()
    def stop(self) -> None:
        pass

    @Slot()
    def is_available(self) -> bool:
        try:
            import CMinimax
            return True
        except ImportError:
            return False
