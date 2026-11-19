"""Theory tab: browse open chord diagrams."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel
from PySide6.QtCore import Qt

from src.content.chords import CHORD_SHAPES
from src.ui.chord_diagram import ChordDiagramWidget


class TheoryScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.chord_box = QComboBox()
        self.chord_box.addItems(CHORD_SHAPES.keys())
        self.chord_box.currentTextChanged.connect(self._on_chord_changed)

        self.diagram = ChordDiagramWidget()

        hint = QLabel("o = leere Saite spielen, x = Saite nicht anschlagen, Punkt = Bund greifen")
        hint.setAlignment(Qt.AlignCenter)
        hint.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Akkord:"))
        layout.addWidget(self.chord_box)
        layout.addWidget(self.diagram)
        layout.addWidget(hint)
        self.setLayout(layout)

        self._on_chord_changed(self.chord_box.currentText())

    def _on_chord_changed(self, name):
        self.diagram.set_chord(CHORD_SHAPES[name])
