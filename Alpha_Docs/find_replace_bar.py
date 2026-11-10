"""
find_replace_bar.py — Sleek Floating / Embedded Find & Replace Bar for Alpha Docs
Provides text search, replace, match counts, case sensitivity, and next/previous navigation.
"""

from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton,
    QLabel, QCheckBox, QToolButton
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon


class FindReplaceBar(QFrame):
    """Modern inline search and replace bar for the document canvas."""

    find_next_requested = Signal(str, bool, bool)       # text, match_case, whole_word
    find_prev_requested = Signal(str, bool, bool)       # text, match_case, whole_word
    replace_requested = Signal(str, str, bool, bool)    # find_text, replace_text, match_case, whole_word
    replace_all_requested = Signal(str, str, bool, bool)
    close_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("findReplaceBar")
        self._theme_accent = "#00adb5"
        self._apply_styling(self._theme_accent)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(6)

        # ── Row 1: Find Row ──────────────────────────────────────────────────
        row1 = QHBoxLayout()
        row1.setSpacing(6)

        lbl_find = QLabel("🔍")
        row1.addWidget(lbl_find)

        self.input_find = QLineEdit()
        self.input_find.setPlaceholderText("Find text in document…")
        self.input_find.returnPressed.connect(self._on_find_next)
        self.input_find.textChanged.connect(self._on_find_text_changed)
        row1.addWidget(self.input_find, 1)

        self.lbl_matches = QLabel("0 matches")
        self.lbl_matches.setObjectName("matchCountLabel")
        self.lbl_matches.setAlignment(Qt.AlignmentFlag.AlignCenter)
        row1.addWidget(self.lbl_matches)

        self.btn_prev = QToolButton()
        self.btn_prev.setText("▲ Prev")
        self.btn_prev.setToolTip("Find Previous (Shift+Enter)")
        self.btn_prev.clicked.connect(self._on_find_prev)
        row1.addWidget(self.btn_prev)

        self.btn_next = QToolButton()
        self.btn_next.setText("▼ Next")
        self.btn_next.setToolTip("Find Next (Enter)")
        self.btn_next.clicked.connect(self._on_find_next)
        row1.addWidget(self.btn_next)

        self.cb_case = QCheckBox("Aa Match Case")
        self.cb_case.toggled.connect(self._on_find_text_changed)
        row1.addWidget(self.cb_case)

        self.cb_word = QCheckBox("Whole Word")
        self.cb_word.toggled.connect(self._on_find_text_changed)
        row1.addWidget(self.cb_word)

        self.btn_close = QToolButton()
        self.btn_close.setText("✕")
        self.btn_close.setToolTip("Close Find Bar (Esc)")
        self.btn_close.clicked.connect(self.close_bar)
        row1.addWidget(self.btn_close)

        main_layout.addLayout(row1)

        # ── Row 2: Replace Row ───────────────────────────────────────────────
        self.row2_widget = QFrame()
        row2 = QHBoxLayout(self.row2_widget)
        row2.setContentsMargins(0, 0, 0, 0)
        row2.setSpacing(6)

        lbl_replace = QLabel("🔄")
        row2.addWidget(lbl_replace)

        self.input_replace = QLineEdit()
        self.input_replace.setPlaceholderText("Replace with…")
        row2.addWidget(self.input_replace, 1)

        self.btn_replace = QPushButton("Replace")
        self.btn_replace.clicked.connect(self._on_replace)
        row2.addWidget(self.btn_replace)

        self.btn_replace_all = QPushButton("Replace All")
        self.btn_replace_all.setObjectName("btnPrimary")
        self.btn_replace_all.clicked.connect(self._on_replace_all)
        row2.addWidget(self.btn_replace_all)

        main_layout.addWidget(self.row2_widget)

    def _apply_styling(self, accent: str):
        self.setStyleSheet(f"""
            QFrame#findReplaceBar {{
                background: rgba(22, 25, 32, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 8px;
                padding: 6px;
            }}
            QLineEdit {{
                background: #1a1d24;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 5px;
                color: #ffffff;
                padding: 4px 8px;
                font-size: 12px;
            }}
            QLineEdit:focus {{
                border: 1px solid {accent};
            }}
            QPushButton, QToolButton {{
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 5px;
                color: #e0e0e0;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: 600;
            }}
            QPushButton:hover, QToolButton:hover {{
                background: rgba(255, 255, 255, 0.16);
                border-color: {accent};
                color: #ffffff;
            }}
            QPushButton#btnPrimary {{
                background: {accent};
                color: #ffffff;
                border: none;
            }}
            QPushButton#btnPrimary:hover {{
                background: {accent};
                border: 1px solid #ffffff;
            }}
            QCheckBox {{
                color: #a0aab8;
                font-size: 11px;
                spacing: 6px;
            }}
            QCheckBox:hover {{
                color: #ffffff;
            }}
            QCheckBox::indicator {{
                width: 14px;
                height: 14px;
                border-radius: 3px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                background: rgba(255, 255, 255, 0.05);
            }}
            QCheckBox::indicator:hover {{
                border-color: {accent};
            }}
            QCheckBox::indicator:checked {{
                background-color: {accent};
                border: 1px solid {accent};
            }}
            QCheckBox:checked {{
                color: #ffffff;
                font-weight: 600;
            }}
            QLabel#matchCountLabel {{
                color: {accent};
                font-weight: bold;
                font-size: 11px;
                min-width: 70px;
            }}
        """)

    def set_theme_accent(self, accent_hex: str):
        """Dynamically updates find bar glow and button styling."""
        self._theme_accent = accent_hex
        self._apply_styling(accent_hex)
        # Update match count label if active
        if hasattr(self, "lbl_matches") and "matches" in self.lbl_matches.text() and not self.lbl_matches.text().startswith("No"):
            self.lbl_matches.setStyleSheet(f"color: {accent_hex}; font-weight: bold; font-size: 11px;")

    # ── Public API ───────────────────────────────────────────────────────────

    def open_find(self, show_replace: bool = False, prefill_text: str = ""):
        self.row2_widget.setVisible(show_replace)
        if prefill_text:
            self.input_find.setText(prefill_text)
        self.show()
        self.input_find.setFocus()
        self.input_find.selectAll()

    def close_bar(self):
        self.hide()
        self.close_requested.emit()

    def set_match_status(self, current: int, total: int):
        if total == 0:
            self.lbl_matches.setText("No matches")
            self.lbl_matches.setStyleSheet("color: #e06c75; font-weight: bold; font-size: 11px;")
        else:
            self.lbl_matches.setText(f"{current} of {total}")
            acc = getattr(self, "_theme_accent", "#00adb5")
            self.lbl_matches.setStyleSheet(f"color: {acc}; font-weight: bold; font-size: 11px;")

    # ── Internal Event Handlers ──────────────────────────────────────────────

    def _on_find_next(self):
        text = self.input_find.text()
        if text:
            self.find_next_requested.emit(text, self.cb_case.isChecked(), self.cb_word.isChecked())

    def _on_find_prev(self):
        text = self.input_find.text()
        if text:
            self.find_prev_requested.emit(text, self.cb_case.isChecked(), self.cb_word.isChecked())

    def _on_find_text_changed(self):
        text = self.input_find.text()
        if text:
            self.find_next_requested.emit(text, self.cb_case.isChecked(), self.cb_word.isChecked())
        else:
            self.lbl_matches.setText("0 matches")

    def _on_replace(self):
        find_text = self.input_find.text()
        replace_text = self.input_replace.text()
        if find_text:
            self.replace_requested.emit(find_text, replace_text, self.cb_case.isChecked(), self.cb_word.isChecked())

    def _on_replace_all(self):
        find_text = self.input_find.text()
        replace_text = self.input_replace.text()
        if find_text:
            self.replace_all_requested.emit(find_text, replace_text, self.cb_case.isChecked(), self.cb_word.isChecked())

