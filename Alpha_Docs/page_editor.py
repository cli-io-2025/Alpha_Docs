"""
page_editor.py — Academic & Enterprise Document Editor Page
Combines RibbonToolbar, HorizontalRulerBar, DocumentViewEngine, EnterpriseSideDrawer,
DocumentPresets, and DocumentIOEngine into a full enterprise editing workspace.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame,
    QInputDialog, QLineEdit, QColorDialog, QMessageBox, QFileDialog, QMenu,
    QSplitter
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import (
    QFont, QTextBlockFormat, QTextCharFormat, QColor, QKeySequence,
    QShortcut, QTextCursor, QTextListFormat
)

from document_view_engine import DocumentViewEngine
from toolbar_ribbon import RibbonToolbar
from ruler_bar import HorizontalRulerBar
from side_panels import EnterpriseSideDrawer
from document_presets import PRESETS, apply_preset_to_editor
from document_io import DocumentIOEngine, ExportDialog
from pyspell_integration import SpellHighlighter
from find_replace_bar import FindReplaceBar


class DocumentEditorPage(QWidget):
    """Enterprise Document Editor Page Component."""

    save_requested = Signal(str, str)
    expansion_requested = Signal(dict)

    @property
    def apa_body_format(self) -> QTextBlockFormat:
        fmt = QTextBlockFormat()
        fmt.setLineHeight(200.0, QTextBlockFormat.LineHeightTypes.ProportionalHeight.value)
        fmt.setTextIndent(36)
        return fmt

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("pageContainer")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(6)

        # 1. Top Formatting Ribbon
        self.ribbon = RibbonToolbar()
        main_layout.addWidget(self.ribbon)

        # 2. Main Editing Splitter (Canvas + Side Drawer)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left Canvas Workspace
        canvas_container = QWidget()
        canvas_layout = QVBoxLayout(canvas_container)
        canvas_layout.setContentsMargins(0, 0, 0, 0)
        canvas_layout.setSpacing(0)

        # Horizontal Ruler Bar
        self.ruler = HorizontalRulerBar()
        canvas_layout.addWidget(self.ruler)

        # Inline Find & Replace Bar (hidden by default)
        self.find_bar = FindReplaceBar()
        self.find_bar.hide()
        self.find_bar.find_next_requested.connect(self._on_find_next)
        self.find_bar.find_prev_requested.connect(self._on_find_prev)
        self.find_bar.replace_requested.connect(self._on_replace_action)
        self.find_bar.replace_all_requested.connect(self._on_replace_all_action)
        canvas_layout.addWidget(self.find_bar)

        # Custom Paged Document Engine
        self.editor = DocumentViewEngine()
        self.editor.setObjectName("documentViewEngine")
        canvas_layout.addWidget(self.editor, 1)

        self.splitter.addWidget(canvas_container)

        # Right Side Drawer Panel
        self.side_drawer = EnterpriseSideDrawer()
        self.side_drawer.heading_selected.connect(self._navigate_to_position)
        self.splitter.addWidget(self.side_drawer)

        # Set initial splitter sizes (Canvas 80%, Side Drawer 20%)
        self.splitter.setSizes([850, 250])
        main_layout.addWidget(self.splitter, 1)

        # Apply default APA preset parameters
        self.page_width_mm = 215.9
        self.page_height_mm = 279.4
        self.editor.setPageSizeMM(self.page_width_mm, self.page_height_mm)
        self.editor.setMarginsMM(25.4, 25.4, 25.4, 25.4)

        apply_preset_to_editor("APA 7th Edition (Academic)", self)
        self._update_ruler_params()

        # Connect Ribbon Signals
        self._wire_ribbon_signals()
        self.editor.cursorPositionChanged.connect(self._on_cursor_position_changed)
        self.editor.horizontalScrollBar().valueChanged.connect(self.ruler.set_scroll_offset)

        # Keyboard Shortcuts
        self._setup_shortcuts()

        # Real-time Spell Highlighter & Analytics Debounce Timer
        doc = self.editor.document()
        self.spell_highlighter = SpellHighlighter(doc)

        self.metrics_timer = QTimer(self)
        self.metrics_timer.setSingleShot(True)
        self.metrics_timer.setInterval(400)
        self.metrics_timer.timeout.connect(self._refresh_side_panels)

        doc.contentsChanged.connect(self.metrics_timer.start)
        self._refresh_side_panels()

    def _update_ruler_params(self):
        margins = self.editor.marginsPoints()
        top_m_mm = margins.top() / 72.0 * 25.4
        left_m_mm = margins.left() / 72.0 * 25.4
        right_m_mm = margins.right() / 72.0 * 25.4
        page_w_mm = self.editor.pageSizePoints().width() / 72.0 * 25.4
        self.ruler.set_ruler_params(left_m_mm, right_m_mm, page_w_mm, self.editor.zoomFactor())

    def _wire_ribbon_signals(self):
        rb = self.ribbon

        # Font & Text Formatting
        rb.font_family_changed.connect(self._on_font_family_changed)
        rb.font_size_changed.connect(self._on_font_size_changed)
        rb.bold_toggled.connect(self._on_bold_toggled)
        rb.italic_toggled.connect(self._on_italic_toggled)
        rb.underline_toggled.connect(self._on_underline_toggled)
        rb.strikethrough_toggled.connect(self._on_strikethrough_toggled)
        rb.text_color_changed.connect(self._on_text_color_changed)
        rb.highlight_color_changed.connect(self._on_highlight_color_changed)
        rb.clear_formatting_requested.connect(self._on_clear_formatting)

        # Alignment
        rb.align_left_requested.connect(lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignLeft))
        rb.align_center_requested.connect(lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignCenter))
        rb.align_right_requested.connect(lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignRight))
        rb.align_justify_requested.connect(lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignJustify))

        # Lists & Indents
        rb.bullet_list_requested.connect(self.editor.toggleBulletList)
        rb.numbered_list_requested.connect(self.editor.toggleNumberedList)
        rb.indent_requested.connect(self.editor.indentList)
        rb.outdent_requested.connect(self.editor.unindentList)
        rb.line_spacing_changed.connect(self._on_line_spacing_changed)

        # Heading Styles
        rb.heading_style_changed.connect(self._on_heading_style_changed)

        # Insertion
        rb.insert_table_requested.connect(self.editor.insertTable)
        rb.insert_image_requested.connect(self.editor.insertImage)
        rb.insert_divider_requested.connect(self._on_insert_divider)
        rb.insert_page_break_requested.connect(self._on_insert_page_break)
        rb.insert_link_requested.connect(self.editor.insertLink)

        # AI Copilot Actions
        rb.ai_summarize_requested.connect(
            lambda: self._trigger_ai_action("Summarize", "Please provide a concise, high-level summary of this content.")
        )
        rb.ai_rephrase_requested.connect(
            lambda: self._trigger_ai_action("Rephrase", "Please rephrase and refine the tone of the selected content for clarity and elegance.")
        )
        rb.ai_grammar_requested.connect(
            lambda: self._trigger_ai_action("Grammar Check", "Please proofread the text, identifying and fixing any grammatical, spelling, or punctuation errors.")
        )

        # Presets & Layout
        rb.preset_changed.connect(lambda p: (apply_preset_to_editor(p, self), self._update_ruler_params()))
        rb.margin_preset_changed.connect(self._on_margin_preset_changed)
        rb.page_size_changed.connect(self._on_page_size_changed)
        rb.cursor_style_changed.connect(self.editor.setCursorStyle)
        rb.caret_style_changed.connect(self.editor.setCaretStyle)
        rb.pointer_style_changed.connect(self.editor.setPointerStyle)

        # Side panel drawer toggles
        rb.toggle_side_panel_requested.connect(self.side_drawer.show_panel)

        # Search & Export Dialog
        rb.find_requested.connect(lambda: self.find_bar.open_find(show_replace=False, prefill_text=self.editor.cursor().selectedText()))
        rb.export_dialog_requested.connect(self._on_open_export_dialog)

        # Canvas Zoom
        rb.zoom_in_requested.connect(self._zoom_in)
        rb.zoom_out_requested.connect(self._zoom_out)
        rb.zoom_reset_requested.connect(self._zoom_reset)
        self.editor.zoom_changed.connect(self._on_zoom_changed)

    def _setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+B"), self, lambda: self._on_bold_toggled(not self.editor.cursor().charFormat().fontWeight() == QFont.Weight.Bold))
        QShortcut(QKeySequence("Ctrl+I"), self, lambda: self._on_italic_toggled(not self.editor.cursor().charFormat().fontItalic()))
        QShortcut(QKeySequence("Ctrl+U"), self, lambda: self._on_underline_toggled(not self.editor.cursor().charFormat().fontUnderline()))
        QShortcut(QKeySequence("Ctrl+S"), self, self._on_save_document)
        QShortcut(QKeySequence("Ctrl+P"), self, self._on_export_pdf)
        QShortcut(QKeySequence("Ctrl+E"), self, self._on_open_export_dialog)
        QShortcut(QKeySequence("Ctrl+F"), self, lambda: self.find_bar.open_find(show_replace=False, prefill_text=self.editor.cursor().selectedText()))
        QShortcut(QKeySequence("Ctrl+H"), self, lambda: self.find_bar.open_find(show_replace=True, prefill_text=self.editor.cursor().selectedText()))
        # Zoom shortcuts
        QShortcut(QKeySequence("Ctrl+="), self, self.editor.zoomIn)
        QShortcut(QKeySequence("Ctrl++"), self, self.editor.zoomIn)
        QShortcut(QKeySequence("Ctrl+-"), self, self.editor.zoomOut)
        QShortcut(QKeySequence("Ctrl+0"), self, self.editor.resetZoom)

    # ── FORMATTING HANDLERS ───────────────────────────────────────────────────
    def _on_font_family_changed(self, family: str):
        self.editor.setFontFamily(family)

    def _on_font_size_changed(self, size: int):
        self.editor.setFontSize(size)

    def _on_bold_toggled(self, bold: bool):
        self.editor.setBold(bold)

    def _on_italic_toggled(self, italic: bool):
        self.editor.setItalic(italic)

    def _on_underline_toggled(self, underline: bool):
        self.editor.setUnderline(underline)

    def _on_strikethrough_toggled(self, strike: bool):
        cursor = self.editor.cursor()
        fmt = cursor.charFormat()
        fmt.setFontStrikeOut(strike)
        cursor.mergeCharFormat(fmt)
        self.editor._set_cursor(cursor)

    def _on_text_color_changed(self, color: QColor):
        self.editor.setTextColor(color)

    def _on_highlight_color_changed(self, color: QColor):
        self.editor.setHighlightColor(color)

    def _on_clear_formatting(self):
        cursor = self.editor.cursor()
        default_fmt = QTextCharFormat()
        default_fmt.setFont(QFont("Times New Roman", 12))
        default_fmt.setForeground(Qt.GlobalColor.black)
        cursor.setCharFormat(default_fmt)
        self.editor._set_cursor(cursor)

    def _on_line_spacing_changed(self, spacing: float):
        cursor = self.editor.cursor()
        block_fmt = cursor.blockFormat()
        block_fmt.setLineHeight(spacing * 100.0, QTextBlockFormat.LineHeightTypes.ProportionalHeight.value)
        cursor.setBlockFormat(block_fmt)
        self.editor._set_cursor(cursor)

    def _on_heading_style_changed(self, style_name: str):
        if style_name == "Heading 1":
            self.editor.setHeaderFormat(1)
        elif style_name == "Heading 2":
            self.editor.setHeaderFormat(2)
        elif style_name == "Heading 3":
            self.editor.setHeaderFormat(3)
        elif style_name == "Title":
            self.editor.setFontSize(24)
            self.editor.setBold(True)
        elif style_name == "Subtitle":
            self.editor.setFontSize(16)
            self.editor.setItalic(True)
        else:
            self.editor.setHeaderFormat(0)

    def _on_insert_divider(self):
        cursor = self.editor.cursor()
        cursor.insertHtml("<hr style='border: 1px solid rgba(255,255,255,0.2);' />")
        self.editor._set_cursor(cursor)

    def _on_insert_page_break(self):
        cursor = self.editor.cursor()
        cursor.insertBlock()
        block_fmt = cursor.blockFormat()
        block_fmt.setPageBreakPolicy(QTextBlockFormat.PageBreakFlag.PageBreak_AlwaysBefore)
        cursor.setBlockFormat(block_fmt)
        self.editor._set_cursor(cursor)

    def _on_margin_preset_changed(self, margin_name: str):
        if "Narrow" in margin_name:
            self.editor.setMarginsMM(12.7, 12.7, 12.7, 12.7)
        elif "Wide" in margin_name:
            self.editor.setMarginsMM(25.4, 25.4, 38.1, 38.1)
        else:
            self.editor.setMarginsMM(25.4, 25.4, 25.4, 25.4)
        self._update_ruler_params()

    def _on_page_size_changed(self, size_name: str):
        if "A4" in size_name:
            self.page_width_mm, self.page_height_mm = 210.0, 297.0
        elif "Legal" in size_name:
            self.page_width_mm, self.page_height_mm = 215.9, 355.6
        elif "Executive" in size_name:
            self.page_width_mm, self.page_height_mm = 184.15, 266.7
        else:
            self.page_width_mm, self.page_height_mm = 215.9, 279.4
        self.editor.setPageSizeMM(self.page_width_mm, self.page_height_mm)
        self._update_ruler_params()

    # ── FILE IO & HELPERS ─────────────────────────────────────────────────────
    def _on_save_document(self) -> bool:
        title, ok = QInputDialog.getText(self, "Save Document", "Enter document name:", QLineEdit.EchoMode.Normal, "my_docs_1")
        if ok and title:
            content = self.editor.document().toHtml()
            self.save_requested.emit(title, content)
            return True
        return False

    def _on_export_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export PDF", "", "PDF Files (*.pdf)")
        if file_path:
            success = DocumentIOEngine.export_pdf(self.editor.document(), file_path)
            if success:
                QMessageBox.information(self, "Export Complete", f"PDF exported successfully to:\n{file_path}")

    def _navigate_to_position(self, pos: int):
        cursor = self.editor.cursor()
        cursor.setPosition(pos)
        self.editor._set_cursor(cursor)
        self.editor.setFocus()

    def _on_cursor_position_changed(self):
        cursor = self.editor.cursor()
        self.ribbon.update_formatting_state(cursor.charFormat(), cursor.blockFormat())

    def _refresh_side_panels(self):
        self.side_drawer.refresh_data(self.editor.document())

    def get_prompt_context(self) -> dict:
        cursor = self.editor.cursor()
        selected = cursor.selectedText().replace('\u2029', '\n')
        current_para = cursor.block().text()
        full_doc = self.editor.document().toPlainText()
        return {
            "selected_text": selected,
            "current_paragraph": current_para,
            "full_document": full_doc
        }

    def _trigger_ai_action(self, action_name: str, instruction: str):
        ctx = self.get_prompt_context()
        ctx["action"] = action_name
        ctx["instruction"] = instruction
        self.expansion_requested.emit(ctx)

    def insert_generation(self, text: str):
        cursor = self.editor.cursor()
        cursor.insertText(text)
        self.editor._set_cursor(cursor)
        self.editor.setFocus()

    def replace_selection(self, text: str):
        cursor = self.editor.cursor()
        if cursor.hasSelection():
            cursor.removeSelectedText()
        cursor.insertText(text)
        self.editor._set_cursor(cursor)
        self.editor.setFocus()

    # ── FIND & REPLACE HANDLERS ───────────────────────────────────────────────
    def _on_find_next(self, text: str, match_case: bool, whole_word: bool):
        current, total = self.editor.find_text(text, forward=True, match_case=match_case, whole_word=whole_word)
        self.find_bar.set_match_status(current, total)

    def _on_find_prev(self, text: str, match_case: bool, whole_word: bool):
        current, total = self.editor.find_text(text, forward=False, match_case=match_case, whole_word=whole_word)
        self.find_bar.set_match_status(current, total)

    def _on_replace_action(self, find_text: str, replace_text: str, match_case: bool, whole_word: bool):
        self.editor.replace_text(find_text, replace_text, match_case=match_case, whole_word=whole_word)
        self._on_find_next(find_text, match_case, whole_word)

    def _on_replace_all_action(self, find_text: str, replace_text: str, match_case: bool, whole_word: bool):
        count = self.editor.replace_all(find_text, replace_text, match_case=match_case, whole_word=whole_word)
        QMessageBox.information(self, "Replace All", f"Replaced {count} occurrences of '{find_text}'.")
        self.find_bar.set_match_status(0, 0)

    # ── EXPORT & ZOOM HANDLERS ────────────────────────────────────────────────
    def _on_open_export_dialog(self):
        dlg = ExportDialog(self.editor.document(), self)
        dlg.exec()

    def _zoom_in(self):
        self.editor.setZoomFactor(self.editor.zoomFactor() + 0.1)

    def _zoom_out(self):
        self.editor.setZoomFactor(self.editor.zoomFactor() - 0.1)

    def _zoom_reset(self):
        self.editor.setZoomFactor(1.0)

    def _on_zoom_changed(self, factor: float):
        self._update_ruler_params()
        self.ribbon.lbl_zoom_val.setText(f"{int(factor * 100)}%")

    def set_theme_accent(self, accent_hex: str) -> None:
        """Propagates theme accent across editor components (ribbon, find bar, canvas)."""
        self._theme_accent = accent_hex
        if hasattr(self, "find_bar") and hasattr(self.find_bar, "set_theme_accent"):
            self.find_bar.set_theme_accent(accent_hex)
        if hasattr(self, "editor") and hasattr(self.editor, "set_theme_accent"):
            self.editor.set_theme_accent(accent_hex)
        if hasattr(self, "ribbon") and hasattr(self.ribbon, "set_theme_accent"):
            self.ribbon.set_theme_accent(accent_hex)
