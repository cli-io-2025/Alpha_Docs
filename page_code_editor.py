"""
page_code_editor.py — Alpha Tech Code Workspace Engine
Enterprise code editor with Pygments syntax highlighting, line numbers gutter,
active line highlighting, language selection, and utility actions.
"""
import os
import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QLabel,
    QComboBox, QPushButton, QFrame, QApplication, QTextEdit,
    QTabWidget, QColorDialog, QInputDialog
)
from PySide6.QtGui import (
    QSyntaxHighlighter, QTextCharFormat, QFont, QColor,
    QPainter, QTextFormat, QTextCursor, QKeySequence, QShortcut
)
from PySide6.QtCore import Qt, QRect, QSize, QTimer

try:
    from pygments import lex
    from pygments.lexers import get_lexer_by_name
    from pygments.styles import get_style_by_name
    HAS_PYGMENTS = True
except ImportError:
    HAS_PYGMENTS = False


class PygmentsHighlighter(QSyntaxHighlighter):
    """QSyntaxHighlighter subclass using Pygments with robust light/dark contrast preservation."""

    def __init__(self, parent=None, language='python', style='monokai', is_dark=True, default_text_color=None):
        super().__init__(parent)
        self.language = language
        self.style_name = style
        self.is_dark = is_dark
        self.default_text_color = default_text_color or ("#f8f8f2" if is_dark else "#24292e")
        self._format_cache = {}
        self.lexer = None
        self.pygments_style = None
        self._init_lexer_and_style()

    def _init_lexer_and_style(self):
        if not HAS_PYGMENTS:
            return
        try:
            self.lexer = get_lexer_by_name(self.language)
        except Exception:
            try:
                self.lexer = get_lexer_by_name('text')
            except Exception:
                self.lexer = None

        try:
            self.pygments_style = get_style_by_name(self.style_name)
        except Exception:
            try:
                self.pygments_style = get_style_by_name('default' if not self.is_dark else 'monokai')
            except Exception:
                self.pygments_style = None

    def set_language(self, language: str):
        self.language = language
        self._format_cache.clear()
        self._init_lexer_and_style()
        self.rehighlight()

    def set_style(self, style_name: str):
        self.style_name = style_name
        self._format_cache.clear()
        self._init_lexer_and_style()
        self.rehighlight()

    def set_theme_context(self, style_name: str, is_dark: bool, default_text_color: str):
        self.style_name = style_name
        self.is_dark = is_dark
        self.default_text_color = default_text_color or ("#f8f8f2" if is_dark else "#24292e")
        self._format_cache.clear()
        self._init_lexer_and_style()
        self.rehighlight()

    def get_format(self, token):
        if token in self._format_cache:
            return self._format_cache[token]

        fmt = QTextCharFormat()
        color_found = False

        if HAS_PYGMENTS and self.pygments_style:
            style_dict = self.pygments_style.style_for_token(token)
            c_hex = style_dict.get('color')
            if c_hex:
                qc = QColor(f"#{c_hex}")
                # Contrast protection: avoid washed-out characters on white/dark surfaces
                lum = qc.red() * 0.299 + qc.green() * 0.587 + qc.blue() * 0.114
                if not self.is_dark and lum > 210:
                    qc = QColor(self.default_text_color)
                elif self.is_dark and lum < 45:
                    qc = QColor(self.default_text_color)
                fmt.setForeground(qc)
                color_found = True
            if style_dict.get('bgcolor'):
                fmt.setBackground(QColor(f"#{style_dict['bgcolor']}"))
            if style_dict.get('bold'):
                fmt.setFontWeight(QFont.Weight.Bold)
            if style_dict.get('italic'):
                fmt.setFontItalic(True)

        if not color_found:
            from pygments.token import Token
            if not self.is_dark:
                # ── Light Theme Syntax (e.g. GitHub Light) ──
                # Guarantees zero washed-out characters against pure white/light backgrounds
                if token in Token.Keyword:
                    fmt.setForeground(QColor("#d73a49"))  # GitHub crimson red
                    fmt.setFontWeight(QFont.Weight.Bold)
                elif token in Token.Name.Function or token in Token.Name.Class:
                    fmt.setForeground(QColor("#6f42c1"))  # GitHub purple
                    fmt.setFontWeight(QFont.Weight.Bold)
                elif token in Token.String:
                    fmt.setForeground(QColor("#032f62"))  # GitHub navy
                elif token in Token.Number:
                    fmt.setForeground(QColor("#005cc5"))  # GitHub royal blue
                elif token in Token.Comment:
                    fmt.setForeground(QColor("#6a737d"))  # GitHub muted grey
                    fmt.setFontItalic(True)
                elif token in Token.Operator:
                    fmt.setForeground(QColor("#d73a49"))  # GitHub crimson operator
                elif token in Token.Name.Builtin:
                    fmt.setForeground(QColor("#005cc5"))  # Royal blue builtin
                elif token in Token.Name.Decorator:
                    fmt.setForeground(QColor("#6f42c1"))  # Purple decorator
                elif token in Token.Name.Tag:
                    fmt.setForeground(QColor("#22863a"))  # Deep green tag
                elif token in Token.Name.Attribute:
                    fmt.setForeground(QColor("#6f42c1"))  # Purple attribute
                else:
                    # Variables, identifiers, punctuation, brackets, operators: high-contrast dark
                    fmt.setForeground(QColor(self.default_text_color or "#24292e"))
            else:
                # ── Dark Theme Syntax (e.g. Monokai / Dark+) ──
                if token in Token.Keyword:
                    fmt.setForeground(QColor("#66d9ef"))
                    fmt.setFontWeight(QFont.Weight.Bold)
                elif token in Token.Name.Function:
                    fmt.setForeground(QColor("#a6e22e"))
                elif token in Token.Name.Class:
                    fmt.setForeground(QColor("#a6e22e"))
                    fmt.setFontWeight(QFont.Weight.Bold)
                elif token in Token.String:
                    fmt.setForeground(QColor("#e6db74"))
                elif token in Token.Number:
                    fmt.setForeground(QColor("#ae81ff"))
                elif token in Token.Comment:
                    fmt.setForeground(QColor("#75715e"))
                    fmt.setFontItalic(True)
                elif token in Token.Operator:
                    fmt.setForeground(QColor("#f92672"))
                elif token in Token.Name.Builtin:
                    fmt.setForeground(QColor("#66d9ef"))
                    fmt.setFontItalic(True)
                elif token in Token.Name.Decorator:
                    fmt.setForeground(QColor("#f92672"))
                elif token in Token.Name.Tag:
                    fmt.setForeground(QColor("#f92672"))
                elif token in Token.Name.Attribute:
                    fmt.setForeground(QColor("#a6e22e"))
                else:
                    fmt.setForeground(QColor(self.default_text_color or "#f8f8f2"))

        self._format_cache[token] = fmt
        return fmt

    def highlightBlock(self, text):
        if not HAS_PYGMENTS or not self.lexer or not text:
            return

        current_idx = 0
        text_len = len(text)
        for token, val in lex(text, self.lexer):
            length = len(val)
            if length > 0 and current_idx < text_len:
                self.setFormat(current_idx, min(length, text_len - current_idx), self.get_format(token))
            current_idx += length


