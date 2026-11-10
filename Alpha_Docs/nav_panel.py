"""
nav_panel.py — Alpha Tech Left Navigation Panel
Emits page_requested(str) for page routing and doc_type_changed(str) when the
document-type dropdown changes.
"""
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLabel
from PySide6.QtCore import Signal, Qt

# (icon, display label, page key)
NAV_ITEMS: list[tuple[str, str, str]] = [
    ("🏠", "Home",        "home"),
    ("📄", "New Document",  "new_document"),
    ("➕", "Add Document","add_document"),
    ("💻", "Code Editor", "code_editor"),
    ("⚙️", "Settings",    "settings"),
    ("🕐", "History",     "history"),
    ("❓", "Help",        "help"),
    ("ℹ️", "About",       "about"),
]

DOC_TYPES = [
    "Brochure - Bi-Fold Spread",
    "Brochure - Modern Tech Tri-Fold",
    "Brochure - Editorial Studio",
    "Brochure - Emerald Enterprise",
    "Essay - APA Format",
    "Resume - Strategic Marketing",
    "Resume - Executive Corporate",
    "Resume - Creative Editorial",
    "Resume - Modern Sage",
    "Cover Letter",
    "Marketing Copy",
    "Technical Document",
    "Report - Business",
]


class NavPanel(QFrame):
    """Fixed-width left panel: dropdown + page navigation buttons."""

    page_requested  = Signal(str)   # page key
    doc_type_changed = Signal(str)  # dropdown text
    new_document_requested = Signal()
    collapse_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("leftPanel")
        self.setFixedWidth(190)
        self._active_key: str = ""
        self._buttons: dict[str, QPushButton] = {}

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 14, 12, 14)
        layout.setSpacing(8)

        # Header with Section label + Collapse Button
        top_header = QHBoxLayout()
        top_header.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel("NAVIGATION")
        lbl.setObjectName("sectionTitle")
        top_header.addWidget(lbl)
        top_header.addStretch()

        self.btn_collapse = QPushButton("◀")
        self.btn_collapse.setObjectName("collapseNavButton")
        self.btn_collapse.setFixedSize(24, 24)
        self.btn_collapse.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_collapse.setToolTip("Collapse Navigation Sidebar")
        self.btn_collapse.setStyleSheet("""
            QPushButton#collapseNavButton {
                padding: 0px;
                font-size: 11px;
                font-weight: bold;
                border-radius: 4px;
            }
        """)
        self.btn_collapse.clicked.connect(self.collapse_requested.emit)
        top_header.addWidget(self.btn_collapse)

        layout.addLayout(top_header)

        # Document-type dropdown
        self.dropdown = QComboBox()
        self.dropdown.setObjectName("dropdownMenu")
        self.dropdown.setFixedWidth(166)
        self.dropdown.addItems(DOC_TYPES)
        self.dropdown.currentTextChanged.connect(self.doc_type_changed)
        layout.addWidget(self.dropdown)
        layout.addSpacing(10)

        # Navigation buttons
        for icon, label, key in NAV_ITEMS:
            btn = QPushButton(f"{icon}  {label}")
            btn.setObjectName("navButton")
            btn.setFixedWidth(166)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _checked=False, k=key: self._on_click(k))
            self._buttons[key] = btn
            layout.addWidget(btn)

        layout.addStretch()

        # Branded title placed under nav widget
        logo_lbl = QLabel("Alpha Tech Document Suite")
        logo_lbl.setObjectName("headerLabel")
        logo_lbl.setWordWrap(True)
        logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_lbl)
        
        self.setLayout(layout)

    # ── Public API ────────────────────────────────────────────────────────────

    def set_active(self, key: str) -> None:
        """Highlight the active button; un-highlight the previous one."""
        if self._active_key and self._active_key in self._buttons:
            self._set_btn_style(self._buttons[self._active_key], active=False)
        self._active_key = key
        if key in self._buttons:
            self._set_btn_style(self._buttons[key], active=True)

    def current_doc_type(self) -> str:
        return self.dropdown.currentText()

    def set_doc_type(self, text: str) -> None:
        idx = self.dropdown.findText(text)
        if idx >= 0:
            self.dropdown.setCurrentIndex(idx)

    # ── Internals ─────────────────────────────────────────────────────────────

    def _on_click(self, key: str) -> None:
        if key == "new_document":
            self.new_document_requested.emit()
            return
        self.set_active(key)
        self.page_requested.emit(key)

    @staticmethod
    def _set_btn_style(btn: QPushButton, active: bool) -> None:
        btn.setObjectName("navButtonActive" if active else "navButton")
        # Force Qt style engine to re-read the new objectName
        btn.style().unpolish(btn)
        btn.style().polish(btn)
        btn.update()