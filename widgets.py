"""
widgets.py — Alpha Tech Reusable Widgets
All custom QWidget subclasses. Styled entirely via object names in themes.py;
no inline colour strings here so themes apply cleanly.
"""
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QWidget,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QColor


# ─── PlaceholderImageBox ──────────────────────────────────────────────────────

class PlaceholderImageBox(QFrame):
    """Small image placeholder with a caption below it."""

    def __init__(self, label_text: str, width: int = 150, height: int = 180):
        super().__init__()
        self.setObjectName("placeholderBox")
        self.setFixedSize(width, height)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.image_label = QLabel("[Image]")
        self.image_label.setObjectName("imageLabel")
        self.image_label.setFixedSize(width - 4, height - 30)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        caption = QLabel(label_text)
        caption.setObjectName("imageCaption")
        caption.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.image_label)
        layout.addWidget(caption)
        self.setLayout(layout)

    def set_image(self, pixmap: QPixmap) -> None:
        scaled = pixmap.scaled(
            self.image_label.width() - 4,
            self.image_label.height() - 4,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.image_label.setPixmap(scaled)

    def clear_image(self) -> None:
        self.image_label.clear()
        self.image_label.setText("[Image]")


# ─── ArtifactButton ───────────────────────────────────────────────────────────

class ArtifactButton(QPushButton):
    """Clickable tile with a thumbnail preview and name label with 3D elevation hover effect."""

    def __init__(self, artifact_name: str, parent=None):
        super().__init__(parent)
        self.artifact_name = artifact_name
        self._theme_accent = "#00adb5"
        self._text_color = "#f0f4f8"
        self._subtext_color = "#9aa5b5"
        self._draft_info = None
        self.setObjectName("artifactButton")
        self.setFixedSize(145, 160)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # 3D Depth Shadow Effect
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(12)
        self._shadow.setYOffset(3)
        self._shadow.setColor(QColor(0, 0, 0, 110))
        self.setGraphicsEffect(self._shadow)

        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        icon_map = {
            "Article": "📰",
            "Guide": "📘",
            "Blog": "✍️",
            "Template": "📐",
            "Draft": "📝",
            "Final": "🏆",
        }
        icon = icon_map.get(artifact_name, "📄")

        self.thumbnail = QLabel(f"{icon}\n[Artifact]")
        self.thumbnail.setObjectName("artifactThumbnail")
        self.thumbnail.setFixedSize(127, 95)
        self.thumbnail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail.setStyleSheet("""
            QLabel#artifactThumbnail {
                background: rgba(0, 0, 0, 0.20);
                border: 1px dashed rgba(255, 255, 255, 0.15);
                border-radius: 8px;
                font-size: 14px;
                color: #8e96a3;
            }
        """)

        name_label = QLabel(artifact_name)
        name_label.setObjectName("artifactName")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("font-size: 12px; font-weight: 700; color: #f0f4f8;")
        self.name_label = name_label
        self.document_content = ""

        layout.addWidget(self.thumbnail)
        layout.addWidget(name_label)
        self.setLayout(layout)

        self._apply_style()

    def _apply_style(self):
        acc = getattr(self, "_theme_accent", "#00adb5")
        txt = getattr(self, "_text_color", "#f0f4f8")
        self.setStyleSheet(f"""
            QPushButton#artifactButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 0.05), stop:1 rgba(255, 255, 255, 0.02));
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-top: 2.5px solid {acc};
                border-radius: 12px;
                padding: 4px;
                margin-top: 5px;
                margin-bottom: 0px;
            }}
            QPushButton#artifactButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 0.11), stop:1 rgba(255, 255, 255, 0.04));
                border: 1.5px solid {acc};
                border-top: 3px solid {acc};
                margin-top: 0px;
                margin-bottom: 5px;
            }}
        """)
        if hasattr(self, "name_label"):
            self.name_label.setStyleSheet(f"font-size: 12px; font-weight: 700; color: {txt};")

    def enterEvent(self, event):
        if hasattr(self, "_shadow"):
            self._shadow.setBlurRadius(24)
            self._shadow.setYOffset(8)
            try:
                c = QColor(self._theme_accent)
                self._shadow.setColor(QColor(c.red(), c.green(), c.blue(), 110))
            except Exception:
                self._shadow.setColor(QColor(0, 0, 0, 180))
        super().enterEvent(event)

    def leaveEvent(self, event):
        if hasattr(self, "_shadow"):
            self._shadow.setBlurRadius(12)
            self._shadow.setYOffset(3)
            self._shadow.setColor(QColor(0, 0, 0, 110))
        super().leaveEvent(event)

    def set_theme_accent(self, accent_hex: str, text_color: str = None, subtext_color: str = None):
        """Dynamically updates artifact button accent glow, shadow, and raises card."""
        self._theme_accent = accent_hex
        if text_color:
            self._text_color = text_color
        if subtext_color:
            self._subtext_color = subtext_color
        self._apply_style()
        if self._draft_info:
            self.set_draft_info(*self._draft_info)

    def set_draft_info(self, title: str, timestamp_str: str, word_count: int, is_autosave: bool = False, content: str = "") -> None:
        self.artifact_name = title
        self.document_content = content
        self._draft_info = (title, timestamp_str, word_count, is_autosave, content)
        icon = "⚡" if is_autosave else "📝"
        badge = "AUTOSAVE" if is_autosave else "DRAFT"
        acc = getattr(self, "_theme_accent", "#00adb5")
        sub = getattr(self, "_subtext_color", "#9aa5b5")
        txt = getattr(self, "_text_color", "#f0f4f8")
        self.thumbnail.setText(f"{icon} <b style='color:{acc};'>[{badge}]</b><br><span style='color:{sub}; font-size:10px;'>{word_count} words<br>{timestamp_str}</span>")
        self.thumbnail.setStyleSheet(f"""
            QLabel#artifactThumbnail {{
                background: rgba(0, 0, 0, 0.25);
                border: 1.5px dashed {acc};
                border-radius: 8px;
                padding: 4px;
            }}
        """)
        self.name_label.setText(title)
        self.name_label.setStyleSheet(f"font-size: 12px; font-weight: 700; color: {txt};")

    def set_thumbnail(self, pixmap: QPixmap) -> None:
        scaled = pixmap.scaled(
            124, 90,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.thumbnail.setPixmap(scaled)


# ─── DocumentSaveArea ─────────────────────────────────────────────────────────

class DocumentSaveArea(QFrame):
    """Card showing a preview of a saved output document with 3D elevation and hover raise."""

    DOC_ICONS = {
        "Brochure": "🏖️",
        "Essay": "🎓",
        "Resume": "👔",
        "Cover Letter": "✉️",
        "Marketing": "🚀",
        "Report": "📊",
    }

    def __init__(self, doc_type: str, width: int = 230, height: int = 280):
        super().__init__()
        self.doc_type = doc_type
        self._theme_accent = "#00adb5"
        self._text_color = "#f0f4f8"
        self._subtext_color = "#9aa5b5"
        self.setObjectName("documentArea")
        self.setFixedSize(width, height + 6)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # 3D Depth Shadow Effect
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(14)
        self._shadow.setYOffset(4)
        self._shadow.setColor(QColor(0, 0, 0, 130))
        self.setGraphicsEffect(self._shadow)

        layout = QVBoxLayout()
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        icon = self.DOC_ICONS.get(doc_type, "📄")
        self.header = QLabel(f"{icon}  {doc_type.upper()}")
        self.header.setObjectName("docAreaHeader")
        self.header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.doc_display = QLabel(f"📄  {doc_type}\n\nClick to Open Template")
        self.doc_display.setObjectName("docDisplay")
        self.doc_display.setFixedSize(width - 28, height - 85)
        self.doc_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doc_display.setStyleSheet("""
            QLabel#docDisplay {
                background: rgba(0, 0, 0, 0.22);
                border: 1px dashed rgba(255, 255, 255, 0.18);
                border-radius: 8px;
                color: #8e96a3;
                font-size: 11px;
                font-weight: 600;
            }
        """)

        self.status = QLabel()
        self.status.setObjectName("docStatus")
        self.status.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self._update_status_text("Ready to Draft")

        layout.addWidget(self.header)
        layout.addWidget(self.doc_display)
        layout.addWidget(self.status)
        self.setLayout(layout)

        self._apply_style()

    def _update_status_text(self, text: str = "Ready to Draft"):
        acc = getattr(self, "_theme_accent", "#00adb5")
        sub = getattr(self, "_subtext_color", "#9aa5b5")
        self.status.setText(f"<span style='color:{acc}; font-weight:bold;'>●</span> <span style='color:{sub}; font-size:11px; font-weight:600;'>{text}</span>")

    def _apply_style(self):
        acc = getattr(self, "_theme_accent", "#00adb5")
        txt = getattr(self, "_text_color", "#f0f4f8")
        sub = getattr(self, "_subtext_color", "#9aa5b5")
        self.setStyleSheet(f"""
            QFrame#documentArea {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 0.05), stop:1 rgba(255, 255, 255, 0.02));
                border: 1px solid rgba(255, 255, 255, 0.14);
                border-top: 3px solid {acc};
                border-radius: 12px;
                margin-top: 6px;
                margin-bottom: 0px;
            }}
            QFrame#documentArea:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 0.11), stop:1 rgba(255, 255, 255, 0.04));
                border: 1.5px solid {acc};
                border-top: 3.5px solid {acc};
                margin-top: 0px;
                margin-bottom: 6px;
            }}
        """)
        if hasattr(self, "header"):
            self.header.setStyleSheet(f"font-size: 13px; font-weight: 800; letter-spacing: 0.5px; color: {txt};")
        if hasattr(self, "doc_display"):
            has_pix = self.doc_display.pixmap() is not None and not self.doc_display.pixmap().isNull()
            if has_pix:
                self.doc_display.setStyleSheet("""
                    QLabel#docDisplay {
                        background: rgba(0, 0, 0, 0.4);
                        border: 1px solid rgba(255, 255, 255, 0.16);
                        border-radius: 8px;
                    }
                """)
            else:
                self.doc_display.setStyleSheet(f"""
                    QLabel#docDisplay {{
                        background: rgba(0, 0, 0, 0.22);
                        border: 1px dashed rgba(255, 255, 255, 0.18);
                        border-radius: 8px;
                        color: {sub};
                        font-size: 11px;
                        font-weight: 600;
                    }}
                """)
        if hasattr(self, "status"):
            current_raw = self.status.text()
            if ">" in current_raw:
                raw = current_raw.split(">")[-2].replace("</span", "").strip() or "Ready to Draft"
            else:
                raw = current_raw.replace("●", "").strip() or "Ready to Draft"
            self._update_status_text(raw)

    def enterEvent(self, event):
        if hasattr(self, "_shadow"):
            self._shadow.setBlurRadius(28)
            self._shadow.setYOffset(10)
            try:
                c = QColor(self._theme_accent)
                self._shadow.setColor(QColor(c.red(), c.green(), c.blue(), 110))
            except Exception:
                self._shadow.setColor(QColor(0, 0, 0, 180))
        super().enterEvent(event)

    def leaveEvent(self, event):
        if hasattr(self, "_shadow"):
            self._shadow.setBlurRadius(14)
            self._shadow.setYOffset(4)
            self._shadow.setColor(QColor(0, 0, 0, 130))
        super().leaveEvent(event)

    def set_theme_accent(self, accent_hex: str, text_color: str = None, subtext_color: str = None):
        """Dynamically aligns card highlights and elevation glow with theme accent."""
        self._theme_accent = accent_hex
        if text_color:
            self._text_color = text_color
        if subtext_color:
            self._subtext_color = subtext_color
        self._apply_style()

    def set_document(self, pixmap: QPixmap, status_text: str = "") -> None:
        scaled = pixmap.scaled(
            self.doc_display.width() - 8,
            self.doc_display.height() - 8,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.doc_display.setPixmap(scaled)
        self.doc_display.setStyleSheet("""
            QLabel#docDisplay {
                background: rgba(0, 0, 0, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.16);
                border-radius: 8px;
            }
        """)
        if status_text:
            self._update_status_text(status_text)

    def clear_document(self) -> None:
        self.doc_display.clear()
        self.doc_display.setText(f"📄  {self.doc_type}\n\nClick to Open Template")
        self._update_status_text("Ready to Draft")

    def set_status(self, text: str) -> None:
        self.status.setText(text)


# ─── ScrollableDocumentViewer & Filmstrip ─────────────────────────────────────

class PageThumbnailCard(QFrame):
    """Clickable, styled page card in the Filmstrip with active state and page number."""
    clicked = Signal(int)

    def __init__(self, page_idx: int, pixmap: QPixmap, is_active: bool = False, accent: str = "#00adb5", parent=None):
        super().__init__(parent)
        self.page_idx = page_idx
        self.is_active = is_active
        self._accent = accent
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(f"Jump to Page {page_idx + 1}")
        
        # 3D Depth Shadow Effect
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(8)
        self._shadow.setYOffset(2)
        self._shadow.setColor(QColor(0, 0, 0, 90))
        self.setGraphicsEffect(self._shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.img_lbl = QLabel()
        self.img_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if pixmap and not pixmap.isNull():
            self.img_lbl.setPixmap(pixmap)
        layout.addWidget(self.img_lbl)

        self.lbl_num = QLabel(f"P. {page_idx + 1}")
        self.lbl_num.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_num)

        self._update_style()

    def set_active(self, active: bool):
        self.is_active = active
        self._update_style()

    def set_accent(self, accent: str):
        self._accent = accent
        self._update_style()

    def _update_style(self):
        if self.is_active:
            self.setStyleSheet(f"""
                PageThumbnailCard {{
                    background: rgba(255, 255, 255, 0.08);
                    border: 1.5px solid {self._accent};
                    border-radius: 6px;
                    margin-top: 1px;
                    margin-bottom: 3px;
                }}
                QLabel {{
                    color: {self._accent};
                    font-size: 9px;
                    font-weight: 700;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                PageThumbnailCard {{
                    background: rgba(255, 255, 255, 0.04);
                    border: 1px solid rgba(255, 255, 255, 0.12);
                    border-radius: 6px;
                    margin-top: 3px;
                    margin-bottom: 1px;
                }}
                PageThumbnailCard:hover {{
                    background: rgba(255, 255, 255, 0.09);
                    border: 1.5px solid {self._accent};
                    margin-top: 0px;
                    margin-bottom: 4px;
                }}
                QLabel {{
                    color: #a0a6b2;
                    font-size: 9px;
                    font-weight: 600;
                }}
                PageThumbnailCard:hover QLabel {{
                    color: {self._accent};
                }}
            """)

    def enterEvent(self, event):
        if hasattr(self, "_shadow"):
            self._shadow.setBlurRadius(16)
            self._shadow.setYOffset(5)
            try:
                c = QColor(self._accent)
                self._shadow.setColor(QColor(c.red(), c.green(), c.blue(), 130))
            except Exception:
                self._shadow.setColor(QColor(0, 0, 0, 140))
        super().enterEvent(event)

    def leaveEvent(self, event):
        if hasattr(self, "_shadow"):
            self._shadow.setBlurRadius(8)
            self._shadow.setYOffset(2)
            self._shadow.setColor(QColor(0, 0, 0, 90))
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.page_idx)
        super().mousePressEvent(event)


class ScrollableDocumentViewer(QScrollArea):
    """Horizontally-scrollable multi-page document strip in the bottom bar."""
    page_clicked = Signal(int)

    def __init__(self, width: int = 600, height: int = 68, parent=None):
        super().__init__(parent)
        self.setObjectName("documentViewer")
        self.setWidgetResizable(True)
        self.setFixedHeight(height)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("""
            QScrollArea#documentViewer {
                border: none;
                background: transparent;
            }
        """)

        self._container = QWidget()
        self._container.setObjectName("viewerContainer")
        self._h_layout = QHBoxLayout(self._container)
        self._h_layout.setSpacing(8)
        self._h_layout.setContentsMargins(4, 2, 4, 2)
        self._h_layout.addStretch()
        self.setWidget(self._container)

        self._cards = []
        self._active_page = 0
        self._accent_color = "#00adb5"
        self.total_pages = 0

    def set_theme_accent(self, accent_hex: str) -> None:
        self._accent_color = accent_hex
        for card in self._cards:
            card.set_accent(accent_hex)

    def set_pages(self, pixmaps: list, active_page: int = 0) -> None:
        """Populates the filmstrip with page thumbnail cards."""
        self.clear_pages()
        self._active_page = active_page

        if not pixmaps:
            # Fallback starter blank page thumbnail
            pm = QPixmap(36, 46)
            pm.fill(QColor(255, 255, 255))
            pixmaps = [pm]

        for idx, pm in enumerate(pixmaps):
            card = PageThumbnailCard(idx, pm, is_active=(idx == active_page), accent=self._accent_color)
            card.clicked.connect(self._on_card_clicked)
            self._cards.append(card)
            self._h_layout.insertWidget(self._h_layout.count() - 1, card)

        self.total_pages = len(self._cards)

    def add_page(self, pixmap: QPixmap) -> None:
        idx = len(self._cards)
        card = PageThumbnailCard(idx, pixmap, is_active=(idx == self._active_page), accent=self._accent_color)
        card.clicked.connect(self._on_card_clicked)
        self._cards.append(card)
        self._h_layout.insertWidget(self._h_layout.count() - 1, card)
        self.total_pages += 1

    def set_active_page(self, page_idx: int) -> None:
        self._active_page = page_idx
        for card in self._cards:
            card.set_active(card.page_idx == page_idx)

    def _on_card_clicked(self, page_idx: int) -> None:
        self.set_active_page(page_idx)
        self.page_clicked.emit(page_idx)

    def clear_pages(self) -> None:
        while self._h_layout.count() > 1:
            item = self._h_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._cards.clear()
        self.total_pages = 0