class LineNumberArea(QWidget):
    """Side gutter widget rendering line numbers synchronized with the code editor."""

    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)


class CodeEditorWidget(QPlainTextEdit):
    """Enhanced QPlainTextEdit with line numbers, active line highlight, zooming, and customizable theme."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("codeEditorArea")
        self.line_number_area = LineNumberArea(self)

        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)

        self._bg_color = QColor("#272822")
        self._gutter_color = QColor("#1c1d1a")
        self._gutter_border = QColor("#2c2d28")
        self._current_line_color = QColor("#3e3d32")
        self._text_color = QColor("#f8f8f2")

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlight_current_line()

    def set_theme_colors(self, bg: str, gutter: str, line_highlight: str, text_color: str):
        self._bg_color = QColor(bg)
        self._gutter_color = QColor(gutter)
        is_dark = (self._bg_color.red() * 0.299 + self._bg_color.green() * 0.587 + self._bg_color.blue() * 0.114) < 128
        self._gutter_border = self._gutter_color.lighter(130) if is_dark else self._gutter_color.darker(115)
        self._current_line_color = QColor(line_highlight)
        self._text_color = QColor(text_color)
        selection_bg = "#264f78" if is_dark else "#c8e1ff"
        selection_color = "#ffffff" if is_dark else "#041427"
        border_color = "rgba(255, 255, 255, 0.08)" if is_dark else "rgba(0, 0, 0, 0.12)"
        self.setStyleSheet(f"""
            QPlainTextEdit#codeEditorArea {{
                background-color: {bg};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 8px;
                padding: 6px;
                selection-background-color: {selection_bg};
                selection-color: {selection_color};
            }}
        """)
        self.highlight_current_line()
        self.line_number_area.update()
        self.viewport().update()

    def zoomIn(self, step: int = 1):
        f = self.font()
        f.setPointSize(min(36, f.pointSize() + step))
        self.setFont(f)
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)
        self.update_line_number_area_width(0)

    def zoomOut(self, step: int = 1):
        f = self.font()
        f.setPointSize(max(8, f.pointSize() - step))
        self.setFont(f)
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)
        self.update_line_number_area_width(0)

    def resetZoom(self):
        f = self.font()
        f.setPointSize(11)
        self.setFont(f)
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)
        self.update_line_number_area_width(0)

    def wheelEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoomIn()
            elif delta < 0:
                self.zoomOut()
            event.accept()
            return
        super().wheelEvent(event)

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            key = event.key()
            if key in (Qt.Key.Key_Plus, Qt.Key.Key_Equal):
                self.zoomIn()
                event.accept()
                return
            elif key in (Qt.Key.Key_Minus, Qt.Key.Key_Underscore):
                self.zoomOut()
                event.accept()
                return
            elif key == Qt.Key.Key_0:
                self.resetZoom()
                event.accept()
                return
        super().keyPressEvent(event)

    def line_number_area_width(self):
        digits = 1
        m = max(1, self.blockCount())
        while m >= 10:
            m //= 10
            digits += 1
        return 16 + self.fontMetrics().horizontalAdvance('9') * max(3, digits)

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), getattr(self, "_gutter_color", QColor("#1c1d1a")))

        # Right border line for line numbers
        painter.setPen(getattr(self, "_gutter_border", QColor("#2c2d28")))
        painter.drawLine(event.rect().topRight(), event.rect().bottomRight())

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        current_block = self.textCursor().blockNumber()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                if block_number == current_block:
                    acc_color = QColor(getattr(self, "_theme_accent", "#00adb5"))
                    painter.setPen(acc_color)
                else:
                    bg_c = getattr(self, "_bg_color", QColor("#272822"))
                    is_dark = (bg_c.red() * 0.299 + bg_c.green() * 0.587 + bg_c.blue() * 0.114) < 128
                    painter.setPen(QColor("#686858") if is_dark else QColor("#8c959f"))
                painter.setFont(self.font())
                painter.drawText(0, top, self.line_number_area.width() - 8, self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(getattr(self, "_current_line_color", QColor("#3e3d32")))
            bg_c = getattr(self, "_bg_color", QColor("#272822"))
            is_dark = (bg_c.red() * 0.299 + bg_c.green() * 0.587 + bg_c.blue() * 0.114) < 128
            line_color.setAlpha(90 if is_dark else 130)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)


CODE_THEMES = {
    "Monokai Dark": {
        "bg": "#272822", "gutter": "#1c1d1a", "line": "#3e3d32", "text": "#f8f8f2", "style": "monokai"
    },
    "VS Code Dark+": {
        "bg": "#1e1e1e", "gutter": "#181818", "line": "#2a2d2e", "text": "#d4d4d4", "style": "monokai"
    },
    "Dracula": {
        "bg": "#282a36", "gutter": "#21222c", "line": "#44475a", "text": "#f8f8f2", "style": "monokai"
    },
    "Cyberpunk Navy": {
        "bg": "#0d1117", "gutter": "#070a0f", "line": "#1f242c", "text": "#c9d1d9", "style": "monokai"
    },
    "GitHub Light": {
        "bg": "#ffffff", "gutter": "#f6f8fa", "line": "#eaeef2", "text": "#24292e", "style": "default"
    },
    "Solarized Dark": {
        "bg": "#002b36", "gutter": "#073642", "line": "#073642", "text": "#839496", "style": "monokai"
    },
}


class CodeEditorPage(QWidget):
    """A dedicated multi-tab code editing workspace with syntax highlighting, background customization, and AI integration."""

    SUPPORTED_LANGUAGES = [
        ("Python", "python"),
        ("JavaScript", "javascript"),
        ("TypeScript", "typescript"),
        ("JSON", "json"),
        ("HTML", "html"),
        ("CSS", "css"),
        ("Markdown", "markdown"),
        ("C / C++", "cpp"),
        ("Rust", "rust"),
        ("SQL", "sql"),
        ("Bash", "bash"),
        ("Plain Text", "text"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("pageContainer")

        self.prefs_file = os.path.join(os.path.dirname(__file__), "theme_prefs.json")
        self._tabs_data = []
        self._tab_counter = 1
        self._current_theme_name = "Monokai Dark"
        self._custom_bg_color = None

        self._load_saved_theme()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # ── Toolbar Bar ───────────────────────────────────────────────────────
        bar = QFrame()
        bar.setStyleSheet("""
            QFrame {
                background: #18191e;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                padding: 4px;
            }
        """)
        bar_layout = QHBoxLayout(bar)
        bar_layout.setContentsMargins(10, 6, 10, 6)
        bar_layout.setSpacing(10)

        self.lbl_title = QLabel("💻 Code Workspace")
        self.lbl_title.setObjectName("accentTitle")
        self.lbl_title.setStyleSheet("font-size: 14px; font-weight: 700;")
        bar_layout.addWidget(self.lbl_title)

        # New Tab Button
        self.btn_new_tab = QPushButton("➕ New Tab")
        self.btn_new_tab.setToolTip("Open new code buffer (Ctrl+T)")
        self.btn_new_tab.setStyleSheet(self._button_style())
        self.btn_new_tab.clicked.connect(lambda: self.new_tab())
        bar_layout.addWidget(self.btn_new_tab)

        bar_layout.addSpacing(6)

        # Language Selector
        lbl_lang = QLabel("Language:")
        lbl_lang.setStyleSheet("color: #a0a6b2; font-size: 11px;")
        bar_layout.addWidget(lbl_lang)

        self.lang_combo = QComboBox()
        self.lang_combo.setStyleSheet("""
            QComboBox {
                background: #272822;
                color: #00adb5;
                font-weight: 600;
                border: 1px solid #3E3D32;
                border-radius: 4px;
                padding: 4px 10px;
                min-width: 100px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background: #272822;
                color: #ffffff;
                selection-background-color: #00adb5;
                selection-color: #ffffff;
            }
        """)
        for display_name, lang_id in self.SUPPORTED_LANGUAGES:
            self.lang_combo.addItem(display_name, lang_id)
        self.lang_combo.currentIndexChanged.connect(self._on_language_changed)
        bar_layout.addWidget(self.lang_combo)

        # Theme / Background Selector
        lbl_theme = QLabel("Theme:")
        lbl_theme.setStyleSheet("color: #a0a6b2; font-size: 11px;")
        bar_layout.addWidget(lbl_theme)

        self.theme_combo = QComboBox()
        self.theme_combo.setStyleSheet("""
            QComboBox {
                background: #272822;
                color: #ffffff;
                font-weight: 600;
                border: 1px solid #3E3D32;
                border-radius: 4px;
                padding: 4px 10px;
                min-width: 110px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background: #272822;
                color: #ffffff;
                selection-background-color: #00adb5;
                selection-color: #ffffff;
            }
        """)
        for t_name in CODE_THEMES.keys():
            self.theme_combo.addItem(t_name)
        self.theme_combo.addItem("🎨 Custom Color...")
        if self._current_theme_name in CODE_THEMES:
            self.theme_combo.setCurrentText(self._current_theme_name)
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        bar_layout.addWidget(self.theme_combo)

        bar_layout.addStretch()

        # Action Buttons
        self.btn_format = QPushButton("⚡ Format")
        self.btn_format.setToolTip("Format indentation and normalize whitespace")
        self.btn_format.setStyleSheet(self._button_style())
        self.btn_format.clicked.connect(self.format_code)
        bar_layout.addWidget(self.btn_format)

        self.btn_copy = QPushButton("📋 Copy Code")
        self.btn_copy.setToolTip("Copy entire code buffer to clipboard")
        self.btn_copy.setStyleSheet(self._button_style())
        self.btn_copy.clicked.connect(self.copy_code)
        bar_layout.addWidget(self.btn_copy)

        self.btn_clear = QPushButton("🗑 Clear")
        self.btn_clear.setToolTip("Clear code editor buffer")
        self.btn_clear.setStyleSheet(self._button_style(danger=True))
        self.btn_clear.clicked.connect(self.clear_code)
        bar_layout.addWidget(self.btn_clear)

        layout.addWidget(bar)

        # ── Multi-Tab Code Workspace ──────────────────────────────────────────
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("codeTabWidget")
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self._on_tab_switched)
        self.tab_widget.setStyleSheet("""
            QTabWidget#codeTabWidget::pane {
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                background: transparent;
            }
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.04);
                color: #a0a6b2;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-bottom: none;
                padding: 6px 14px;
                margin-right: 4px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 11px;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background: rgba(0, 173, 181, 0.15);
                color: #00adb5;
                border-color: #00adb5;
            }
            QTabBar::tab:hover:!selected {
                background: rgba(255, 255, 255, 0.08);
                color: #ffffff;
            }
        """)
        layout.addWidget(self.tab_widget, 1)

        # ── Status Bar ────────────────────────────────────────────────────────
        status_bar = QFrame()
        status_bar.setStyleSheet("background: transparent; padding: 2px;")
        sb_layout = QHBoxLayout(status_bar)
        sb_layout.setContentsMargins(4, 0, 4, 0)

        self.lbl_cursor_pos = QLabel("Ln 1, Col 1")
        self.lbl_cursor_pos.setStyleSheet("color: #8e96a3; font-size: 11px;")
        sb_layout.addWidget(self.lbl_cursor_pos)

        sb_layout.addSpacing(16)

        self.lbl_stats = QLabel("Lines: 1  •  Chars: 0")
        self.lbl_stats.setStyleSheet("color: #8e96a3; font-size: 11px;")
        sb_layout.addWidget(self.lbl_stats)

        sb_layout.addStretch()

        self.lbl_feedback = QLabel("")
        self.lbl_feedback.setStyleSheet("color: #00adb5; font-size: 11px; font-weight: bold;")
        sb_layout.addWidget(self.lbl_feedback)

        self.lbl_encoding = QLabel("UTF-8  •  Tab Size: 4  •  Zoom: Ctrl+ / Ctrl-")
        self.lbl_encoding.setStyleSheet("color: #8e96a3; font-size: 11px;")
        sb_layout.addWidget(self.lbl_encoding)

        layout.addWidget(status_bar)

        # Initialize primary starter tab
        starter_code = (
            "# Alpha Tech Enterprise Multi-Tab Code Workspace\n"
            "# Multi-language syntax highlighting, custom backgrounds & real-time token parsing\n\n"
            "import math\n"
            "from typing import List, Optional\n\n"
            "class VectorEngine:\n"
            "    \"\"\"High-performance multi-dimensional vector computation engine.\"\"\"\n\n"
            "    def __init__(self, dimensions: int = 128, name: str = 'AlphaCore'):\n"
            "        self.dimensions = dimensions\n"
            "        self.name = name\n"
            "        self._weights = [0.0] * dimensions\n\n"
            "    def compute_similarity(self, vector_a: List[float], vector_b: List[float]) -> float:\n"
            "        \"\"\"Calculates cosine similarity between two feature vectors.\"\"\"\n"
            "        if len(vector_a) != len(vector_b):\n"
            "            raise ValueError('Vector dimension mismatch')\n\n"
            "        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))\n"
            "        mag_a = math.sqrt(sum(a * a for a in vector_a))\n"
            "        mag_b = math.sqrt(sum(b * b for b in vector_b))\n"
            "        return dot_product / (mag_a * mag_b) if mag_a and mag_b else 0.0\n\n"
            "if __name__ == '__main__':\n"
            "    engine = VectorEngine(dimensions=4)\n"
            "    print(f'Initialized {engine.name} with {engine.dimensions} channels.')\n"
        )
        self.new_tab(name="main.py", code=starter_code, language="python")

        # Shortcuts
        QShortcut(QKeySequence("Ctrl+T"), self, lambda: self.new_tab())
        QShortcut(QKeySequence("Ctrl+W"), self, lambda: self.close_tab(self.tab_widget.currentIndex()))
        QShortcut(QKeySequence("Ctrl+="), self, lambda: self.editor.zoomIn() if self.editor else None)
        QShortcut(QKeySequence("Ctrl++"), self, lambda: self.editor.zoomIn() if self.editor else None)
        QShortcut(QKeySequence("Ctrl+-"), self, lambda: self.editor.zoomOut() if self.editor else None)
        QShortcut(QKeySequence("Ctrl+0"), self, lambda: self.editor.resetZoom() if self.editor else None)

    # ── Tab Management ────────────────────────────────────────────────────────

    def new_tab(self, name: str = None, code: str = "", language: str = "python") -> CodeEditorWidget:
        """Creates a new code editor tab buffer."""
        if not name:
            name = f"Untitled-{self._tab_counter}.py"
            self._tab_counter += 1

        editor = CodeEditorWidget()
        editor.setPlaceholderText(f"# Write or paste code in {name}...\n")

        # Determine theme parameters
        style = "monokai"
        is_dark = True
        default_text = "#f8f8f2"
        if self._current_theme_name in CODE_THEMES:
            t = CODE_THEMES[self._current_theme_name]
            bg_q = QColor(t["bg"])
            is_dark = (bg_q.red() * 0.299 + bg_q.green() * 0.587 + bg_q.blue() * 0.114) < 128
            default_text = t["text"]
            style = t["style"]
        elif self._current_theme_name == "🎨 Custom Color..." and self._custom_bg_color:
            bg_q = QColor(self._custom_bg_color)
            is_dark = (bg_q.red() * 0.299 + bg_q.green() * 0.587 + bg_q.blue() * 0.114) < 128
            default_text = "#f8f8f2" if is_dark else "#24292e"
            style = "monokai" if is_dark else "default"

        # Attach Pygments highlighter with proper dark/light theme context
        highlighter = PygmentsHighlighter(
            editor.document(),
            language=language,
            style=style,
            is_dark=is_dark,
            default_text_color=default_text
        )

        # Apply active theme colors
        self._apply_colors_to_editor(editor, highlighter)

        if code:
            editor.setPlainText(code)

        editor.cursorPositionChanged.connect(self._update_cursor_stats)
        editor.textChanged.connect(self._update_cursor_stats)

        tab_idx = self.tab_widget.addTab(editor, f"📄 {name}")
        tab_info = {
            "editor": editor,
            "highlighter": highlighter,
            "language": language,
            "title": name
        }
        self._tabs_data.append(tab_info)
        self.tab_widget.setCurrentIndex(tab_idx)
        self._show_feedback(f"Opened tab: {name}")
        return editor

    def close_tab(self, index: int):
        """Closes tab at index. If only 1 tab remains, resets its contents."""
        if index < 0 or index >= len(self._tabs_data):
            return

        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)
            self._tabs_data.pop(index)
            self._show_feedback("Closed tab")
        else:
            self.clear_code()
            self.tab_widget.setTabText(0, "📄 Untitled-1.py")
            if self._tabs_data:
                self._tabs_data[0]["title"] = "Untitled-1.py"
            self._show_feedback("Tab reset")

    def _on_tab_switched(self, index: int):
        if 0 <= index < len(self._tabs_data):
            info = self._tabs_data[index]
            lang = info.get("language", "python")
            idx = self.lang_combo.findData(lang)
            if idx >= 0:
                self.lang_combo.blockSignals(True)
                self.lang_combo.setCurrentIndex(idx)
                self.lang_combo.blockSignals(False)
            self._update_cursor_stats()

    @property
    def current_editor(self) -> CodeEditorWidget:
        idx = self.tab_widget.currentIndex()
        if 0 <= idx < len(self._tabs_data):
            return self._tabs_data[idx]["editor"]
        return None

    @property
    def current_highlighter(self) -> PygmentsHighlighter:
        idx = self.tab_widget.currentIndex()
        if 0 <= idx < len(self._tabs_data):
            return self._tabs_data[idx]["highlighter"]
        return None

    # Backwards compatibility properties
    @property
    def editor(self) -> CodeEditorWidget:
        return self.current_editor

    @property
    def highlighter(self) -> PygmentsHighlighter:
        return self.current_highlighter

    # ── Theme & Background Customization ──────────────────────────────────────

    def _load_saved_theme(self):
        from themes import load_theme_prefs
        data = load_theme_prefs()
        self._current_theme_name = data.get("code_editor_theme", "Monokai Dark")
        self._custom_bg_color = data.get("code_editor_custom_bg")

    def _save_code_theme_prefs(self):
        from themes import save_theme_prefs
        updates = {"code_editor_theme": self._current_theme_name}
        if self._custom_bg_color:
            updates["code_editor_custom_bg"] = self._custom_bg_color
        save_theme_prefs(updates)

    def _apply_colors_to_editor(self, editor: CodeEditorWidget, highlighter: PygmentsHighlighter = None):
        if self._current_theme_name == "🎨 Custom Color..." and self._custom_bg_color:
            bg_q = QColor(self._custom_bg_color)
            is_dark = (bg_q.red() * 0.299 + bg_q.green() * 0.587 + bg_q.blue() * 0.114) < 128
            gutter_q = bg_q.darker(120) if is_dark else bg_q.lighter(105)
            line_q = bg_q.lighter(125) if is_dark else bg_q.darker(110)
            text_hex = "#f8f8f2" if is_dark else "#24292e"
            editor.set_theme_colors(bg_q.name(), gutter_q.name(), line_q.name(), text_hex)
            if highlighter:
                style = "monokai" if is_dark else "default"
                highlighter.set_theme_context(style, is_dark=is_dark, default_text_color=text_hex)
        elif self._current_theme_name in CODE_THEMES:
            t = CODE_THEMES[self._current_theme_name]
            editor.set_theme_colors(t["bg"], t["gutter"], t["line"], t["text"])
            if highlighter:
                bg_q = QColor(t["bg"])
                is_dark = (bg_q.red() * 0.299 + bg_q.green() * 0.587 + bg_q.blue() * 0.114) < 128
                highlighter.set_theme_context(t["style"], is_dark=is_dark, default_text_color=t["text"])

    def _on_theme_changed(self, name: str):
        if name == "🎨 Custom Color...":
            init_c = QColor(self._custom_bg_color or "#272822")
            color = QColorDialog.getColor(init_c, self, "Select Code Editor Background Color")
            if color.isValid():
                self._current_theme_name = "🎨 Custom Color..."
                self._custom_bg_color = color.name()
                self._save_code_theme_prefs()
                for tab in self._tabs_data:
                    self._apply_colors_to_editor(tab["editor"], tab.get("highlighter"))
                self._show_feedback(f"Custom background applied: {color.name()}")
            else:
                self.theme_combo.blockSignals(True)
                self.theme_combo.setCurrentText(self._current_theme_name)
                self.theme_combo.blockSignals(False)
            return

        if name in CODE_THEMES:
            self._current_theme_name = name
            self._save_code_theme_prefs()
            for tab in self._tabs_data:
                self._apply_colors_to_editor(tab["editor"], tab.get("highlighter"))
            self._show_feedback(f"Code theme changed to {name}")

    def set_editor_background(self, hex_color: str):
        """Public API to programmatically set code editor background color."""
        self._current_theme_name = "🎨 Custom Color..."
        self._custom_bg_color = hex_color
        self._save_code_theme_prefs()
        for tab in self._tabs_data:
            self._apply_colors_to_editor(tab["editor"], tab.get("highlighter"))

    # ── AI Code Copilot Insertion API ─────────────────────────────────────────

    def insert_code_at_cursor(self, text: str):
        """Inserts generated AI code directly into the active editor buffer at the cursor."""
        ed = self.current_editor
        if ed:
            cursor = ed.textCursor()
            cursor.insertText(text)
            ed.setTextCursor(cursor)
            self._show_feedback("✓ Inserted code from AI Copilot")

    def replace_code_selection(self, text: str):
        """Replaces current selection (or entire buffer) with AI generated code."""
        ed = self.current_editor
        if ed:
            cursor = ed.textCursor()
            if cursor.hasSelection():
                cursor.insertText(text)
            else:
                ed.setPlainText(text)
            self._show_feedback("✓ Replaced code from AI Copilot")

    # ── Public APIs & Handlers ────────────────────────────────────────────────

    def _button_style(self, danger: bool = False) -> str:
        if danger:
            return """
                QPushButton {
                    background: rgba(220, 53, 69, 0.15);
                    color: #ff6b6b;
                    border: 1px solid rgba(220, 53, 69, 0.3);
                    border-radius: 4px;
                    padding: 5px 12px;
                    font-size: 11px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: rgba(220, 53, 69, 0.35);
                    border-color: #ff6b6b;
                }
            """
        accent = getattr(self, "_theme_accent", "#00adb5")
        return f"""
            QPushButton {{
                background: rgba(255, 255, 255, 0.05);
                color: {accent};
                border: 1px solid {accent};
                border-radius: 4px;
                padding: 5px 12px;
                font-size: 11px;
                font-weight: 600;
                margin-top: 2px;
                margin-bottom: 0px;
            }}
            QPushButton:hover {{
                background: {accent};
                color: #ffffff;
                margin-top: 0px;
                margin-bottom: 2px;
            }}
            QPushButton:pressed {{
                margin-top: 3px;
                margin-bottom: -1px;
            }}
        """

    def set_theme_accent(self, accent_hex: str):
        """Dynamically updates code editor accent glows."""
        self._theme_accent = accent_hex
        if hasattr(self, "lbl_title"):
            self.lbl_title.setStyleSheet(f"font-size: 14px; font-weight: 700; color: {accent_hex};")
        if hasattr(self, "lbl_feedback"):
            self.lbl_feedback.setStyleSheet(f"color: {accent_hex}; font-size: 11px; font-weight: bold;")
        if hasattr(self, "btn_format"):
            self.btn_format.setStyleSheet(self._button_style())
        if hasattr(self, "btn_copy"):
            self.btn_copy.setStyleSheet(self._button_style())
        if hasattr(self, "btn_new_tab"):
            self.btn_new_tab.setStyleSheet(f"""
                QPushButton {{
                    background: rgba(255, 255, 255, 0.06);
                    border: 1px solid {accent_hex};
                    color: {accent_hex};
                    font-weight: 700;
                    padding: 4px 10px;
                    border-radius: 4px;
                    font-size: 11px;
                    margin-top: 2px;
                    margin-bottom: 0px;
                }}
                QPushButton:hover {{
                    background: {accent_hex};
                    color: #ffffff;
                    margin-top: 0px;
                    margin-bottom: 2px;
                }}
                QPushButton:pressed {{
                    margin-top: 3px;
                    margin-bottom: -1px;
                }}
            """)
        if hasattr(self, "tab_widget"):
            self.tab_widget.setStyleSheet(f"""
                QTabWidget::pane {{
                    border: 1px solid #3E3D32;
                    background: #272822;
                    border-radius: 6px;
                }}
                QTabBar::tab {{
                    background: rgba(255, 255, 255, 0.04);
                    color: #8e96a3;
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-bottom: none;
                    padding: 6px 14px;
                    margin-right: 4px;
                    border-top-left-radius: 6px;
                    border-top-right-radius: 6px;
                    font-size: 11px;
                    font-weight: 600;
                }}
                QTabBar::tab:selected {{
                    background: rgba(255, 255, 255, 0.12);
                    color: {accent_hex};
                    border-color: {accent_hex};
                }}
                QTabBar::tab:hover:!selected {{
                    background: rgba(255, 255, 255, 0.08);
                    color: #ffffff;
                }}
            """)
        # Update all open tab editors' gutter line number accent
        for t_info in getattr(self, "_tabs_data", []):
            ed = t_info.get("editor")
            if ed:
                ed._theme_accent = accent_hex
                if hasattr(ed, "line_number_area"):
                    ed.line_number_area.update()

    def _on_language_changed(self, index: int):
        lang_id = self.lang_combo.itemData(index)
        if lang_id and self.current_highlighter:
            self.current_highlighter.set_language(lang_id)
            idx = self.tab_widget.currentIndex()
            if 0 <= idx < len(self._tabs_data):
                self._tabs_data[idx]["language"] = lang_id
            self._show_feedback(f"Language changed to {self.lang_combo.currentText()}")

    def _update_cursor_stats(self):
        ed = self.current_editor
        if not ed:
            return
        cursor = ed.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.positionInBlock() + 1
        self.lbl_cursor_pos.setText(f"Ln {line}, Col {col}")

        lines = ed.blockCount()
        chars = len(ed.toPlainText())
        self.lbl_stats.setText(f"Lines: {lines:,}  •  Chars: {chars:,}")

    def _show_feedback(self, msg: str, duration_ms: int = 2500):
        self.lbl_feedback.setText(msg)
        QTimer.singleShot(duration_ms, lambda: self.lbl_feedback.setText(""))

    def copy_code(self):
        ed = self.current_editor
        if ed and ed.toPlainText():
            QApplication.clipboard().setText(ed.toPlainText())
            self._show_feedback("✓ Code copied to clipboard!")
        else:
            self._show_feedback("Editor is empty", 1500)

    def format_code(self):
        ed = self.current_editor
        if not ed or not ed.toPlainText().strip():
            return

        current_lang = self.lang_combo.itemData(self.lang_combo.currentIndex())
        text = ed.toPlainText()

        if current_lang == "json":
            try:
                parsed = json.loads(text)
                formatted = json.dumps(parsed, indent=4)
                ed.setPlainText(formatted)
                self._show_feedback("✓ Formatted JSON")
                return
            except Exception as e:
                self._show_feedback(f"JSON Error: {e}", 3000)
                return

        # Generic code cleanup: normalize tabs to 4 spaces, strip trailing whitespace
        lines = [line.replace("\t", "    ").rstrip() for line in text.split("\n")]
        ed.setPlainText("\n".join(lines))
        self._show_feedback("✓ Indentation normalized")

    def clear_code(self):
        ed = self.current_editor
        if ed:
            ed.clear()
            self._show_feedback("Editor buffer cleared")

    def set_code(self, code: str, language: str = None):
        ed = self.current_editor
        if ed:
            ed.setPlainText(code)
        if language:
            idx = self.lang_combo.findData(language)
            if idx >= 0:
                self.lang_combo.setCurrentIndex(idx)

    def get_code(self) -> str:
        ed = self.current_editor
        return ed.toPlainText() if ed else ""
