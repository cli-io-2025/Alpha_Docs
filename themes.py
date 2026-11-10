"""
themes.py — Alpha Tech Enterprise Glassmorphism Theme Engine
Includes 7 pre-engineered high-contrast palettes plus a dynamic Custom Theme engine.
Applies frosted-glass aesthetics, soft shadows, rounded corners, and glowing accent rims.
"""
from dataclasses import dataclass
import json
import os
from PySide6.QtGui import QColor


@dataclass
class Theme:
    name: str
    # ── Backgrounds ──────────────────────────────────
    bg_primary:   str
    bg_secondary: str
    bg_tertiary:  str
    bg_input:     str
    # ── Borders ──────────────────────────────────────
    border:       str
    border_hover: str
    # ── Text ─────────────────────────────────────────
    text_primary:   str
    text_secondary: str
    text_muted:     str
    text_bright:    str
    # ── Accent ───────────────────────────────────────
    accent:         str
    accent_hover:   str
    accent_pressed: str
    # ── Scrollbars ───────────────────────────────────
    scroll_bg:     str
    scroll_handle: str
    scroll_hover:  str


# ─── Theme Palettes ───────────────────────────────────────────────────────────

BLUE = Theme(
    name="Blue",
    bg_primary="#0e1117",    bg_secondary="#151922",
    bg_tertiary="#1a202c",   bg_input="#1f2634",
    border="#252d3d",        border_hover="#364156",
    text_primary="#c2c8d5",  text_secondary="#a2abbd",
    text_muted="#667389",    text_bright="#ffffff",
    accent="#00adb5",        accent_hover="#00c4ce",   accent_pressed="#00939a",
    scroll_bg="#0b0d12",     scroll_handle="#263143",  scroll_hover="#00adb5",
)

DARK = Theme(
    name="Dark",
    bg_primary="#090a0d",    bg_secondary="#11131a",
    bg_tertiary="#171a24",   bg_input="#1c202d",
    border="#212636",        border_hover="#2e354a",
    text_primary="#949dae",  text_secondary="#727c8d",
    text_muted="#4a5364",    text_bright="#dce2ed",
    accent="#3e4d65",        accent_hover="#4f6280",   accent_pressed="#2f3b4e",
    scroll_bg="#06070a",     scroll_handle="#1e2536",  scroll_hover="#3e4d65",
)

MOCHA = Theme(
    name="Mocha",
    bg_primary="#f4efe6",    bg_secondary="#eae3d6",
    bg_tertiary="#dfd7c8",   bg_input="#eee8dc",
    border="#d0c7b6",        border_hover="#bdb39e",
    text_primary="#382e25",  text_secondary="#5a4d41",
    text_muted="#8c7d70",    text_bright="#1b1007",
    accent="#b8834c",        accent_hover="#cc9560",   accent_pressed="#a47040",
    scroll_bg="#dbd3c5",     scroll_handle="#c0b9a9",  scroll_hover="#b8834c",
)

CYBERPUNK = Theme(
    name="Cyberpunk",
    bg_primary="#0d0c1d",    bg_secondary="#15132c",
    bg_tertiary="#1c193c",   bg_input="#231f4c",
    border="#312a64",        border_hover="#483e92",
    text_primary="#d3cbe8",  text_secondary="#b4a7d6",
    text_muted="#74679a",    text_bright="#ffffff",
    accent="#bd93f9",        accent_hover="#ff79c6",   accent_pressed="#9867db",
    scroll_bg="#090814",     scroll_handle="#2d265d",  scroll_hover="#bd93f9",
)

EMERALD = Theme(
    name="Emerald",
    bg_primary="#090f0c",    bg_secondary="#0e1713",
    bg_tertiary="#14211b",   bg_input="#1a2b23",
    border="#213a2e",        border_hover="#2e5442",
    text_primary="#c3dbd0",  text_secondary="#9cbfae",
    text_muted="#5a7e6c",    text_bright="#ffffff",
    accent="#00f5a0",        accent_hover="#26ffb0",   accent_pressed="#00c781",
    scroll_bg="#060a08",     scroll_handle="#1d3529",  scroll_hover="#00f5a0",
)

