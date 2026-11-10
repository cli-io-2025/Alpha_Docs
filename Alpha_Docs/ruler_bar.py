"""
ruler_bar.py — Horizontal Top Ruler Widget for Alpha Docs Tool
Renders page margin indicators and inch/cm scale markers above the document viewport.
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QFont, QPen


class HorizontalRulerBar(QWidget):
    """Visual horizontal ruler widget matching page margins and width."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(24)
        self._margin_left_mm = 25.4
        self._margin_right_mm = 25.4
        self._page_width_mm = 215.9
        self._zoom_factor = 1.0
        self._scroll_x = 0.0

    def set_ruler_params(self, left_mm: float, right_mm: float, page_w_mm: float, zoom: float):
        self._margin_left_mm = left_mm
        self._margin_right_mm = right_mm
        self._page_width_mm = page_w_mm
        self._zoom_factor = zoom
        self.update()

    def set_scroll_offset(self, scroll_x: float):
        if self._scroll_x != scroll_x:
            self._scroll_x = float(scroll_x)
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        # Background bar
        painter.fillRect(0, 0, w, h, QColor(25, 28, 36))

        # Calculate page center alignment with horizontal scroll offset
        page_w_px = (self._page_width_mm / 25.4 * 72.0) * self._zoom_factor
        page_x = max(0.0, (w - page_w_px) / 2.0) - self._scroll_x
        left_m_px = (self._margin_left_mm / 25.4 * 72.0) * self._zoom_factor
        right_m_px = (self._margin_right_mm / 25.4 * 72.0) * self._zoom_factor

        # Draw page canvas boundary on ruler
        painter.fillRect(QRectF(page_x, 0, page_w_px, h), QColor(40, 44, 55))
        painter.fillRect(QRectF(page_x + left_m_px, 0, page_w_px - left_m_px - right_m_px, h), QColor(50, 56, 70))

        # Ruler tick marks (every 0.25 inch = 18 points)
        pen = QPen(QColor(160, 170, 185), 1)
        painter.setPen(pen)
        font = QFont("Sans-Serif", 7)
        painter.setFont(font)

        step_px = 18.0 * self._zoom_factor
        total_ticks = int(page_w_px / step_px)

        for i in range(total_ticks + 1):
            x = page_x + i * step_px
            if x > page_x + page_w_px:
                break
            
            tick_h = 4
            if i % 4 == 0:
                tick_h = 10
                inch_num = i // 4
                painter.drawText(int(x - 6), 11, f"{inch_num}")
            elif i % 2 == 0:
                tick_h = 6

            painter.drawLine(int(x), h - tick_h, int(x), h)
