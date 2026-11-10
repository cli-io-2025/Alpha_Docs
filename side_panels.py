"""
side_panels.py — Enterprise Side Panel Drawers for Alpha Docs Tool
Provides Outline Document Navigation, Live Analytics & Readability Metrics,
and Inline Comments / Revision Tracking drawers.
"""

import math
import re
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QLabel, QPushButton, QFrame, QStackedWidget, QTextEdit, QListWidget,
    QListWidgetItem, QLineEdit, QGroupBox, QFormLayout
)
from PySide6.QtCore import Qt, Signal, QDateTime
from PySide6.QtGui import QTextDocument, QTextCursor, QFont, QColor


class OutlineNavigationPanel(QWidget):
    """Auto-generates a document outline tree from headings for instant click-navigation."""

    heading_selected = Signal(int) # emits document position of the heading

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        lbl = QLabel("DOCUMENT OUTLINE")
        lbl.setStyleSheet("font-weight: bold; font-size: 11px; opacity: 0.7;")
        layout.addWidget(lbl)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setStyleSheet("""
            QTreeWidget {
                background: rgba(0, 0, 0, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 6px;
            }
            QTreeWidget::item {
                padding: 4px;
            }
        """)
        self.tree.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.tree)

    def refresh_outline(self, doc: QTextDocument):
        """Scans document blocks and builds outline hierarchy."""
        self.tree.clear()
        if not doc:
            return

        block = doc.begin()
        root_item = self.tree.invisibleRootItem()
        current_h1 = None
        current_h2 = None

        while block.isValid():
            text = block.text().strip()
            fmt = block.blockFormat()
            heading_level = fmt.headingLevel()
            
            # Fallback heuristic if heading level isn't set: inspect font size or bold style
            if heading_level == 0 and text:
                cursor = QTextCursor(block)
                char_fmt = cursor.charFormat()
                font_size = char_fmt.fontPointSize()
                if font_size <= 0:
                    font_size = char_fmt.font().pointSizeF()
                if font_size <= 0:
                    font_size = 12.0
                is_bold = char_fmt.font().bold() or char_fmt.fontWeight() >= 700
                if font_size >= 18:
                    heading_level = 1
                elif font_size >= 14:
                    heading_level = 2
                elif font_size >= 12 and is_bold:
                    heading_level = 3

            if heading_level > 0 and text:
                item = QTreeWidgetItem()
                item.setText(0, text[:40] + ("..." if len(text) > 40 else ""))
                item.setData(0, Qt.ItemDataRole.UserRole, block.position())

                if heading_level == 1 or current_h1 is None:
                    root_item.addChild(item)
                    current_h1 = item
                    current_h2 = None
                elif heading_level == 2:
                    current_h1.addChild(item)
                    current_h1.setExpanded(True)
                    current_h2 = item
                else:
                    parent_node = current_h2 if current_h2 else current_h1
                    parent_node.addChild(item)
                    parent_node.setExpanded(True)

            block = block.next()

    def _on_item_clicked(self, item: QTreeWidgetItem, col: int):
        pos = item.data(0, Qt.ItemDataRole.UserRole)
        if pos is not None:
            self.heading_selected.emit(pos)