SOLAR = Theme(
    name="Solar",
    bg_primary="#14110d",    bg_secondary="#1c1813",
    bg_tertiary="#26201a",   bg_input="#302922",
    border="#3d332a",        border_hover="#57493c",
    text_primary="#dbcbbd",  text_secondary="#bda897",
    text_muted="#786554",    text_bright="#ffffff",
    accent="#ffb703",        accent_hover="#ffc633",   accent_pressed="#e09f00",
    scroll_bg="#0d0b09",     scroll_handle="#3b3127",  scroll_hover="#ffb703",
)

NORDIC = Theme(
    name="Nordic",
    bg_primary="#f0f4f8",    bg_secondary="#e4ebf2",
    bg_tertiary="#d7e2ec",   bg_input="#e9f0f6",
    border="#c7d5e4",        border_hover="#b2c4d6",
    text_primary="#2d3748",  text_secondary="#4a5568",
    text_muted="#718096",    text_bright="#1a202c",
    accent="#0284c7",        accent_hover="#039be5",   accent_pressed="#026aa2",
    scroll_bg="#d8e2ec",     scroll_handle="#bcccdc",  scroll_hover="#0284c7",
)

CUSTOM = Theme(
    name="Custom",
    bg_primary="#0f1115",    bg_secondary="#161920",
    bg_tertiary="#1b212c",   bg_input="#1f2430",
    border="#232834",        border_hover="#343d46",
    text_primary="#c0c5ce",  text_secondary="#a6acb9",
    text_muted="#65737e",    text_bright="#ffffff",
    accent="#00adb5",        accent_hover="#00c2cb",   accent_pressed="#00939a",
    scroll_bg="#101216",     scroll_handle="#2b3542",  scroll_hover="#00adb5",
)

ALL_THEMES: dict[str, Theme] = {
    "Blue": BLUE,
    "Dark": DARK,
    "Mocha": MOCHA,
    "Cyberpunk": CYBERPUNK,
    "Emerald": EMERALD,
    "Solar": SOLAR,
    "Nordic": NORDIC,
    "Custom": CUSTOM,
}


# ─── Preference Persistence ───────────────────────────────────────────────────

def get_theme_prefs_path() -> str:
    return os.path.join(os.path.dirname(__file__), "theme_prefs.json")

def load_theme_prefs() -> dict:
    """Reads theme_prefs.json, returning empty dict if missing or invalid."""
    path = get_theme_prefs_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except Exception:
            pass
    return {}

def save_theme_prefs(updates: dict) -> dict:
    """Updates theme_prefs.json in place with new keys/values without wiping existing prefs."""
    prefs = load_theme_prefs()
    prefs.update(updates)
    path = get_theme_prefs_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(prefs, f, indent=2)
    except Exception:
        pass
    return prefs


