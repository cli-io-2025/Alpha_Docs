"""
toolbar_ribbon.py — Enterprise Formatting Ribbon Toolbar for Alpha Docs Tool
Provides modern tabbed formatting controls, font styling, paragraph alignment,
table/image insertion, layout presets, and AI action buttons.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QToolButton,
    QComboBox, QFontComboBox, QSpinBox, QColorDialog, QInputDialog,
    QFileDialog, QMenu, QLabel, QFrame, QSizePolicy, QDialog,
    QDialogButtonBox, QFormLayout
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QFont, QColor, QIcon, QTextCharFormat, QTextBlockFormat


class InsertTableDialog(QDialog):
    """Dialog for entering table rows and columns."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Insert Table")
        self.setFixedWidth(240)
        
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(1, 50)
        self.rows_spin.setValue(3)
        form.addRow("Rows:", self.rows_spin)
        
        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(1, 20)
        self.cols_spin.setValue(3)
        form.addRow("Columns:", self.cols_spin)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_dimensions(self) -> tuple[int, int]:
        return self.rows_spin.value(), self.cols_spin.value()


class RibbonGroup(QFrame):
    """A visually distinct group box within a ribbon tab."""
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setObjectName("ribbonGroup")
        self.setStyleSheet("""
            QFrame#ribbonGroup {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 6px;
                margin: 1px 2px;
                padding: 2px 4px;
            }
        """)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(4, 3, 4, 2)
        self.main_layout.setSpacing(2)
        
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(4)
        self.main_layout.addLayout(self.content_layout)
        
        lbl = QLabel(title)
        lbl.setFixedHeight(13)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size: 9px; opacity: 0.7; font-weight: bold; letter-spacing: 0.3px;")
        self.main_layout.addWidget(lbl)


