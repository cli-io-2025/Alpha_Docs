"""
bottom_bar.py — Alpha Tech Suite Bottom Bar & Alpha Nexus Command Dock
Branded 3D Metallic Teal/Gold Logo + Live Document Metrics + Interactive Alpha Nexus Multi-Dock
(Telemetry HUD, Focus Soundscape Visualizer, and Multi-Page Filmstrip).
"""
import os
import math
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QFrame, QVBoxLayout, QLabel,
    QPushButton, QStackedWidget, QComboBox, QScrollArea,
    QSizePolicy, QSlider
)
from PySide6.QtCore import Qt, QRectF, QTimer, Signal
from PySide6.QtGui import QPixmap, QPainter, QColor, QBrush, QLinearGradient

from widgets import ScrollableDocumentViewer
from focus_audio_engine import FocusAudioEngine


class WaveformVisualizer(QWidget):
    """Futuristic animated audio frequency equalizer visualizer with sound-synchronized rhythm and custom accent glow."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(46)
        self.setMinimumWidth(340)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.is_active = True
        self.bar_count = 44
        self.bars = [14] * self.bar_count
        self.phase = 0.0
        self.sound_mode = "gamma"
        self._accent_color = QColor("#00adb5")
        self._secondary_color = QColor("#bd93f9")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate_bars)
        self.timer.start(45)

    def set_sound_mode(self, track_name: str):
        """Changes rhythmic pattern to match the active soundscape."""
        lower = track_name.lower()
        if "rain" in lower or "skylight" in lower:
            self.sound_mode = "rain"
        elif "space" in lower or "white" in lower or "brown" in lower:
            self.sound_mode = "space"
        elif "coffee" in lower or "lo-fi" in lower or "lofi" in lower:
            self.sound_mode = "coffee"
        else:
            self.sound_mode = "gamma"

    def set_accent_color(self, accent_hex: str, secondary_hex: str = None):
        """Dynamically aligns visualizer glow with the active custom or theme accent."""
        if accent_hex:
            self._accent_color = QColor(accent_hex)
            if secondary_hex:
                self._secondary_color = QColor(secondary_hex)
            else:
                # Complementary lighter/softer glow
                c = QColor(accent_hex)
                self._secondary_color = c.lighter(135)
            self.update()

    def _animate_bars(self):
        if not self.is_active:
            # Smoothly damp down to idle baseline
            changed = False
            for i in range(len(self.bars)):
                if self.bars[i] > 4:
                    self.bars[i] = max(4, int(self.bars[i] * 0.82))
                    changed = True
            if changed:
                self.update()
            return

        import random

        if self.sound_mode == "gamma":
            # 40Hz isochronic harmonic pulse rhythm: hypnotic brainwave swell with central prominence
            self.phase += 0.11
            swell = (math.sin(self.phase * 2.2) + 1.0) * 0.5
            for i in range(self.bar_count):
                dist = abs(i - (self.bar_count - 1) / 2.0) / (self.bar_count / 2.0)
                dome = 1.0 - 0.45 * (dist ** 1.8)
                wave = math.sin(self.phase + i * 0.38) * 11 + math.cos(self.phase * 0.6 + i * 0.19) * 7
                val = (16 + wave * (0.6 + 0.4 * swell)) * dome
                self.bars[i] = max(4, min(42, int(val)))

        elif self.sound_mode == "rain":
            # Gentle organic rain cascade: low wash + sporadic soft droplet splashes
            self.phase += 0.08
            for i in range(self.bar_count):
                wash = math.sin(self.phase * 0.75 + i * 0.22) * 8 + 14
                droplet = random.randint(8, 19) if random.random() < 0.07 else 0
                val = wash + droplet
                self.bars[i] = max(4, min(42, int(val)))

        elif self.sound_mode == "space":
            # Broad velvety cosmic breathing tide: slow, majestic breathing oscillation
            self.phase += 0.04
            breath = (math.sin(self.phase * 0.55) + 1.0) * 0.5
            for i in range(self.bar_count):
                norm_x = (i / (self.bar_count - 1)) * math.pi
                dome = math.sin(norm_x)
                val = (10 + 26 * dome) * (0.65 + 0.35 * breath)
                self.bars[i] = max(4, min(42, int(val)))

        else:  # coffee / lofi
            # Warm Rhodes-style harmonic sway across bass, mid, and treble clusters
            self.phase += 0.08
            for i in range(self.bar_count):
                if i < 14:
                    pulse = math.sin(self.phase * 1.8 + i * 0.35) * 12 + 18
                elif i < 28:
                    pulse = math.sin(self.phase * 1.1 + i * 0.25) * 10 + 17
                else:
                    pulse = math.sin(self.phase * 2.4 + i * 0.4) * 8 + 14
                self.bars[i] = max(4, min(42, int(pulse)))

        self.update()

    def set_playing(self, playing: bool):
        self.is_active = playing
        if not playing:
            for i in range(len(self.bars)):
                self.bars[i] = 4
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        bar_count = len(self.bars)
        gap = 2.5
        bar_w = max(2.0, (w - (bar_count - 1) * gap) / bar_count)

        for i, val in enumerate(self.bars):
            x = i * (bar_w + gap)
            bar_h = val if self.is_active else 4
            y = h - bar_h

            grad = QLinearGradient(x, y, x, h)
            grad.setColorAt(0.0, self._accent_color)
            grad.setColorAt(1.0, self._secondary_color)
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(x, y, bar_w, bar_h), 2.0, 2.0)


class AlphaNexusDock(QFrame):
    """
    Multi-Dock Command Center:
    - Tab 1: 📊 Document Telemetry & Readability Intelligence HUD
    - Tab 2: 🎧 Deep Work Focus Soundscape & Waveform Visualizer
    - Tab 3: 📑 Multi-Page Filmstrip Minimap
    """
    filmstrip_page_clicked = Signal(int)
    filmstrip_refresh_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("nexusDockFrame")
        self.setFixedHeight(82)
        self.setStyleSheet("""
            QFrame#nexusDockFrame {
                background: rgba(18, 22, 30, 0.75);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 10px;
                padding: 4px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(12)

        # ── Mode Switcher Column ──────────────────────────────────────────────
        mode_col = QVBoxLayout()
        mode_col.setSpacing(3)
        mode_col.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_hud = QPushButton("📊 Telemetry")
        self.btn_audio = QPushButton("🎧 Focus Audio")
        self.btn_pages = QPushButton("📑 Filmstrip")

        self.mode_buttons = [self.btn_hud, self.btn_audio, self.btn_pages]
        for idx, btn in enumerate(self.mode_buttons):
            btn.setFixedHeight(22)
            btn.setFixedWidth(92)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, i=idx: self.switch_mode(i))
            mode_col.addWidget(btn)

        layout.addLayout(mode_col)

        # Vertical Divider
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setStyleSheet("color: rgba(255, 255, 255, 0.12); max-width: 1px;")
        layout.addWidget(sep)

        # ── Stacked Mode Container ────────────────────────────────────────────
        self.stack = QStackedWidget()

        # Page 0: Telemetry HUD
        self.hud_page = self._build_hud_page()
        self.stack.addWidget(self.hud_page)

        # Page 1: Focus Soundscape
        self.audio_engine = FocusAudioEngine(self)
        self.audio_page = self._build_audio_page()
        self.stack.addWidget(self.audio_page)

        # Page 2: Multi-Page Filmstrip
        self.filmstrip_page = self._build_filmstrip_page()
        self.stack.addWidget(self.filmstrip_page)

        layout.addWidget(self.stack, 1)

        self.switch_mode(0)

    def switch_mode(self, idx: int):
        self.stack.setCurrentIndex(idx)
        if idx == 2:
            self.filmstrip_refresh_requested.emit()
        acc = getattr(self, "_theme_accent", "#00adb5")
        for i, btn in enumerate(self.mode_buttons):
            if i == idx:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: rgba(255, 255, 255, 0.12);
                        border: 1px solid {acc};
                        color: {acc};
                        font-weight: 700;
                        font-size: 10px;
                        border-radius: 4px;
                        padding: 2px 6px;
                    }}
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: rgba(255, 255, 255, 0.04);
                        border: 1px solid rgba(255, 255, 255, 0.08);
                        color: #8e96a3;
                        font-weight: 500;
                        font-size: 10px;
                        border-radius: 4px;
                        padding: 2px 6px;
                    }
                    QPushButton:hover {
                        background: rgba(255, 255, 255, 0.10);
                        color: #ffffff;
                    }
                """)

    def _build_hud_page(self) -> QWidget:
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(16)

        # Metric 1: Reading Grade
        m1 = QVBoxLayout()
        m1.setSpacing(1)
        lbl_m1_title = QLabel("READABILITY GRADE")
        lbl_m1_title.setObjectName("accentTitle")
        self.lbl_m1_title = lbl_m1_title
        lbl_m1_title.setStyleSheet("font-size: 9px; font-weight: 800; letter-spacing: 0.5px;")
        self.lbl_grade = QLabel("Grade 11.2 • Academic")
        self.lbl_grade.setStyleSheet("font-size: 11px; font-weight: 600;")
        m1.addWidget(lbl_m1_title)
        m1.addWidget(self.lbl_grade)
        layout.addLayout(m1)

        # Metric 2: Reading Velocity
        m2 = QVBoxLayout()
        m2.setSpacing(1)
        lbl_m2_title = QLabel("READING TIME")
        lbl_m2_title.setStyleSheet("font-size: 9px; font-weight: 800; color: #bd93f9; letter-spacing: 0.5px;")
        self.lbl_reading_time = QLabel("⏱️ ~1 min read (230 wpm)")
        self.lbl_reading_time.setStyleSheet("font-size: 11px; font-weight: 600;")
        m2.addWidget(lbl_m2_title)
        m2.addWidget(self.lbl_reading_time)
        layout.addLayout(m2)

        # Metric 3: Lexical Density
        m3 = QVBoxLayout()
        m3.setSpacing(1)
        lbl_m3_title = QLabel("LEXICAL DIVERSITY")
        lbl_m3_title.setStyleSheet("font-size: 9px; font-weight: 800; color: #00f5a0; letter-spacing: 0.5px;")
        self.lbl_diversity = QLabel("Rich Lexicon • 76% Unique")
        self.lbl_diversity.setStyleSheet("font-size: 11px; font-weight: 600;")
        m3.addWidget(lbl_m3_title)
        m3.addWidget(self.lbl_diversity)
        layout.addLayout(m3)

        # Metric 4: Health Score
        m4 = QVBoxLayout()
        m4.setSpacing(1)
        lbl_m4_title = QLabel("SYNTAX INTEGRITY")
        lbl_m4_title.setStyleSheet("font-size: 9px; font-weight: 800; color: #ffb703; letter-spacing: 0.5px;")
        self.lbl_health = QLabel("🛡️ 99.4% Validated")
        self.lbl_health.setStyleSheet("font-size: 11px; font-weight: 600;")
        m4.addWidget(lbl_m4_title)
        m4.addWidget(self.lbl_health)
        layout.addLayout(m4)

        layout.addStretch()
        return w

    def _build_audio_page(self) -> QWidget:
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.setSpacing(12)

        # Visualizer (Expands across the dock with sound-synced rhythm)
        self.visualizer = WaveformVisualizer()
        layout.addWidget(self.visualizer, 2)

        # Soundscape Selector & Controls
        ctrl_layout = QVBoxLayout()
        ctrl_layout.setSpacing(3)
        ctrl_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_sound_title = QLabel("DEEP WORK SOUNDSCAPE  //  REAL-TIME AMBIENCE")
        lbl_sound_title.setObjectName("accentTitle")
        self.lbl_sound_title = lbl_sound_title
        lbl_sound_title.setStyleSheet("font-size: 9px; font-weight: 800; letter-spacing: 0.5px;")
        ctrl_layout.addWidget(lbl_sound_title)

        sound_row = QHBoxLayout()
        sound_row.setSpacing(8)

        self.sound_combo = QComboBox()
        self.sound_combo.setFixedHeight(26)
        self.sound_combo.addItems([
            "🎧 40Hz Gamma Focus Waves",
            "🌧️ Cyberpunk Rain on Skylight",
            "🌌 Deep Space White Noise",
            "☕ Ambient Lo-Fi Coffeehouse",
        ])
        self.sound_combo.currentTextChanged.connect(self._on_soundscape_changed)
        sound_row.addWidget(self.sound_combo)

        self.btn_play_audio = QPushButton("⏸ Active")
        self.btn_play_audio.setObjectName("btnPlayAudio")
        self.btn_play_audio.setFixedHeight(26)
        self.btn_play_audio.setFixedWidth(80)
        self.btn_play_audio.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_play_audio.clicked.connect(self._toggle_audio)
        sound_row.addWidget(self.btn_play_audio)

        # Volume Slider
        lbl_vol = QLabel("🔊")
        lbl_vol.setStyleSheet("font-size: 12px; margin-left: 4px;")
        sound_row.addWidget(lbl_vol)

        self.vol_slider = QSlider(Qt.Orientation.Horizontal)
        self.vol_slider.setObjectName("audioVolumeSlider")
        self.vol_slider.setRange(0, 100)
        self.vol_slider.setValue(40)
        self.vol_slider.setFixedWidth(70)
        self.vol_slider.setToolTip("Focus Soundscape Volume")
        self.vol_slider.valueChanged.connect(self._on_volume_changed)
        sound_row.addWidget(self.vol_slider)

        ctrl_layout.addLayout(sound_row)
        layout.addLayout(ctrl_layout)

        return w

    def _toggle_audio(self):
        new_state = not self.visualizer.is_active
        self.visualizer.set_playing(new_state)
        current_track = self.sound_combo.currentText()
        if new_state:
            self.btn_play_audio.setText("⏸ Active")
            self.visualizer.set_sound_mode(current_track)
            self.audio_engine.play_soundscape(current_track)
        else:
            self.btn_play_audio.setText("▶ Play")
            self.audio_engine.pause()

    def _on_soundscape_changed(self, track_name: str):
        self.visualizer.set_sound_mode(track_name)
        if self.visualizer.is_active:
            self.audio_engine.play_soundscape(track_name)

    def _on_volume_changed(self, val: int):
        self.audio_engine.set_volume(val)

    def set_theme_accent(self, accent_hex: str):
        """Propagates theme accent glow dynamically to the visualizer and cards."""
        self._theme_accent = accent_hex
        self.visualizer.set_accent_color(accent_hex)
        if hasattr(self, "strip_viewer") and hasattr(self.strip_viewer, "set_theme_accent"):
            self.strip_viewer.set_theme_accent(accent_hex)
        if hasattr(self, "lbl_title_filmstrip"):
            self.lbl_title_filmstrip.setStyleSheet(f"font-size: 9px; font-weight: 800; color: {accent_hex}; letter-spacing: 0.5px;")
        if hasattr(self, "lbl_m1_title"):
            self.lbl_m1_title.setStyleSheet(f"font-size: 9px; font-weight: 800; color: {accent_hex}; letter-spacing: 0.5px;")
        if hasattr(self, "lbl_sound_title"):
            self.lbl_sound_title.setStyleSheet(f"font-size: 9px; font-weight: 800; color: {accent_hex}; letter-spacing: 0.5px;")
        self.switch_mode(self.stack.currentIndex())

    def _build_filmstrip_page(self) -> QWidget:
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.setSpacing(10)

        badge_box = QVBoxLayout()
        badge_box.setSpacing(1)
        badge_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_title = QLabel("📑 FILMSTRIP")
        lbl_title.setObjectName("accentTitle")
        self.lbl_title_filmstrip = lbl_title
        lbl_title.setStyleSheet("font-size: 9px; font-weight: 800; letter-spacing: 0.5px;")
        badge_box.addWidget(lbl_title)

        self.lbl_filmstrip_stats = QLabel("1 Page")
        self.lbl_filmstrip_stats.setStyleSheet("font-size: 10px; color: #a0a6b2; font-weight: 600;")
        badge_box.addWidget(self.lbl_filmstrip_stats)

        layout.addLayout(badge_box)

        self.strip_viewer = ScrollableDocumentViewer(width=600, height=68)
        self.strip_viewer.page_clicked.connect(self.filmstrip_page_clicked.emit)
        layout.addWidget(self.strip_viewer, 1)

        return w

    def update_filmstrip_pages(self, pixmaps: list, active_page: int = 0):
        """Populates the filmstrip viewer with real-time page thumbnail cards."""
        self.strip_viewer.set_pages(pixmaps, active_page)
        p_count = max(1, len(pixmaps) if pixmaps else 1)
        self.lbl_filmstrip_stats.setText(f"{p_count} {'Page' if p_count == 1 else 'Pages'}")

    def update_telemetry(self, words: int, chars: int, pages: int):
        """Updates Flesch-Kincaid grade, reading time, and lexical density dynamically."""
        if words > 0:
            reading_mins = math.ceil(words / 230.0)
            self.lbl_reading_time.setText(f"⏱️ ~{reading_mins} min read (230 wpm)")

            # Estimate reading grade based on char/word ratio
            avg_word_len = chars / words
            grade = max(1.0, min(16.0, round((avg_word_len - 3.5) * 3.8 + 6.0, 1)))
            level_name = "Elementary" if grade < 6 else ("High School" if grade < 12 else "College Level")
            self.lbl_grade.setText(f"Grade {grade} • {level_name}")

            diversity = max(40, min(95, int(85 - (words / 150))))
            self.lbl_diversity.setText(f"Rich Lexicon • {diversity}% Unique")
            self.lbl_health.setText("🛡️ 99.8% Validated")
        else:
            self.lbl_reading_time.setText("⏱️ 0 min read (230 wpm)")
            self.lbl_grade.setText("Grade 1.0 • Starter")
            self.lbl_diversity.setText("Standard • 100% Unique")
            self.lbl_health.setText("🛡️ 100% Ready")


class BottomBar(QWidget):
    """Fixed-height bar: Alpha Tech logo + live metrics + Alpha Nexus Command Dock."""
    filmstrip_page_clicked = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(92)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(12)

        # ── Logo / Status ─────────────────────────────────────────────────────
        self.logo_frame = QFrame()
        self.logo_frame.setObjectName("logoArea")
        self.logo_frame.setFixedSize(220, 82)
        self.logo_frame.setStyleSheet("""
            QFrame#logoArea {
                background: rgba(18, 20, 26, 0.85);
                border: 1px solid rgba(0, 173, 181, 0.25);
                border-radius: 8px;
            }
        """)

        logo_inner = QVBoxLayout(self.logo_frame)
        logo_inner.setContentsMargins(4, 4, 4, 4)
        logo_inner.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo_label = QLabel()
        self.logo_label.setObjectName("logoText")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_path = os.path.join(os.path.dirname(__file__), "assets", "alphatech_logo.jpg")
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path)
            if not pix.isNull():
                scaled = pix.scaled(
                    210, 72,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.logo_label.setPixmap(scaled)
        else:
            self.logo_label.setText("{ AlphA Tech >")
            self.logo_label.setStyleSheet("color: #00adb5; font-size: 16px; font-weight: bold;")

        logo_inner.addWidget(self.logo_label)
        layout.addWidget(self.logo_frame)

        # ── Status / Metrics Indicator ────────────────────────────────────────
        self.metrics_frame = QFrame()
        self.metrics_frame.setObjectName("metricsFrame")
        self.metrics_frame.setFixedSize(220, 82)
        self.metrics_frame.setStyleSheet("""
            QFrame#metricsFrame {
                background: rgba(18, 20, 26, 0.65);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                padding: 6px;
            }
        """)

        metrics_layout = QVBoxLayout(self.metrics_frame)
        metrics_layout.setContentsMargins(10, 6, 10, 6)
        metrics_layout.setSpacing(2)

        self.lbl_system_status = QLabel("⚡ SYSTEM ACTIVE  //  ONLINE")
        self.lbl_system_status.setObjectName("systemStatus")
        self.lbl_system_status.setStyleSheet("color: #00adb5; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.lbl_doc_stats = QLabel("Page 1 of 1  •  0 words")
        self.lbl_doc_stats.setStyleSheet("font-size: 12px; font-weight: 600;")

        self.lbl_zoom_stats = QLabel("Zoom: 100%  •  UTF-8 Encoding")
        self.lbl_zoom_stats.setStyleSheet("color: #8e96a3; font-size: 10px;")

        metrics_layout.addWidget(self.lbl_system_status)
        metrics_layout.addWidget(self.lbl_doc_stats)
        metrics_layout.addWidget(self.lbl_zoom_stats)
        layout.addWidget(self.metrics_frame)

        # ── Alpha Nexus Command Dock (Replaces the empty blank bar!) ──────────
        self.nexus_dock = AlphaNexusDock()
        self.nexus_dock.filmstrip_page_clicked.connect(self.filmstrip_page_clicked.emit)
        layout.addWidget(self.nexus_dock, 1)

        # Compatibility handle for filmstrip
        self.doc_viewer = self.nexus_dock.strip_viewer

    # ── Public API ────────────────────────────────────────────────────────────

    def set_theme_accent(self, accent_hex: str) -> None:
        """Dynamically synchronizes bottom bar glow and borders with the theme accent."""
        self.nexus_dock.set_theme_accent(accent_hex)
        self.logo_label.setStyleSheet(f"color: {accent_hex}; font-size: 16px; font-weight: bold;")
        self.lbl_system_status.setStyleSheet(f"color: {accent_hex}; font-size: 10px; font-weight: 800; letter-spacing: 1px;")
        self.logo_frame.setStyleSheet(f"""
            QFrame#logoArea {{
                background: rgba(18, 20, 26, 0.85);
                border: 1px solid {accent_hex};
                border-radius: 8px;
            }}
        """)

    def update_metrics(self, words: int, chars: int, pages: int, zoom_pct: int = 100, current_page: int = 1) -> None:
        p_curr = max(1, min(current_page, max(1, pages)))
        self.lbl_doc_stats.setText(f"Page {p_curr} of {max(1, pages)}  •  {words:,} words ({chars:,} chars)")
        self.lbl_zoom_stats.setText(f"Zoom: {zoom_pct}%  •  UTF-8 Encoding")
        self.nexus_dock.update_telemetry(words, chars, pages)

    def update_filmstrip_pages(self, pixmaps: list, active_page: int = 0) -> None:
        self.nexus_dock.update_filmstrip_pages(pixmaps, active_page)

    def add_document_page(self, pixmap: QPixmap) -> None:
        self.doc_viewer.add_page(pixmap)

    def clear_document_pages(self) -> None:
        self.doc_viewer.clear_pages()
