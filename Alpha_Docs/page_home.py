"""
page_home.py — Alpha Tech Home / Dashboard Page
Artifact Pipeline Map (6 tiles) + Output Registry (6 document areas).
"""
import os
import json
import time
from PySide6.QtWidgets import (
    QScrollArea, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QGridLayout,
)
from PySide6.QtCore import Qt, Signal

from widgets import ArtifactButton, DocumentSaveArea

_DEFAULT_DRAFTS = [
    ("AI Strategy Proposal", "Executive proposal outlining automated workflow deployments and governance."),
    ("Quarterly Executive Brief", "Synthesis of cross-functional operational metrics, milestones, and roadmaps."),
    ("Academic Literature Review", "Methodological analysis of autonomous cognitive architectures."),
    ("Technical Architecture Spec", "System design specification for enterprise document streaming engines."),
    ("Product Launch Memo", "Go-to-market timeline, positioning points, and channel distributions."),
    ("Meeting Synthesis Notes", "Actionable synthesis of cross-departmental alignment discussions.")
]

_DOC_TYPES = [
    "Brochure", "Essay", "Resume",
    "Cover Letter", "Marketing", "Report",
]


class HomePage(QScrollArea):
    """Main dashboard: Quick Access to Recent & Unfinished Documents + Output Registry."""

    artifact_selected        = Signal(str)        # artifact / draft name
    document_selected        = Signal(str)        # doc-type name
    recent_document_selected = Signal(str, str)   # title, content

    def __init__(self, accent: str = "#00adb5", text_color: str = "#f0f4f8", subtext_color: str = "#9aa5b5", parent=None):
        super().__init__(parent)
        self.setObjectName("pageContainer")
        self.setWidgetResizable(True)
        self.setFrameShape(QScrollArea.Shape.NoFrame)

        self._theme_accent = accent
        self._text_color = text_color
        self._subtext_color = subtext_color

        self.history_dir = os.path.join(os.path.dirname(__file__), "history_data")
        os.makedirs(self.history_dir, exist_ok=True)

        self.artifact_buttons: list[ArtifactButton] = []
        self.document_areas: list[DocumentSaveArea]  = []

        container = QWidget()
        container.setObjectName("pageContainer")
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(20)

        # ── Quick Access: Recent & Unfinished Documents ───────────────────────
        layout.addWidget(self._section_title("QUICK ACCESS — RECENT & UNFINISHED DRAFTS"))
        layout.addLayout(self._build_artifact_grid())
        layout.addSpacing(8)

        # ── Output Registry ───────────────────────────────────────────────────
        layout.addWidget(self._section_title("OUTPUT REGISTRY"))
        layout.addLayout(self._build_doc_grid())

        layout.addStretch()
        container.setLayout(layout)
        self.setWidget(container)

    # ── Grid builders ─────────────────────────────────────────────────────────

    def _build_artifact_grid(self) -> QGridLayout:
        grid = QGridLayout()
        grid.setSpacing(12)

        drafts = self._fetch_recent_drafts()
        self.artifact_buttons.clear()

        acc = getattr(self, "_theme_accent", "#00adb5")
        txt = getattr(self, "_text_color", "#f0f4f8")
        sub = getattr(self, "_subtext_color", "#9aa5b5")

        for idx, (title, content, timestamp_str, word_count, is_autosave) in enumerate(drafts):
            btn = ArtifactButton(title)
            btn.set_theme_accent(acc, txt, sub)
            btn.set_draft_info(title, timestamp_str, word_count, is_autosave, content)
            btn.clicked.connect(lambda _=False, b=btn: self._on_draft_card_clicked(b))
            self.artifact_buttons.append(btn)

            row, col = divmod(idx, 3)
            wrapper = QVBoxLayout()
            wrapper.setContentsMargins(0, 10 if row == 1 else 0, 0, 0)
            wrapper.addWidget(btn)
            wrapper.addStretch()
            grid.addLayout(wrapper, row, col)

        return grid

    def _fetch_recent_drafts(self) -> list:
        drafts = []
        if os.path.exists(self.history_dir):
            files = sorted(os.listdir(self.history_dir), reverse=True)
            for f in files:
                if f.endswith(".json") and len(drafts) < 6:
                    filepath = os.path.join(self.history_dir, f)
                    try:
                        with open(filepath, "r", encoding="utf-8") as file:
                            data = json.load(file)
                            title = data.get("title", "Untitled Draft")
                            content = data.get("content", "")
                            is_auto = data.get("is_autosave", False)
                            ts = data.get("timestamp", time.time())
                            t_str = time.strftime("%b %d, %I:%M %p", time.localtime(ts))
                            words = len(content.split()) if content else 0
                            drafts.append((title, content, t_str, words, is_auto))
                    except Exception:
                        pass

        # Pad with starter templates if fewer than 6 saved drafts
        pad_idx = 0
        while len(drafts) < 6:
            default_title, default_content = _DEFAULT_DRAFTS[pad_idx % len(_DEFAULT_DRAFTS)]
            pad_idx += 1
            words = len(default_content.split())
            drafts.append((default_title, f"# {default_title}\n\n{default_content}\n", "Ready to edit", words, False))

        return drafts

    def refresh_recent_documents(self) -> None:
        """Refreshes the Quick Access cards with the latest saved drafts and autosaves."""
        drafts = self._fetch_recent_drafts()
        acc = getattr(self, "_theme_accent", "#00adb5")
        txt = getattr(self, "_text_color", "#f0f4f8")
        sub = getattr(self, "_subtext_color", "#9aa5b5")
        for idx, (title, content, timestamp_str, word_count, is_autosave) in enumerate(drafts):
            if idx < len(self.artifact_buttons):
                self.artifact_buttons[idx].set_theme_accent(acc, txt, sub)
                self.artifact_buttons[idx].set_draft_info(title, timestamp_str, word_count, is_autosave, content)

    def _on_draft_card_clicked(self, btn: ArtifactButton) -> None:
        self.recent_document_selected.emit(btn.artifact_name, getattr(btn, "document_content", ""))
        self.artifact_selected.emit(btn.artifact_name)

    def _build_doc_grid(self) -> QGridLayout:
        grid = QGridLayout()
        grid.setSpacing(14)

        acc = getattr(self, "_theme_accent", "#00adb5")
        txt = getattr(self, "_text_color", "#f0f4f8")
        sub = getattr(self, "_subtext_color", "#9aa5b5")

        for idx, doc_type in enumerate(_DOC_TYPES):
            area = DocumentSaveArea(doc_type)
            area.set_theme_accent(acc, txt, sub)
            if doc_type == "Resume":
                cover_path = os.path.join(os.path.dirname(__file__), "assets", "resume_section_cover.jpg")
                if os.path.exists(cover_path):
                    from PySide6.QtGui import QPixmap
                    pix = QPixmap(cover_path)
                    if not pix.isNull():
                        area.set_document(pix, "4 Templates • Click to Pick")
            elif doc_type == "Brochure":
                cover_path = os.path.join(os.path.dirname(__file__), "assets", "brochure_section_cover.jpg")
                if os.path.exists(cover_path):
                    from PySide6.QtGui import QPixmap
                    pix = QPixmap(cover_path)
                    if not pix.isNull():
                        area.set_document(pix, "4 Templates • Click to Pick")
            area.mousePressEvent = lambda _e, d=doc_type: self.document_selected.emit(d)
            self.document_areas.append(area)
            row, col = divmod(idx, 3)
            grid.addWidget(area, row, col)

        return grid

    # ── Public helpers ────────────────────────────────────────────────────────

    def set_theme_accent(self, accent_hex: str, text_color: str = None, subtext_color: str = None) -> None:
        """Propagates theme accent dynamically across draft cards and output registry areas."""
        self._theme_accent = accent_hex
        if text_color:
            self._text_color = text_color
        if subtext_color:
            self._subtext_color = subtext_color
        for btn in self.artifact_buttons:
            if hasattr(btn, "set_theme_accent"):
                btn.set_theme_accent(accent_hex, self._text_color, self._subtext_color)
        for area in self.document_areas:
            if hasattr(area, "set_theme_accent"):
                area.set_theme_accent(accent_hex, self._text_color, self._subtext_color)

    def set_artifact_thumbnail(self, index: int, pixmap) -> None:
        if 0 <= index < len(self.artifact_buttons):
            self.artifact_buttons[index].set_thumbnail(pixmap)

    def set_document_preview(self, index: int, pixmap, status: str = "") -> None:
        if 0 <= index < len(self.document_areas):
            self.document_areas[index].set_document(pixmap, status)

    def clear_document(self, index: int) -> None:
        if 0 <= index < len(self.document_areas):
            self.document_areas[index].clear_document()

    def mark_document_status(self, index: int, text: str) -> None:
        if 0 <= index < len(self.document_areas):
            self.document_areas[index].set_status(text)

    # ── Internal ──────────────────────────────────────────────────────────────

    @staticmethod
    def _section_title(text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("sectionTitle")
        return lbl