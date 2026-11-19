"""Draws a simple open-chord fretboard diagram (6 strings x 4 frets)."""
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt

FRETS_SHOWN = 4
MARGIN = 30


class ChordDiagramWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.shape = None
        self.setMinimumSize(200, 240)

    def set_chord(self, shape):
        self.shape = shape
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        grid_w = w - 2 * MARGIN
        grid_h = h - 2 * MARGIN
        string_gap = grid_w / 5
        fret_gap = grid_h / FRETS_SHOWN

        pen = QPen(QColor("#333333"))
        pen.setWidth(2)
        painter.setPen(pen)

        # nut (thick top line) + frets
        for f in range(FRETS_SHOWN + 1):
            y = MARGIN + f * fret_gap
            pen.setWidth(5 if f == 0 else 1)
            painter.setPen(pen)
            painter.drawLine(MARGIN, y, MARGIN + grid_w, y)

        # strings
        pen.setWidth(1)
        painter.setPen(pen)
        for s in range(6):
            x = MARGIN + s * string_gap
            painter.drawLine(x, MARGIN, x, MARGIN + grid_h)

        if not self.shape:
            painter.end()
            return

        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)

        for s, fret in enumerate(self.shape):
            x = MARGIN + s * string_gap
            if fret is None:
                painter.drawText(x - 5, MARGIN - 10, "x")
            elif fret == 0:
                painter.drawText(x - 5, MARGIN - 10, "o")
            else:
                y = MARGIN + (fret - 0.5) * fret_gap
                painter.setBrush(QColor("#2b6cb0"))
                painter.drawEllipse(x - 8, y - 8, 16, 16)

        painter.end()