def ensure_check_icon() -> str:
    """Guarantees the presence of a crisp antialiased white checkmark icon for checkboxes."""
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    os.makedirs(assets_dir, exist_ok=True)
    icon_path = os.path.join(assets_dir, "check_white.png")
    if not os.path.exists(icon_path):
        try:
            from PySide6.QtGui import QImage, QPainter, QPen, QColor
            from PySide6.QtCore import Qt
            img = QImage(16, 16, QImage.Format_ARGB32)
            img.fill(0)
            p = QPainter(img)
            p.setRenderHint(QPainter.RenderHint.Antialiasing)
            pen = QPen(QColor("#ffffff"), 2.2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
            p.setPen(pen)
            p.drawLine(3, 8, 6, 12)
            p.drawLine(6, 12, 13, 4)
            p.end()
            img.save(icon_path)
        except Exception:
            pass
    return icon_path.replace("\\", "/")


# ─── Manager ──────────────────────────────────────────────────────────────────

class ThemeManager:
    def __init__(self, initial: str = "Blue"):
        self._theme: Theme = ALL_THEMES.get(initial, BLUE)
        self.load_custom_theme_cache()
        if initial == "Custom":
            self._theme = ALL_THEMES["Custom"]

    def load_custom_theme_cache(self):
        """Loads custom theme preferences from theme_prefs.json if available."""
        data = load_theme_prefs()
        custom_data = data.get("custom_colors")
        if custom_data:
            self.set_custom_colors(
                accent=custom_data.get("accent", "#00adb5"),
                bg_primary=custom_data.get("bg_primary", "#0f1115"),
                bg_secondary=custom_data.get("bg_secondary", "#161920"),
                text_primary=custom_data.get("text_primary", "#c0c5ce"),
                persist=False
            )

    @property
    def current(self) -> Theme:
        return self._theme

    @property
    def names(self) -> list[str]:
        return list(ALL_THEMES.keys())

    def set_theme(self, name: str) -> bool:
        if name in ALL_THEMES:
            self._theme = ALL_THEMES[name]
            return True
        return False

    def save_theme(self, name: str) -> None:
        """Persists theme name without losing custom colors or other settings."""
        save_theme_prefs({"theme": name})

    def save_custom_colors(self, accent: str, bg_primary: str, bg_secondary: str, text_primary: str) -> None:
        """Updates and persists custom theme colors."""
        self.set_custom_colors(accent, bg_primary, bg_secondary, text_primary)
        save_theme_prefs({
            "theme": "Custom",
            "custom_colors": {
                "accent": accent,
                "bg_primary": bg_primary,
                "bg_secondary": bg_secondary,
                "text_primary": text_primary
            }
        })

    def set_custom_colors(self, accent: str, bg_primary: str, bg_secondary: str, text_primary: str, persist: bool = True) -> None:
        """Dynamically configures the Custom Theme with user-selected colors."""
        global CUSTOM
        CUSTOM = Theme(
            name="Custom",
            bg_primary=bg_primary,
            bg_secondary=bg_secondary,
            bg_tertiary=bg_secondary,
            bg_input=bg_secondary,
            border="rgba(255, 255, 255, 0.12)",
            border_hover=accent,
            text_primary=text_primary,
            text_secondary=text_primary,
            text_muted="rgba(255, 255, 255, 0.45)",
            text_bright="#ffffff",
            accent=accent,
            accent_hover=accent,
            accent_pressed=accent,
            scroll_bg=bg_primary,
            scroll_handle="rgba(255, 255, 255, 0.2)",
            scroll_hover=accent
        )
        ALL_THEMES["Custom"] = CUSTOM
        if hasattr(self, "_theme") and self._theme and self._theme.name == "Custom":
            self._theme = CUSTOM

        if persist:
            save_theme_prefs({
                "custom_colors": {
                    "accent": accent,
                    "bg_primary": bg_primary,
                    "bg_secondary": bg_secondary,
                    "text_primary": text_primary
                }
            })

    def stylesheet(self) -> str:
        t = self._theme
        is_light = t.name in ("Mocha", "Nordic")
        glass_bg = "rgba(255, 255, 255, 0.05)" if not is_light else "rgba(0, 0, 0, 0.04)"
        glass_hover = "rgba(255, 255, 255, 0.12)" if not is_light else "rgba(0, 0, 0, 0.08)"
        glass_border = "rgba(255, 255, 255, 0.10)" if not is_light else "rgba(0, 0, 0, 0.10)"
        card_text = t.text_bright if (not is_light and t.text_bright) else t.text_primary

        check_icon_path = ensure_check_icon()
        acc_q = QColor(t.accent) if hasattr(t, "accent") and t.accent else QColor("#00adb5")
        lum = acc_q.red() * 0.299 + acc_q.green() * 0.587 + acc_q.blue() * 0.114
        btn_checked_text = "#05080c" if lum > 165 else "#ffffff"
        btn_checked_border = "rgba(0, 0, 0, 0.4)" if lum > 165 else "rgba(255, 255, 255, 0.8)"

        return f"""
/* ── Global Architecture ─────────────────────────────────────────────────── */
QMainWindow {{ background-color: {t.bg_primary}; }}
QWidget     {{ background-color: {t.bg_primary}; color: {t.text_primary}; }}
QDialog     {{ background-color: {t.bg_secondary}; border: 1px solid {glass_border}; border-radius: 12px; }}

/* ── Glassmorphism Push Buttons ─────────────────────────────────────────── */
QPushButton {{
    background: {glass_bg};
    border: 1px solid {glass_border};
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 11px;
    font-weight: 600;
    color: {t.text_bright};
}}
QPushButton:hover {{
    background: {glass_hover};
    border-color: {t.accent};
    color: {t.accent};
}}
QPushButton:pressed {{
    background: {t.accent_pressed};
    color: #ffffff;
    border-color: {t.accent};
}}
QPushButton:disabled {{
    background: transparent;
    border-color: rgba(255, 255, 255, 0.04);
    color: {t.text_muted};
}}

/* ── Compact Ribbon & Tool Buttons (Fix symbol overlap & lit-up checked state) ─ */
QToolButton {{
    background: {glass_bg};
    border: 1px solid {glass_border};
    border-radius: 6px;
    padding: 2px 4px;
    font-size: 11px;
    font-weight: 600;
    color: {t.text_bright};
}}
QToolButton:hover {{
    background: {glass_hover};
    border-color: {t.accent};
    color: {t.accent};
}}
QToolButton:pressed, QToolButton:checked {{
    background: {t.accent};
    color: {btn_checked_text};
    border: 1.5px solid {btn_checked_border};
    font-weight: 800;
}}
QToolButton:disabled {{
    background: transparent;
    border-color: rgba(255, 255, 255, 0.04);
    color: {t.text_muted};
}}

/* ── Check Boxes (Lit Up when Checked) ──────────────────────────────────── */
QCheckBox {{
    spacing: 7px;
    color: {t.text_primary};
    font-size: 11px;
    font-weight: 500;
}}
QCheckBox:hover {{
    color: {t.text_bright};
}}
QCheckBox::indicator {{
    width: 15px;
    height: 15px;
    border-radius: 4px;
    border: 1.5px solid {glass_border};
    background: {glass_bg};
}}
QCheckBox::indicator:hover {{
    border-color: {t.accent};
    background: {glass_hover};
}}
QCheckBox::indicator:checked {{
    background-color: {t.accent};
    border: 1.5px solid {t.accent};
    image: url({check_icon_path});
}}
QCheckBox:checked {{
    color: {t.text_bright};
    font-weight: 600;
}}

/* ── Close Panel Button (fix X visibility) ───────────────────────────────── */
QPushButton#closePanelButton {{
    padding: 0px;
    margin: 0px;
    min-width: 26px;
    max-width: 26px;
    min-height: 26px;
    max-height: 26px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: bold;
    color: {t.text_bright};
    background: {glass_bg};
    border: 1px solid {glass_border};
    text-align: center;
}}
QPushButton#closePanelButton:hover {{
    background: rgba(220, 53, 69, 0.5);
    border-color: #ff4d4d;
    color: #ffffff;
}}

/* ── Draggable Splitter Handle (Between Workspace/Outline & AI Panel) ─────── */
QSplitter::handle:horizontal {{
    background: {t.border};
    width: 6px;
    border-left: 1px solid rgba(255, 255, 255, 0.04);
    border-right: 1px solid rgba(0, 0, 0, 0.08);
}}
QSplitter::handle:horizontal:hover {{
    background: {t.accent};
}}

/* ── Navigation Sidebar Controls ─────────────────────────────────────────── */
QPushButton#toggleNavButton {{
    background: {glass_bg};
    border: 1px solid {glass_border};
    border-radius: 8px;
    padding: 4px 12px;
    color: {t.text_primary};
    font-size: 12px;
    font-weight: 600;
    margin-top: 2px;
    margin-bottom: 0px;
}}
QPushButton#toggleNavButton:hover {{
    background: {glass_hover};
    border-color: {t.accent};
    color: {t.text_bright};
    margin-top: 0px;
    margin-bottom: 2px;
}}
QPushButton#collapseNavButton {{
    background: {glass_bg};
    border: 1px solid {glass_border};
    border-radius: 6px;
    padding: 0px;
    color: {t.text_secondary};
    font-size: 11px;
}}
QPushButton#collapseNavButton:hover {{
    background: {glass_hover};
    border-color: {t.accent};
    color: {t.text_bright};
}}

/* ── Home Page Output Registry & Artifact Cards ──────────────────────────── */
QFrame#documentArea {{
    background: {glass_bg};
    border: 1px solid {glass_border};
    border-top: 3px solid {t.accent};
    border-radius: 12px;
}}
QFrame#documentArea:hover {{
    background: {glass_hover};
    border: 1.5px solid {t.accent};
    border-top: 3.5px solid {t.accent};
}}
QLabel#docAreaHeader {{
    color: {card_text};
    font-weight: 800;
    font-size: 13px;
}}
QLabel#docDisplay {{
    background: rgba(0, 0, 0, 0.15);
    border: 1px dashed {glass_border};
    border-radius: 8px;
    color: {t.text_secondary};
}}
QLabel#docStatus {{
    color: {t.text_secondary};
}}

QPushButton#artifactButton {{
    background: {glass_bg};
    border: 1px solid {glass_border};
    border-top: 2.5px solid {t.accent};
    border-radius: 12px;
    padding: 6px;
}}
QPushButton#artifactButton:hover {{
    background: {glass_hover};
    border: 1.5px solid {t.accent};
    border-top: 3px solid {t.accent};
}}
QLabel#artifactName {{
    color: {card_text};
    font-weight: 700;
    font-size: 12px;
}}
QLabel#artifactThumbnail {{
    background: rgba(0, 0, 0, 0.15);
    border: 1px dashed {t.accent};
    border-radius: 8px;
    color: {t.text_secondary};
}}

/* ── Primary Action / Model Button ───────────────────────────────────────── */
QPushButton#modelButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {t.accent}, stop:1 {t.accent_pressed});
    color: #ffffff;
    font-weight: 700;
    font-size: 11px;
    border: 1px solid {t.accent_hover};
    border-radius: 8px;
    padding: 6px 14px;
    margin-top: 2px;
    margin-bottom: 0px;
}}
QPushButton#modelButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {t.accent_hover}, stop:1 {t.accent});
    border-color: {t.text_bright};
    margin-top: 0px;
    margin-bottom: 2px;
}}
QPushButton#modelButton:pressed {{
    background: {t.accent_pressed};
    margin-top: 3px;
    margin-bottom: -1px;
}}
QPushButton#modelButton:disabled {{
    background: rgba(120, 120, 120, 0.25);
    color: {t.text_muted};
    border-color: {glass_border};
}}

/* ── Dynamic Accent Action Buttons & Pills (Cohesive Theme Glow) ─────────── */
QPushButton#modelModeToggle, QPushButton#btnModelInsert, QPushButton#btnModelReplace,
QPushButton#btnPlayAudio, QPushButton#btnAddPrompt, QPushButton#btnCodeAction,
QPushButton#btnFindReplaceAction, QPushButton#btnCustomPreset, QPushButton#btnApplyCustom {{
    background: {glass_bg};
    border: 1px solid {t.accent};
    color: {t.accent};
    border-radius: 6px;
    font-weight: 700;
    font-size: 11px;
    padding: 6px 12px;
    margin-top: 2px;
    margin-bottom: 0px;
}}
QPushButton#modelModeToggle:hover, QPushButton#btnModelInsert:hover, QPushButton#btnModelReplace:hover,
QPushButton#btnPlayAudio:hover, QPushButton#btnAddPrompt:hover, QPushButton#btnCodeAction:hover,
QPushButton#btnFindReplaceAction:hover, QPushButton#btnCustomPreset:hover, QPushButton#btnApplyCustom:hover {{
    background: {t.accent};
    color: #ffffff;
    margin-top: 0px;
    margin-bottom: 2px;
}}
QPushButton#modelModeToggle:pressed, QPushButton#btnModelInsert:pressed, QPushButton#btnModelReplace:pressed,
QPushButton#btnPlayAudio:pressed, QPushButton#btnAddPrompt:pressed, QPushButton#btnCodeAction:pressed,
QPushButton#btnFindReplaceAction:pressed, QPushButton#btnCustomPreset:pressed, QPushButton#btnApplyCustom:pressed {{
    margin-top: 3px;
    margin-bottom: -1px;
}}
QPushButton#modelModeToggle:checked {{
    background: {t.accent};
    color: #ffffff;
    border: 1px solid {t.accent};
}}
QPushButton#modelPill {{
    background: {glass_bg};
    border: 1px solid {t.accent};
    border-radius: 12px;
    color: {t.accent};
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    margin-top: 1px;
    margin-bottom: 0px;
}}
QPushButton#modelPill:hover {{
    background: {t.accent};
    color: #ffffff;
    margin-top: 0px;
    margin-bottom: 1px;
}}
    background: {t.accent};
    color: #ffffff;
}}

/* ── Accent Labels & Headers ─────────────────────────────────────────────── */
QLabel#accentTitle, QLabel#modelPanelTitle, QLabel#systemStatus, QLabel#logoText,
QLabel#lblFilmstripStats, QLabel#codeFeedback, QLabel#promptTag, QLabel#zoomValLabel,
QLabel#lblCustomStatusActive, QLabel#docAreaHeader, QLabel#artifactName, QLabel#docStatus {{
    color: {t.accent};
}}
QLabel#statusDot {{
    background-color: {t.accent};
    border-radius: 4px;
}}

/* ── Interactive Sliders (Volume & Controls) ─────────────────────────────── */
QSlider::groove:horizontal {{
    height: 4px;
    background: {glass_border};
    border-radius: 2px;
}}
QSlider::sub-page:horizontal {{
    background: {t.accent};
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: #ffffff;
    border: 1.5px solid {t.accent};
    width: 12px;
    margin-top: -4px;
    margin-bottom: -4px;
    border-radius: 6px;
}}

/* ── Filmstrip Page Thumbnail Card ───────────────────────────────────────── */
QFrame#pageThumbnailCard[active="true"] {{
    background: {glass_hover};
    border: 1.5px solid {t.accent};
    border-radius: 6px;
}}
QFrame#pageThumbnailCard[active="true"] QLabel {{
    color: {t.accent};
    font-weight: 700;
}}

/* ── Glass Containers & Section Frames ───────────────────────────────────── */
QFrame#navArea, QFrame#logoArea, QFrame#metricsFrame, QFrame#bottomBarFrame {{
    background: {t.bg_secondary};
    border: 1px solid {glass_border};
    border-radius: 10px;
}}
QFrame#sectionFrame, QGroupBox {{
    background: {glass_bg};
    border: 1px solid {glass_border};
    border-radius: 10px;
    margin-top: 10px;
    padding: 12px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: {t.accent};
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 0.5px;
}}

/* ── Navigation Buttons ──────────────────────────────────────────────────── */
QPushButton#navButton {{
    background: transparent;
    color: {t.text_secondary};
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 8px 12px;
    text-align: left;
    font-size: 11px;
    font-weight: 600;
}}
QPushButton#navButton:hover {{
    background: {glass_hover};
    color: {t.text_bright};
    border-color: {glass_border};
}}
QPushButton#navButtonActive {{
    background: {glass_hover};
    color: {t.accent};
    font-weight: 700;
    border: 1px solid {t.accent};
    border-radius: 8px;
    padding: 8px 12px;
    text-align: left;
    font-size: 11px;
}}

/* ── Input Controls & Combos ─────────────────────────────────────────────── */
QLineEdit, QTextEdit {{
    background: {t.bg_input};
    color: {t.text_bright};
    border: 1px solid {glass_border};
    border-radius: 8px;
    padding: 8px 10px;
}}
QLineEdit:focus, QTextEdit:focus {{
    border: 1px solid {t.accent};
}}

QComboBox {{
    background: {t.bg_input};
    color: {t.text_bright};
    border: 1px solid {glass_border};
    border-radius: 8px;
    padding: 6px 12px;
    min-height: 22px;
}}
QComboBox:hover {{
    border-color: {t.accent};
}}
QComboBox::drop-down {{
    border: none;
    width: 20px;
}}
QComboBox QAbstractItemView {{
    background: {t.bg_secondary};
    color: {t.text_bright};
    border: 1px solid {glass_border};
    border-radius: 8px;
    selection-background-color: {t.accent};
    selection-color: #ffffff;
    padding: 4px;
}}

/* ── Ribbon Toolbar Specialized Compact Controls ────────────────────────── */
QFrame#ribbonGroup QComboBox,
QFrame#ribbonGroup QFontComboBox,
QFrame#ribbonGroup QSpinBox {{
    background: {t.bg_input};
    color: {t.text_bright};
    border: 1px solid {glass_border};
    border-radius: 4px;
    padding: 1px 6px;
    min-height: 18px;
    max-height: 22px;
    font-size: 11px;
}}
QFrame#ribbonGroup QComboBox::drop-down,
QFrame#ribbonGroup QFontComboBox::drop-down {{
    border: none;
    width: 14px;
}}
QFrame#ribbonGroup QToolButton {{
    padding: 2px;
    min-height: 20px;
    max-height: 24px;
    border-radius: 4px;
}}
QFrame#ribbonGroup QToolButton:checked {{
    background: {t.accent};
    color: {btn_checked_text};
    border: 1.5px solid {btn_checked_border};
    font-weight: 800;
}}
QFrame#ribbonGroup QLabel {{
    color: {t.text_secondary};
}}

/* ── Tab Widgets ─────────────────────────────────────────────────────────── */
QTabWidget::pane {{
    border: 1px solid {glass_border};
    border-radius: 10px;
    background: {t.bg_secondary};
}}
QTabBar::tab {{
    background: {glass_bg};
    color: {t.text_secondary};
    border: 1px solid {glass_border};
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 8px 18px;
    margin-right: 3px;
    font-weight: 600;
    font-size: 11px;
}}
QTabBar::tab:selected {{
    background: {t.accent};
    color: #ffffff;
    font-weight: 700;
    border-color: {t.accent};
}}
QTabBar::tab:hover:!selected {{
    background: {glass_hover};
    color: {t.text_bright};
}}

/* ── Dedicated Code Workspace Preservation ───────────────────────────────── */
QPlainTextEdit#codeEditorArea {{
    background-color: #1e1f24;
    color: #f8f8f2;
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 8px;
    selection-background-color: rgba(0, 173, 181, 0.4);
}}

/* ── Scrollbars ──────────────────────────────────────────────────────────── */
QScrollBar:vertical {{
    background: {t.scroll_bg};
    width: 8px;
    border-radius: 4px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {t.scroll_handle};
    min-height: 24px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical:hover {{
    background: {t.scroll_hover};
}}
QScrollBar:horizontal {{
    background: {t.scroll_bg};
    height: 8px;
    border-radius: 4px;
    margin: 0;
}}
QScrollBar::handle:horizontal {{
    background: {t.scroll_handle};
    min-width: 24px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {t.scroll_hover};
}}
QScrollBar::add-line, QScrollBar::sub-line {{
    width: 0;
    height: 0;
}}
"""