class DocumentAnalyticsPanel(QWidget):
    """Calculates and displays real-time document metrics & readability scores."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        lbl = QLabel("LIVE DOCUMENT METRICS")
        lbl.setStyleSheet("font-weight: bold; font-size: 11px; opacity: 0.7;")
        layout.addWidget(lbl)

        form = QFormLayout()
        self.lbl_words = QLabel("0")
        self.lbl_chars = QLabel("0")
        self.lbl_chars_no_space = QLabel("0")
        self.lbl_paragraphs = QLabel("0")
        self.lbl_read_time = QLabel("0 min")
        self.lbl_readability = QLabel("N/A")

        form.addRow("Word Count:", self.lbl_words)
        form.addRow("Characters:", self.lbl_chars)
        form.addRow("Chars (no space):", self.lbl_chars_no_space)
        form.addRow("Paragraphs:", self.lbl_paragraphs)
        form.addRow("Reading Time:", self.lbl_read_time)
        form.addRow("Readability (Flesch):", self.lbl_readability)

        box = QGroupBox("Metrics Summary")
        box.setLayout(form)
        layout.addWidget(box)
        layout.addStretch()

    def update_metrics(self, doc: QTextDocument):
        if not doc:
            return
        text = doc.toPlainText()
        
        words = len(re.findall(r'\b\w+\b', text))
        chars = len(text)
        chars_no_space = len(text.replace(' ', '').replace('\n', ''))
        
        paragraphs = 0
        block = doc.begin()
        while block.isValid():
            if block.text().strip():
                paragraphs += 1
            block = block.next()

        read_time_mins = math.ceil(words / 200.0) if words > 0 else 0

        # Calculate Flesch Reading Ease score
        sentences = max(1, len(re.split(r'[.!?]+', text)))
        words_count = max(1, words)
        syllables = sum([len(re.findall(r'[aeiouyAEIOUY]+', w)) for w in re.findall(r'\b\w+\b', text)])
        syllables = max(1, syllables)

        flesch = 206.835 - 1.015 * (words_count / sentences) - 84.6 * (syllables / words_count)
        flesch_score = round(max(0, min(100, flesch)), 1) if words > 10 else "N/A"

        self.lbl_words.setText(f"{words:,}")
        self.lbl_chars.setText(f"{chars:,}")
        self.lbl_chars_no_space.setText(f"{chars_no_space:,}")
        self.lbl_paragraphs.setText(f"{paragraphs:,}")
        self.lbl_read_time.setText(f"~{read_time_mins} min")
        self.lbl_readability.setText(f"{flesch_score}" + (" / 100" if isinstance(flesch_score, float) else ""))


class CommentsPanel(QWidget):
    """Allows adding and resolving inline comments tied to document text selections."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        lbl = QLabel("DOCUMENT COMMENTS & REVISIONS")
        lbl.setStyleSheet("font-weight: bold; font-size: 11px; opacity: 0.7;")
        layout.addWidget(lbl)

        self.comment_input = QLineEdit()
        self.comment_input.setPlaceholderText("Add a comment to selection...")
        layout.addWidget(self.comment_input)

        btn_add = QPushButton("+ Add Comment")
        btn_add.clicked.connect(self._add_comment)
        layout.addWidget(btn_add)

        self.comments_list = QListWidget()
        self.comments_list.setStyleSheet("background: rgba(0,0,0,0.15); border-radius: 6px;")
        layout.addWidget(self.comments_list)

    def _add_comment(self):
        text = self.comment_input.text().strip()
        if not text:
            return
        dt = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm")
        item_text = f"💬 [{dt}]\n{text}"
        item = QListWidgetItem(item_text)
        self.comments_list.addItem(item)
        self.comment_input.clear()


class EnterpriseSideDrawer(QWidget):
    """Unified Side Panel Drawer containing Outline, Analytics, and Comments."""

    heading_selected = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(200)
        self.setMaximumWidth(500)
        self.setStyleSheet("""
            QWidget#enterpriseDrawer {
                background: rgba(18, 20, 26, 0.95);
                border-left: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        self.setObjectName("enterpriseDrawer")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        # Tab Selector Bar
        tab_bar = QHBoxLayout()
        self.btn_outline = QPushButton("Outline")
        self.btn_analytics = QPushButton("Analytics")
        self.btn_comments = QPushButton("Comments")

        for btn in [self.btn_outline, self.btn_analytics, self.btn_comments]:
            btn.setFixedHeight(28)
            tab_bar.addWidget(btn)

        layout.addLayout(tab_bar)

        self.stack = QStackedWidget()
        self.outline_panel = OutlineNavigationPanel()
        self.outline_panel.heading_selected.connect(self.heading_selected.emit)

        self.analytics_panel = DocumentAnalyticsPanel()
        self.comments_panel = CommentsPanel()

        self.stack.addWidget(self.outline_panel)
        self.stack.addWidget(self.analytics_panel)
        self.stack.addWidget(self.comments_panel)

        layout.addWidget(self.stack)

        self.btn_outline.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_analytics.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_comments.clicked.connect(lambda: self.stack.setCurrentIndex(2))

    def show_panel(self, panel_name: str):
        if panel_name == "outline":
            self.stack.setCurrentIndex(0)
        elif panel_name == "analytics":
            self.stack.setCurrentIndex(1)
        elif panel_name == "comments":
            self.stack.setCurrentIndex(2)

    def refresh_data(self, doc: QTextDocument):
        self.outline_panel.refresh_outline(doc)
        self.analytics_panel.update_metrics(doc)
