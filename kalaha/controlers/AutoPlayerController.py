from qtpy.QtCore import QObject, Signal, Slot, QTimer

from kalaha.windows import AutoPlayerDialog
from kalaha.models import AutoPlayer


class AutoPlayerController(QObject):
    make_move = Signal(int)
    highlight_pit = Signal(bool, int)
    auto_player_enabled = Signal(bool)
    """
    Controller for the AutoPlayer.
    """

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.window = AutoPlayerDialog(self.parent().window)
        self.window.enable_auto_player.stateChanged.connect(self.window.auto_player_groupbox.setEnabled)
        self.window.accepted.connect(self.on_auto_player_accepted)
        self.window.rejected.connect(self.window.close)
        self.window.auto_player_groupbox.setEnabled(self.window.enable_auto_player.isChecked())

        self.auto_player = None
        if self.config.auto_play:
            self.window.enable_auto_player.setChecked(True)
            self.window.minimax_depth.setValue(self.config.minimax_depth)
            self.window.enable_alpha_beta.setChecked(self.config.alpha_beta)
            self.window.enable_iterative_deepening.setChecked(self.config.iterative_deepening)
            self.window.highlight_moves_checkbox.setChecked(self.config.highlight_moves)
            self.window.auto_player_delay.setValue(self.config.auto_player_delay)
            self.on_auto_player_accepted()

    def on_auto_player_accepted(self):
        if self.window.enable_auto_player.isChecked():
            self.auto_player = AutoPlayer(self.window.minimax_depth.value(),
                                          self.window.enable_alpha_beta.isChecked(),
                                          self.window.enable_iterative_deepening.isChecked())
            self.auto_player.move_calculated.connect(self.on_move_calculated)
            self.auto_player_enabled.emit(True)
        else:
            self.auto_player = None
            self.auto_player_enabled.emit(False)
        self.window.close()

    @Slot(int)
    def on_move_calculated(self, pit: int):
        if self.window.highlight_moves_checkbox.isChecked():
            self.highlight_pit.emit(True, pit)
        QTimer.singleShot(self.window.auto_player_delay.value() * 1000, lambda: self.make_move.emit(pit))

    def is_active(self):
        return self.auto_player is not None

