from qtpy.QtCore import QObject, Signal, Slot

from kalaha.windows import AutoPlayerDialog
from kalaha.models import AutoPlayer


class AutoPlayerController(QObject):
    """
    Controller for the AutoPlayer.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.window = AutoPlayerDialog(parent)
        self.window.accepted.connect(self.on_auto_player_accepted)
        self.window.rejected.connect(self.window.on_auto_player_rejected)

        self.auto_player = None

    def on_auto_player_accepted(self):
        # TODO: take values from dialog
        if self.window.autoplayer_checkbox.isChecked():
            self.auto_player = AutoPlayer(self.window.minimax_depth, self.window.alpha_beta_pruning,
                                          self.window.iterative_deepening, self.window.turn_delay)
        else:
            self.auto_player = None
        self.window.close()

    def is_active(self):
        return self.auto_player is not None


