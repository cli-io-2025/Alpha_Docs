"""
template_picker.py — Resume Template Studio & Gallery Picker
Displays curated resume layouts with high-resolution visual previews,
badges, descriptions, and one-click 'Create Copy & Edit' workflow.
"""
import os
from PySide6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QGraphicsDropShadowEffect, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPixmap, QCursor


class ResumeTemplateCard(QFrame):
    """Interactive card showcasing a resume template with preview thumbnail and hover raise."""
    card_selected = Signal(str)

    def __init__(self, key: str, title: str, badge: str, desc: str, image_filename: str,
                 accent: str = "#00adb5", text_color: str = "#f0f4f8", subtext_color: str = "#9aa5b5", parent=None):
        super().__init__(parent)
        self.key = key
        self.title_text = title
        self.badge_text = badge
        self.desc_text = desc
        self.image_filename = image_filename
        self._accent = accent
        self._text_color = text_color
        self._subtext_color = subtext_color

        self.setObjectName("templateCard")
        self.setFixedSize(260, 520)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # 3D Depth Shadow
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(14)
        self._shadow.setYOffset(4)
        self._shadow.setColor(QColor(0, 0, 0, 140))
        self.setGraphicsEffect(self._shadow)

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 14, 12, 14)
        layout.setSpacing(10)

        # ── Preview Thumbnail ─────────────────────────────────────────────────
        self.img_label = QLabel()
        self.img_label.setObjectName("templatePreview")
        self.img_label.setFixedSize(236, 280)
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        img_path = os.path.join(assets_dir, image_filename)
        if os.path.exists(img_path):
            pix = QPixmap(img_path)
            if not pix.isNull():
                scaled = pix.scaled(
                    234, 278,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.img_label.setPixmap(scaled)

        # ── Badge ─────────────────────────────────────────────────────────────
        self.lbl_badge = QLabel(badge.upper())
        self.lbl_badge.setObjectName("templateBadge")
        self.lbl_badge.setFixedHeight(22)
        self.lbl_badge.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # ── Title ─────────────────────────────────────────────────────────────
        self.lbl_title = QLabel(title)
        self.lbl_title.setObjectName("templateTitle")
        self.lbl_title.setFixedHeight(24)

        # ── Description ───────────────────────────────────────────────────────
        self.lbl_desc = QLabel(desc)
        self.lbl_desc.setObjectName("templateDesc")
        self.lbl_desc.setWordWrap(True)
        self.lbl_desc.setFixedHeight(60)

        # ── Action Button ─────────────────────────────────────────────────────
        self.btn_select = QPushButton("⚡ Create Copy & Edit")
        self.btn_select.setObjectName("btnCreateCopy")
        self.btn_select.setFixedHeight(36)
        self.btn_select.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_select.clicked.connect(lambda: self.card_selected.emit(self.key))

        layout.addWidget(self.img_label)
        layout.addWidget(self.lbl_badge)
        layout.addWidget(self.lbl_title)
        layout.addWidget(self.lbl_desc)
        layout.addStretch()
        layout.addWidget(self.btn_select)

        self.setLayout(layout)
        self.apply_style()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.card_selected.emit(self.key)
        super().mousePressEvent(event)

    def enterEvent(self, event):
        if hasattr(self, "_shadow"):
            self._shadow.setBlurRadius(28)
            self._shadow.setYOffset(10)
            try:
                c = QColor(self._accent)
                self._shadow.setColor(QColor(c.red(), c.green(), c.blue(), 130))
            except Exception:
                self._shadow.setColor(QColor(0, 0, 0, 180))
        super().enterEvent(event)

    def leaveEvent(self, event):
        if hasattr(self, "_shadow"):
            self._shadow.setBlurRadius(14)
            self._shadow.setYOffset(4)
            self._shadow.setColor(QColor(0, 0, 0, 140))
        super().leaveEvent(event)

    def apply_style(self):
        acc = self._accent
        txt = self._text_color
        sub = self._subtext_color

        self.setStyleSheet(f"""
            QFrame#templateCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(25, 28, 38, 0.95), stop:1 rgba(16, 18, 25, 0.95));
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-top: 3.5px solid {acc};
                border-radius: 12px;
                margin-top: 6px;
                margin-bottom: 0px;
            }}
            QFrame#templateCard:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(32, 36, 48, 0.98), stop:1 rgba(22, 24, 34, 0.98));
                border: 1.5px solid {acc};
                border-top: 4px solid {acc};
                margin-top: 0px;
                margin-bottom: 6px;
            }}
            QLabel#templatePreview {{
                background: rgba(0, 0, 0, 0.35);
                border: 1px solid rgba(255, 255, 255, 0.14);
                border-radius: 8px;
            }}
            QLabel#templateBadge {{
                color: {acc};
                font-size: 10px;
                font-weight: 800;
                letter-spacing: 1px;
            }}
            QLabel#templateTitle {{
                color: {txt};
                font-size: 16px;
                font-weight: bold;
            }}
            QLabel#templateDesc {{
                color: {sub};
                font-size: 11px;
                line-height: 1.3;
            }}
            QPushButton#btnCreateCopy {{
                background: {acc};
                color: #ffffff;
                font-size: 12px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 6px 14px;
            }}
            QPushButton#btnCreateCopy:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {acc}, stop:1 #ffffff);
                color: #121212;
            }}
        """)


class ResumeTemplatePicker(QDialog):
    """Studio modal to choose and create a fresh working copy of a curated resume template."""

    def __init__(self, parent=None, accent: str = "#00adb5", text_color: str = "#f0f4f8", subtext_color: str = "#9aa5b5"):
        super().__init__(parent)
        self.setWindowTitle("Resume Template Studio — Alpha_Doc Suite")
        self.setModal(True)
        self.setFixedSize(1160, 680)
        self.selected_template_key = None
        self._accent = accent
        self._text_color = text_color
        self._subtext_color = subtext_color

        # Overall Dialog Styling
        self.setStyleSheet(f"""
            QDialog {{
                background: #111319;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 14px;
            }}
        """)

        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setSpacing(18)

        # ── Top Header ────────────────────────────────────────────────────────
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        title_col = QVBoxLayout()
        title_col.setSpacing(4)

        main_title = QLabel("👔  Resume Template Studio")
        main_title.setStyleSheet(f"color: {text_color}; font-size: 22px; font-weight: 800; letter-spacing: 0.5px;")
        subtitle = QLabel("Select a designer layout to create a fresh, fully editable copy in your workspace.")
        subtitle.setStyleSheet(f"color: {subtext_color}; font-size: 12px;")

        title_col.addWidget(main_title)
        title_col.addWidget(subtitle)
        header_layout.addLayout(title_col)
        header_layout.addStretch()

        btn_close = QPushButton("✕")
        btn_close.setFixedSize(32, 32)
        btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_close.setStyleSheet(f"""
            QPushButton {{
                background: rgba(255, 255, 255, 0.08);
                color: {text_color};
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
                border: 1px solid rgba(255, 255, 255, 0.12);
            }}
            QPushButton:hover {{
                background: rgba(239, 68, 68, 0.85);
                color: #ffffff;
            }}
        """)
        btn_close.clicked.connect(self.reject)
        header_layout.addWidget(btn_close)

        root_layout.addLayout(header_layout)

        # ── Scrollable Cards Row ──────────────────────────────────────────────
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:horizontal {
                height: 8px;
                background: rgba(0, 0, 0, 0.2);
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background: rgba(255, 255, 255, 0.25);
                border-radius: 4px;
            }
        """)

        cards_container = QWidget()
        cards_container.setStyleSheet("background: transparent;")
        cards_layout = QHBoxLayout(cards_container)
        cards_layout.setContentsMargins(4, 4, 4, 4)
        cards_layout.setSpacing(16)

        from document_presets import RESUME_TEMPLATES_CATALOG
        for key, meta in RESUME_TEMPLATES_CATALOG.items():
            card = ResumeTemplateCard(
                key=key,
                title=meta["title"],
                badge=meta["badge"],
                desc=meta["description"],
                image_filename=meta["image_file"],
                accent=self._accent,
                text_color=self._text_color,
                subtext_color=self._subtext_color,
                parent=self
            )
            card.card_selected.connect(self._on_card_selected)
            cards_layout.addWidget(card)

        scroll_area.setWidget(cards_container)
        root_layout.addWidget(scroll_area)
        self.setLayout(root_layout)

    def _on_card_selected(self, key: str):
        self.selected_template_key = key
        self.accept()


class BrochureTemplatePicker(QDialog):
    """Studio modal to choose and create a fresh working copy of a curated brochure template."""

    def __init__(self, parent=None, accent: str = "#00adb5", text_color: str = "#f0f4f8", subtext_color: str = "#9aa5b5"):
        super().__init__(parent)
        self.setWindowTitle("Brochure Template Studio — Alpha_Doc Suite")
        self.setModal(True)
        self.setFixedSize(1160, 680)
        self.selected_template_key = None
        self._accent = accent
        self._text_color = text_color
        self._subtext_color = subtext_color

        # Overall Dialog Styling
        self.setStyleSheet(f"""
            QDialog {{
                background: #111319;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 14px;
            }}
        """)

        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setSpacing(18)

        # ── Top Header ────────────────────────────────────────────────────────
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        title_col = QVBoxLayout()
        title_col.setSpacing(4)

        main_title = QLabel("🏖️  Brochure Template Studio")
        main_title.setStyleSheet(f"color: {text_color}; font-size: 22px; font-weight: 800; letter-spacing: 0.5px;")
        subtitle = QLabel("Select a publication spread to create a fresh, fully editable copy in your workspace.")
        subtitle.setStyleSheet(f"color: {subtext_color}; font-size: 12px;")

        title_col.addWidget(main_title)
        title_col.addWidget(subtitle)
        header_layout.addLayout(title_col)
        header_layout.addStretch()

        btn_close = QPushButton("✕")
        btn_close.setFixedSize(32, 32)
        btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_close.setStyleSheet(f"""
            QPushButton {{
                background: rgba(255, 255, 255, 0.08);
                color: {text_color};
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
                border: 1px solid rgba(255, 255, 255, 0.12);
            }}
            QPushButton:hover {{
                background: rgba(239, 68, 68, 0.85);
                color: #ffffff;
            }}
        """)
        btn_close.clicked.connect(self.reject)
        header_layout.addWidget(btn_close)

        root_layout.addLayout(header_layout)

        # ── Scrollable Cards Row ──────────────────────────────────────────────
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:horizontal {
                height: 8px;
                background: rgba(0, 0, 0, 0.2);
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background: rgba(255, 255, 255, 0.25);
                border-radius: 4px;
            }
        """)

        cards_container = QWidget()
        cards_container.setStyleSheet("background: transparent;")
        cards_layout = QHBoxLayout(cards_container)
        cards_layout.setContentsMargins(4, 4, 4, 4)
        cards_layout.setSpacing(16)

        from document_presets import BROCHURE_TEMPLATES_CATALOG
        for key, meta in BROCHURE_TEMPLATES_CATALOG.items():
            card = ResumeTemplateCard(
                key=key,
                title=meta["title"],
                badge=meta["badge"],
                desc=meta["description"],
                image_filename=meta["image_file"],
                accent=self._accent,
                text_color=self._text_color,
                subtext_color=self._subtext_color,
                parent=self
            )
            card.card_selected.connect(self._on_card_selected)
            cards_layout.addWidget(card)

        scroll_area.setWidget(cards_container)
        root_layout.addWidget(scroll_area)
        self.setLayout(root_layout)

    def _on_card_selected(self, key: str):
        self.selected_template_key = key
        self.accept()