class RibbonToolbar(QWidget):
    """Enterprise tabbed ribbon toolbar."""

    # Signal emissions for editor actions
    font_family_changed = Signal(str)
    font_size_changed = Signal(int)
    bold_toggled = Signal(bool)
    italic_toggled = Signal(bool)
    underline_toggled = Signal(bool)
    strikethrough_toggled = Signal(bool)
    text_color_changed = Signal(QColor)
    highlight_color_changed = Signal(QColor)
    clear_formatting_requested = Signal()

    align_left_requested = Signal()
    align_center_requested = Signal()
    align_right_requested = Signal()
    align_justify_requested = Signal()

    bullet_list_requested = Signal()
    numbered_list_requested = Signal()
    indent_requested = Signal()
    outdent_requested = Signal()
    line_spacing_changed = Signal(float)

    heading_style_changed = Signal(str)

    insert_table_requested = Signal(int, int)
    insert_image_requested = Signal(str)
    insert_divider_requested = Signal()
    insert_page_break_requested = Signal()
    insert_link_requested = Signal(str, str)

    preset_changed = Signal(str)
    margin_preset_changed = Signal(str)
    page_size_changed = Signal(str)

    find_requested = Signal()
    replace_requested = Signal()
    export_dialog_requested = Signal()
    zoom_in_requested = Signal()
    zoom_out_requested = Signal()
    zoom_reset_requested = Signal()

    ai_summarize_requested = Signal()
    ai_rephrase_requested = Signal()
    ai_grammar_requested = Signal()
    toggle_side_panel_requested = Signal(str)
    cursor_style_changed = Signal(str)
    caret_style_changed = Signal(str)
    pointer_style_changed = Signal(str)
    help_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(134)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(255, 255, 255, 0.1);
                background: rgba(18, 20, 26, 0.85);
                border-radius: 8px;
            }
            QTabBar::tab {
                padding: 6px 14px;
                font-weight: 600;
                font-size: 12px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                color: #A0AAB8;
            }
            QTabBar::tab:selected {
                color: #FFFFFF;
                background: rgba(255, 255, 255, 0.1);
                border-bottom: 2px solid #3B82F6;
            }
        """)
        
        self.tabs.addTab(self._build_home_tab(), "Home")
        self.tabs.addTab(self._build_insert_tab(), "Insert")
        self.tabs.addTab(self._build_layout_tab(), "Page Layout")
        self.tabs.addTab(self._build_ai_tab(), "AI Assistant")

        layout.addWidget(self.tabs)
        self.set_theme_accent(getattr(self, "_theme_accent", "#00adb5"))

    # ── HOME TAB ─────────────────────────────────────────────────────────────
    def _build_home_tab(self) -> QWidget:
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)

        # 1. Styles Group
        grp_styles = RibbonGroup("STYLES")
        self.combo_styles = QComboBox()
        self.combo_styles.addItems([
            "Normal", "Title", "Subtitle",
            "Heading 1", "Heading 2", "Heading 3",
            "Blockquote"
        ])
        self.combo_styles.setFixedWidth(120)
        self.combo_styles.currentTextChanged.connect(self.heading_style_changed.emit)
        grp_styles.content_layout.addWidget(self.combo_styles)
        layout.addWidget(grp_styles)

        # 2. Font Group
        grp_font = RibbonGroup("FONT")

        col_font = QVBoxLayout()
        col_font.setContentsMargins(0, 0, 0, 0)
        col_font.setSpacing(2)

        row1 = QHBoxLayout()
        row1.setContentsMargins(0, 0, 0, 0)
        row1.setSpacing(4)

        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont("Times New Roman"))
        self.font_combo.setFixedWidth(130)
        self.font_combo.setFixedHeight(22)
        self.font_combo.currentFontChanged.connect(lambda f: self.font_family_changed.emit(f.family()))
        row1.addWidget(self.font_combo)

        self.size_spin = QSpinBox()
        self.size_spin.setRange(6, 144)
        self.size_spin.setValue(12)
        self.size_spin.setFixedWidth(50)
        self.size_spin.setFixedHeight(22)
        self.size_spin.valueChanged.connect(self.font_size_changed.emit)
        row1.addWidget(self.size_spin)
        col_font.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setContentsMargins(0, 0, 0, 0)
        row2.setSpacing(2)

        self.btn_bold = QToolButton()
        self.btn_bold.setText("B")
        self.btn_bold.setCheckable(True)
        self.btn_bold.setFixedSize(22, 22)
        self.btn_bold.setToolTip("Bold (Ctrl+B)")
        self.btn_bold.toggled.connect(self.bold_toggled.emit)
        row2.addWidget(self.btn_bold)

        self.btn_italic = QToolButton()
        self.btn_italic.setText("I")
        self.btn_italic.setCheckable(True)
        self.btn_italic.setFixedSize(22, 22)
        self.btn_italic.setToolTip("Italic (Ctrl+I)")
        self.btn_italic.toggled.connect(self.italic_toggled.emit)
        row2.addWidget(self.btn_italic)

        self.btn_underline = QToolButton()
        self.btn_underline.setText("U")
        self.btn_underline.setCheckable(True)
        self.btn_underline.setFixedSize(22, 22)
        self.btn_underline.setToolTip("Underline (Ctrl+U)")
        self.btn_underline.toggled.connect(self.underline_toggled.emit)
        row2.addWidget(self.btn_underline)

        self.btn_strike = QToolButton()
        self.btn_strike.setText("S")
        self.btn_strike.setCheckable(True)
        self.btn_strike.setFixedSize(22, 22)
        self.btn_strike.setToolTip("Strikethrough")
        self.btn_strike.toggled.connect(self.strikethrough_toggled.emit)
        row2.addWidget(self.btn_strike)

        self.btn_text_color = QToolButton()
        self.btn_text_color.setText("A")
        self.btn_text_color.setToolTip("Text Color")
        self.btn_text_color.setFixedSize(22, 22)
        self.btn_text_color.clicked.connect(self._pick_text_color)
        row2.addWidget(self.btn_text_color)

        self.btn_highlight = QToolButton()
        self.btn_highlight.setText("🖍")
        self.btn_highlight.setToolTip("Highlight Color")
        self.btn_highlight.setFixedSize(22, 22)
        self.btn_highlight.clicked.connect(self._pick_highlight_color)
        row2.addWidget(self.btn_highlight)

        self.btn_clear_fmt = QToolButton()
        self.btn_clear_fmt.setText("🧹")
        self.btn_clear_fmt.setToolTip("Clear Formatting")
        self.btn_clear_fmt.setFixedSize(22, 22)
        self.btn_clear_fmt.clicked.connect(self.clear_formatting_requested.emit)
        row2.addWidget(self.btn_clear_fmt)

        col_font.addLayout(row2)
        grp_font.content_layout.addLayout(col_font)
        layout.addWidget(grp_font)

        # 3. Paragraph Group
        grp_para = RibbonGroup("PARAGRAPH")
        col_para = QVBoxLayout()
        
        p_row1 = QHBoxLayout()
        self.btn_left = QToolButton()
        self.btn_left.setText("Left")
        self.btn_left.setCheckable(True)
        self.btn_left.setToolTip("Align Left (Ctrl+L)")
        self.btn_left.clicked.connect(self.align_left_requested.emit)
        p_row1.addWidget(self.btn_left)

        self.btn_center = QToolButton()
        self.btn_center.setText("Center")
        self.btn_center.setCheckable(True)
        self.btn_center.setToolTip("Align Center (Ctrl+E)")
        self.btn_center.clicked.connect(self.align_center_requested.emit)
        p_row1.addWidget(self.btn_center)

        self.btn_right = QToolButton()
        self.btn_right.setText("Right")
        self.btn_right.setCheckable(True)
        self.btn_right.setToolTip("Align Right (Ctrl+R)")
        self.btn_right.clicked.connect(self.align_right_requested.emit)
        p_row1.addWidget(self.btn_right)

        self.btn_justify = QToolButton()
        self.btn_justify.setText("Justify")
        self.btn_justify.setCheckable(True)
        self.btn_justify.setToolTip("Justify (Ctrl+J)")
        self.btn_justify.clicked.connect(self.align_justify_requested.emit)
        p_row1.addWidget(self.btn_justify)
        col_para.addLayout(p_row1)

        p_row2 = QHBoxLayout()
        self.btn_bullets = QToolButton()
        self.btn_bullets.setText("• List")
        self.btn_bullets.clicked.connect(self.bullet_list_requested.emit)
        p_row2.addWidget(self.btn_bullets)

        self.btn_nums = QToolButton()
        self.btn_nums.setText("1. List")
        self.btn_nums.clicked.connect(self.numbered_list_requested.emit)
        p_row2.addWidget(self.btn_nums)

        self.btn_indent = QToolButton()
        self.btn_indent.setText("Indent ->")
        self.btn_indent.clicked.connect(self.indent_requested.emit)
        p_row2.addWidget(self.btn_indent)

        self.btn_outdent = QToolButton()
        self.btn_outdent.setText("<- Outdent")
        self.btn_outdent.clicked.connect(self.outdent_requested.emit)
        p_row2.addWidget(self.btn_outdent)

        self.combo_spacing = QComboBox()
        self.combo_spacing.addItems(["1.0", "1.15", "1.5", "2.0 (Double)"])
        self.combo_spacing.setFixedWidth(90)
        self.combo_spacing.currentIndexChanged.connect(self._on_spacing_changed)
        p_row2.addWidget(self.combo_spacing)

        col_para.addLayout(p_row2)
        grp_para.content_layout.addLayout(col_para)
        layout.addWidget(grp_para)

        # 4. Actions & Search Group
        grp_actions = RibbonGroup("SEARCH & EXPORT")
        col_actions = QVBoxLayout()
        
        self.btn_find = QToolButton()
        self.btn_find.setText("🔍 Find & Replace (Ctrl+F)")
        self.btn_find.clicked.connect(self.find_requested.emit)
        col_actions.addWidget(self.btn_find)

        self.btn_export = QToolButton()
        self.btn_export.setText("💾 Export As… (PDF, MD, HTML)")
        self.btn_export.clicked.connect(self.export_dialog_requested.emit)
        col_actions.addWidget(self.btn_export)

        grp_actions.content_layout.addLayout(col_actions)
        layout.addWidget(grp_actions)

        layout.addStretch()
        return tab

    # ── INSERT TAB ────────────────────────────────────────────────────────────
    def _build_insert_tab(self) -> QWidget:
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)

        grp_tables = RibbonGroup("TABLE & MEDIA")
        
        btn_tbl = QToolButton()
        btn_tbl.setText("📊 Insert Table")
        btn_tbl.clicked.connect(self._on_insert_table)
        grp_tables.content_layout.addWidget(btn_tbl)

        btn_img = QToolButton()
        btn_img.setText("🖼 Insert Image")
        btn_img.clicked.connect(self._on_insert_image)
        grp_tables.content_layout.addWidget(btn_img)

        btn_divider = QToolButton()
        btn_divider.setText("➖ Line Divider")
        btn_divider.clicked.connect(self.insert_divider_requested.emit)
        grp_tables.content_layout.addWidget(btn_divider)

        btn_pagebreak = QToolButton()
        btn_pagebreak.setText("📄 Page Break")
        btn_pagebreak.clicked.connect(self.insert_page_break_requested.emit)
        grp_tables.content_layout.addWidget(btn_pagebreak)

        layout.addWidget(grp_tables)
        layout.addStretch()
        return tab

    # ── LAYOUT TAB ────────────────────────────────────────────────────────────
    def _build_layout_tab(self) -> QWidget:
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)

        grp_presets = RibbonGroup("DOCUMENT PRESETS")
        self.combo_preset = QComboBox()
        self.combo_preset.addItems([
            "Custom Layout",
            "APA 7th Edition (Academic)",
            "MLA 9th Edition",
            "IEEE Academic Paper",
            "Corporate Business Report"
        ])
        self.combo_preset.setFixedWidth(190)
        self.combo_preset.currentTextChanged.connect(self.preset_changed.emit)
        grp_presets.content_layout.addWidget(self.combo_preset)
        layout.addWidget(grp_presets)

        grp_page = RibbonGroup("MARGINS & SIZE")
        self.combo_margins = QComboBox()
        self.combo_margins.addItems(["Normal (1.0 in)", "Narrow (0.5 in)", "Moderate", "Wide"])
        self.combo_margins.setFixedWidth(130)
        self.combo_margins.currentTextChanged.connect(self.margin_preset_changed.emit)
        grp_page.content_layout.addWidget(self.combo_margins)

        self.combo_size = QComboBox()
        self.combo_size.addItems(["Letter (8.5 x 11 in)", "A4 (210 x 297 mm)", "Legal (8.5 x 14 in)", "Executive"])
        self.combo_size.setFixedWidth(140)
        self.combo_size.currentTextChanged.connect(self.page_size_changed.emit)
        grp_page.content_layout.addWidget(self.combo_size)
        layout.addWidget(grp_page)

        grp_cursor = RibbonGroup("CURSOR & CARETS")
        col_cursor = QVBoxLayout()
        col_cursor.setContentsMargins(0, 0, 0, 0)
        col_cursor.setSpacing(2)

        row_caret = QHBoxLayout()
        row_caret.setContentsMargins(0, 0, 0, 0)
        row_caret.setSpacing(4)
        lbl_c = QLabel("Caret:")
        lbl_c.setFixedWidth(40)
        lbl_c.setFixedHeight(22)
        lbl_c.setStyleSheet("font-size: 11px; font-weight: 500;")
        row_caret.addWidget(lbl_c)
        self.combo_caret_style = QComboBox()
        self.combo_caret_style.addItems([
            "I-Beam Line",
            "Thick Bar",
            "Full Block Caret",
            "Underline Caret"
        ])
        self.combo_caret_style.setFixedWidth(115)
        self.combo_caret_style.setFixedHeight(22)
        self.combo_caret_style.currentTextChanged.connect(self.caret_style_changed.emit)
        row_caret.addWidget(self.combo_caret_style)
        col_cursor.addLayout(row_caret)

        row_ptr = QHBoxLayout()
        row_ptr.setContentsMargins(0, 0, 0, 0)
        row_ptr.setSpacing(4)
        lbl_p = QLabel("Mouse:")
        lbl_p.setFixedWidth(40)
        lbl_p.setFixedHeight(22)
        lbl_p.setStyleSheet("font-size: 11px; font-weight: 500;")
        row_ptr.addWidget(lbl_p)
        self.combo_pointer_style = QComboBox()
        self.combo_pointer_style.addItems([
            "Standard I-Beam",
            "Crosshair Pointer",
            "Pointing Hand",
            "Arrow Pointer"
        ])
        self.combo_pointer_style.setFixedWidth(115)
        self.combo_pointer_style.setFixedHeight(22)
        self.combo_pointer_style.currentTextChanged.connect(self.pointer_style_changed.emit)
        row_ptr.addWidget(self.combo_pointer_style)
        col_cursor.addLayout(row_ptr)

        grp_cursor.content_layout.addLayout(col_cursor)

        self.btn_help = QToolButton()
        self.btn_help.setText("❓ Help & Shortcuts")
        self.btn_help.setToolTip("View System Documentation & Keyboard Shortcuts")
        self.btn_help.clicked.connect(self.help_requested.emit)
        grp_cursor.content_layout.addWidget(self.btn_help)
        layout.addWidget(grp_cursor)

        # Zoom Control Group
        grp_zoom = RibbonGroup("CANVAS ZOOM")
        col_zoom = QVBoxLayout()
        z_row = QHBoxLayout()

        self.btn_zoom_out = QToolButton()
        self.btn_zoom_out.setText("➖")
        self.btn_zoom_out.setToolTip("Zoom Out (Ctrl + Scroll Down)")
        self.btn_zoom_out.clicked.connect(self.zoom_out_requested.emit)
        z_row.addWidget(self.btn_zoom_out)

        self.lbl_zoom_val = QLabel("100%")
        self.lbl_zoom_val.setObjectName("zoomValLabel")
        self.lbl_zoom_val.setStyleSheet("font-weight: bold; font-size: 11px;")
        self.lbl_zoom_val.setAlignment(Qt.AlignmentFlag.AlignCenter)
        z_row.addWidget(self.lbl_zoom_val)

        self.btn_zoom_in = QToolButton()
        self.btn_zoom_in.setText("➕")
        self.btn_zoom_in.setToolTip("Zoom In (Ctrl + Scroll Up)")
        self.btn_zoom_in.clicked.connect(self.zoom_in_requested.emit)
        z_row.addWidget(self.btn_zoom_in)
        col_zoom.addLayout(z_row)

        self.btn_zoom_reset = QToolButton()
        self.btn_zoom_reset.setText("↺ Reset 100%")
        self.btn_zoom_reset.clicked.connect(self.zoom_reset_requested.emit)
        col_zoom.addWidget(self.btn_zoom_reset)

        grp_zoom.content_layout.addLayout(col_zoom)
        layout.addWidget(grp_zoom)

        layout.addStretch()
        return tab

    # ── AI TAB ────────────────────────────────────────────────────────────────
    def _build_ai_tab(self) -> QWidget:
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)

        grp_ai = RibbonGroup("AI COPILOT")
        
        btn_sum = QToolButton()
        btn_sum.setText("📝 Summarize")
        btn_sum.clicked.connect(self.ai_summarize_requested.emit)
        grp_ai.content_layout.addWidget(btn_sum)

        btn_rephrase = QToolButton()
        btn_rephrase.setText("✨ Rephrase / Tone")
        btn_rephrase.clicked.connect(self.ai_rephrase_requested.emit)
        grp_ai.content_layout.addWidget(btn_rephrase)

        btn_grammar = QToolButton()
        btn_grammar.setText("🔍 Grammar Check")
        btn_grammar.clicked.connect(self.ai_grammar_requested.emit)
        grp_ai.content_layout.addWidget(btn_grammar)

        layout.addWidget(grp_ai)

        grp_drawers = RibbonGroup("PANELS & TOOLS")
        btn_outline = QToolButton()
        btn_outline.setText("🌳 Outline Navigation")
        btn_outline.clicked.connect(lambda: self.toggle_side_panel_requested.emit("outline"))
        grp_drawers.content_layout.addWidget(btn_outline)

        btn_analytics = QToolButton()
        btn_analytics.setText("📊 Live Analytics")
        btn_analytics.clicked.connect(lambda: self.toggle_side_panel_requested.emit("analytics"))
        grp_drawers.content_layout.addWidget(btn_analytics)

        btn_comments = QToolButton()
        btn_comments.setText("💬 Comments & Changes")
        btn_comments.clicked.connect(lambda: self.toggle_side_panel_requested.emit("comments"))
        grp_drawers.content_layout.addWidget(btn_comments)

        layout.addWidget(grp_drawers)

        layout.addStretch()
        return tab

    # ── EVENT HANDLERS ────────────────────────────────────────────────────────
    def _pick_text_color(self):
        color = QColorDialog.getColor(Qt.GlobalColor.black, self, "Select Text Color")
        if color.isValid():
            self.text_color_changed.emit(color)

    def _pick_highlight_color(self):
        color = QColorDialog.getColor(Qt.GlobalColor.yellow, self, "Select Highlight Color")
        if color.isValid():
            self.highlight_color_changed.emit(color)

    def _on_spacing_changed(self, idx: int):
        spacings = [1.0, 1.15, 1.5, 2.0]
        if idx < len(spacings):
            self.line_spacing_changed.emit(spacings[idx])

    def _on_insert_table(self):
        dlg = InsertTableDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            r, c = dlg.get_dimensions()
            self.insert_table_requested.emit(r, c)

    def _on_insert_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_path:
            self.insert_image_requested.emit(file_path)

    def update_formatting_state(self, fmt: QTextCharFormat, block_fmt: QTextBlockFormat):
        """Syncs ribbon controls with the active editor selection/cursor."""
        self.btn_bold.blockSignals(True)
        self.btn_italic.blockSignals(True)
        self.btn_underline.blockSignals(True)
        self.btn_strike.blockSignals(True)
        self.font_combo.blockSignals(True)
        self.size_spin.blockSignals(True)

        self.btn_bold.setChecked(fmt.font().bold() or fmt.fontWeight() >= 700)
        self.btn_italic.setChecked(fmt.fontItalic())
        self.btn_underline.setChecked(fmt.fontUnderline())
        self.btn_strike.setChecked(fmt.fontStrikeOut())
        
        if hasattr(self, "btn_left") and block_fmt is not None:
            self.btn_left.blockSignals(True)
            self.btn_center.blockSignals(True)
            self.btn_right.blockSignals(True)
            self.btn_justify.blockSignals(True)
            align = block_fmt.alignment()
            is_right = bool(align & Qt.AlignmentFlag.AlignRight)
            is_center = bool(align & Qt.AlignmentFlag.AlignHCenter)
            is_justify = bool(align & Qt.AlignmentFlag.AlignJustify)
            is_left = not (is_right or is_center or is_justify)
            self.btn_left.setChecked(is_left)
            self.btn_center.setChecked(is_center)
            self.btn_right.setChecked(is_right)
            self.btn_justify.setChecked(is_justify)
            self.btn_left.blockSignals(False)
            self.btn_center.blockSignals(False)
            self.btn_right.blockSignals(False)
            self.btn_justify.blockSignals(False)

        font_family = fmt.font().family()
        if font_family:
            self.font_combo.setCurrentFont(QFont(font_family))
        pt_size = fmt.fontPointSize()
        if pt_size <= 0:
            pt_size = fmt.font().pointSizeF()
        if pt_size <= 0:
            pt_size = fmt.font().pointSize()
        if pt_size > 0:
            self.size_spin.setValue(int(pt_size))

        self.btn_bold.blockSignals(False)
        self.btn_italic.blockSignals(False)
        self.btn_underline.blockSignals(False)
        self.btn_strike.blockSignals(False)
        self.font_combo.blockSignals(False)
        self.size_spin.blockSignals(False)

    def _create_toggle_style(self, accent_hex: str, extra_css: str = "") -> str:
        accent_q = QColor(accent_hex) if accent_hex else QColor("#00adb5")
        lum = accent_q.red() * 0.299 + accent_q.green() * 0.587 + accent_q.blue() * 0.114
        checked_text = "#05080c" if lum > 165 else "#ffffff"
        checked_border = "rgba(0, 0, 0, 0.4)" if lum > 165 else "rgba(255, 255, 255, 0.85)"
        
        return f"""
            QToolButton {{
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 4px;
                color: #e2e8f0;
                font-size: 11px;
                padding: 1px 3px;
                {extra_css}
            }}
            QToolButton:hover {{
                background: rgba(255, 255, 255, 0.14);
                border: 1px solid {accent_hex};
                color: {accent_hex};
            }}
            QToolButton:checked {{
                background: {accent_hex};
                border: 1.5px solid {checked_border};
                color: {checked_text};
                font-weight: 900;
            }}
            QToolButton:checked:hover {{
                background: {accent_hex};
                border: 1.5px solid #ffffff;
                color: {checked_text};
            }}
        """

    def set_theme_accent(self, accent_hex: str) -> None:
        """Dynamically aligns ribbon indicators and checkable toggle buttons with the theme accent."""
        self._theme_accent = accent_hex
        if hasattr(self, "lbl_zoom_val"):
            self.lbl_zoom_val.setStyleSheet(f"color: {accent_hex}; font-weight: bold; font-size: 11px;")

        if hasattr(self, "btn_bold"):
            self.btn_bold.setStyleSheet(self._create_toggle_style(accent_hex, "font-weight: bold;"))
        if hasattr(self, "btn_italic"):
            self.btn_italic.setStyleSheet(self._create_toggle_style(accent_hex, "font-style: italic; font-weight: 600;"))
        if hasattr(self, "btn_underline"):
            self.btn_underline.setStyleSheet(self._create_toggle_style(accent_hex, "text-decoration: underline; font-weight: 600;"))
        if hasattr(self, "btn_strike"):
            self.btn_strike.setStyleSheet(self._create_toggle_style(accent_hex, "text-decoration: line-through; font-weight: 600;"))

        if hasattr(self, "btn_left"):
            self.btn_left.setStyleSheet(self._create_toggle_style(accent_hex, "font-weight: 600;"))
        if hasattr(self, "btn_center"):
            self.btn_center.setStyleSheet(self._create_toggle_style(accent_hex, "font-weight: 600;"))
        if hasattr(self, "btn_right"):
            self.btn_right.setStyleSheet(self._create_toggle_style(accent_hex, "font-weight: 600;"))
        if hasattr(self, "btn_justify"):
            self.btn_justify.setStyleSheet(self._create_toggle_style(accent_hex, "font-weight: 600;"))
