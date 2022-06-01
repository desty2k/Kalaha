from qtpy.QtWidgets import QWidget, QCheckBox, QGroupBox, QFormLayout, QSpinBox, QDialogButtonBox
from qtpy.QtCore import Slot
from qrainbowstyle.windows import FramelessCriticalMessageBox, FramelessWindow

from kalaha.widgets import CenteredFrameWidget


class AutoPlayerDialog(FramelessWindow):

    def __init__(self, parent=None):
        super(AutoPlayerDialog, self).__init__(parent)
        self.message_box = None
        self.frame_widget = CenteredFrameWidget(self)
        self.content_widget = QWidget(self.frame_widget)
        self.widget_layout = QFormLayout(self.content_widget)
        self.content_widget.setLayout(self.widget_layout)

        self.addContentWidget(self.frame_widget)
        self.frame_widget.set_center_widget(self.content_widget)

        self.enable_auto_player = QCheckBox("Enable Auto Player", self.content_widget)
        self.widget_layout.addRow(self.enable_auto_player)

        self.auto_player_groupbox = QGroupBox("Auto Player", self.content_widget)
        self.auto_player_groupbox_layout = QFormLayout(self.auto_player_groupbox)
        self.auto_player_groupbox.setLayout(self.auto_player_groupbox_layout)
        self.widget_layout.addRow(self.auto_player_groupbox)

        self.automove_checkbox = QCheckBox("Automove", self.auto_player_groupbox)
        self.auto_player_groupbox_layout.addRow(self.automove_checkbox)

        self.highlight_moves_checkbox = QCheckBox("Highlight", self.auto_player_groupbox)
        self.auto_player_groupbox_layout.addRow(self.highlight_moves_checkbox)

        self.auto_player_delay = QSpinBox(self.auto_player_groupbox)
        self.auto_player_groupbox_layout.addRow("Auto player delay", self.auto_player_delay)

        self.minimax_depth = QSpinBox(self.auto_player_groupbox)
        self.auto_player_groupbox_layout.addRow("Minimax depth", self.minimax_depth)

        self.enable_alpha_beta = QCheckBox("Alpha-beta pruning", self.auto_player_groupbox)
        self.auto_player_groupbox_layout.addRow(self.enable_alpha_beta)

        self.enable_iterative_deepening = QCheckBox("Iterative deepening", self.auto_player_groupbox)
        self.auto_player_groupbox_layout.addRow(self.enable_iterative_deepening)

        self.button_box = QDialogButtonBox(self.content_widget)
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.button(QDialogButtonBox.Ok).clicked.connect(self.accepted.emit)
        self.button_box.button(QDialogButtonBox.Cancel).clicked.connect(self.rejected.emit)

        self.widget_layout.addWidget(self.button_box)

    @Slot()
    def on_failed_to_enable_auto_player(self):
        self.message_box = FramelessCriticalMessageBox(self)
        self.message_box.setText("Failed to enable auto player. Could not load CMiniMax extension module."
                                 "Please build the extension module and try again.")
        self.message_box.setStandardButtons(QDialogButtonBox.Ok)
        self.message_box.button(QDialogButtonBox.Ok).clicked.connect(self.message_box.close)
        self.message_box.show()
