"""
page_settings.py — Alpha Tech Suite Settings Page
Theme switcher (Blue / Dark / Mocha) + general preferences.
Emits theme_changed(str) when the user selects a new theme.
"""
from PySide6.QtWidgets import (
    QScrollArea, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QRadioButton, QButtonGroup,
    QCheckBox, QLineEdit, QSizePolicy, QPushButton,
    QColorDialog, QGridLayout
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
import json
import os

from themes import ALL_THEMES, Theme, CUSTOM

# Colour swatches shown next to each theme radio button
_SWATCH_STYLE = "border-radius: 6px; border: 1px solid rgba(0,0,0,0.2);"


DEFAULT_CODE_PROMPTS = [
    ("⚡ Refactor Architecture", "Refactor the selected code into clean, modular, decoupled functions with single responsibility."),
    ("🧪 Generate Unit Tests", "Write comprehensive unit tests with edge case coverage and mocking for external dependencies."),
    ("🛡️ Security & Bug Audit", "Analyze this code for security vulnerabilities, race conditions, memory leaks, or unhandled exceptions."),
    ("📝 Add Type Hints & Docs", "Add complete PEP 484 type annotations and detailed docstrings explaining arguments and return types."),
    ("🚀 Optimize Algorithm (Big-O)", "Analyze time and space complexity and provide an optimized, high-performance refactored implementation.")
]


class SettingsPage(QScrollArea):
    """Settings page with live theme switching, code prompts, and general preferences."""

    theme_changed = Signal(str)            # emitted with the theme name
    code_prompts_changed = Signal(list)    # emitted with list of (label, prompt) tuples

    def __init__(self, current_theme_name: str = "Blue", parent=None):
        super().__init__(parent)
        self.setObjectName("pageContainer")
        self.setWidgetResizable(True)
        self.setFrameShape(QScrollArea.Shape.NoFrame)

        self.settings_file = os.path.join(os.path.dirname(__file__), "settings_prefs.json")
        self._saved_settings = self._load_saved_settings()

        self._radio_group  = QButtonGroup(self)
        self._radio_buttons: dict[str, QRadioButton] = {}
        self.server_fields: dict[str, QLineEdit] = {}
        self.pref_checkboxes: dict[str, QCheckBox] = {}
        self.code_prompts = [list(x) for x in self._saved_settings.get("code_prompts", DEFAULT_CODE_PROMPTS)]

        container = QWidget()
        container.setObjectName("pageContainer")
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)

        layout.addWidget(self._page_header(
            "Settings",
            "Configure the Alpha Tech Document Suite to your preferences.",
        ))
        layout.addWidget(self._divider())

        # Theme section
        layout.addWidget(self._section_title("APPEARANCE"))
        layout.addWidget(self._build_theme_section(current_theme_name))
        layout.addWidget(self._divider())

        # AI connection section
        layout.addWidget(self._section_title("AI & MODEL SERVER"))
        layout.addWidget(self._build_ai_server_section())
        layout.addWidget(self._divider())

        # Code Prompts section
        layout.addWidget(self._section_title("CODE EDITOR AI PROMPTS & DIRECTIVES"))
        layout.addWidget(self._build_code_prompts_section())
        layout.addWidget(self._divider())

        # General preferences
        layout.addWidget(self._section_title("GENERAL"))
        layout.addWidget(self._build_general_section())

        layout.addStretch()
        container.setLayout(layout)
        self.setWidget(container)

    # ── Theme section ─────────────────────────────────────────────────────────

    def _build_theme_section(self, current_name: str) -> QFrame:
        card = self._card()
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        desc = QLabel("Choose a colour theme for the interface.")
        desc.setObjectName("infoCardBody")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        for name, theme in ALL_THEMES.items():
            row = QHBoxLayout()
            row.setSpacing(10)

            radio = QRadioButton(name)
            if name == current_name:
                radio.setChecked(True)
            radio.toggled.connect(lambda checked, n=name: self._on_radio(checked, n))
            self._radio_group.addButton(radio)
            self._radio_buttons[name] = radio

            # Mini colour swatch: bg + accent
            swatch_bg = QLabel()
            swatch_bg.setFixedSize(20, 20)
            swatch_bg.setStyleSheet(
                f"background-color: {theme.bg_primary}; {_SWATCH_STYLE}"
            )
            swatch_ac = QLabel()
            swatch_ac.setFixedSize(20, 20)
            swatch_ac.setStyleSheet(
                f"background-color: {theme.accent}; {_SWATCH_STYLE}"
            )

            row.addWidget(radio)
            row.addStretch()
            row.addWidget(swatch_bg)
            row.addWidget(swatch_ac)
            layout.addLayout(row)

        # ── Custom Theme Palette Studio ───────────────────────────────────────
        self.custom_studio = QFrame()
        self.custom_studio.setObjectName("customStudio")
        self.custom_studio.setStyleSheet("""
            QFrame#customStudio {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.10);
                border-radius: 10px;
                padding: 12px;
                margin-top: 10px;
            }
            QFrame#customStudio:disabled {
                background: rgba(0, 0, 0, 0.04);
                border: 1px dashed rgba(255, 255, 255, 0.05);
            }
        """)
        studio_layout = QVBoxLayout(self.custom_studio)
        studio_layout.setSpacing(10)

        lbl_custom_title = QLabel("🎨 Custom Theme Palette Studio")
        lbl_custom_title.setStyleSheet("font-size: 13px; font-weight: 700;")
        studio_layout.addWidget(lbl_custom_title)

        is_custom_init = (current_name == "Custom")
        self.lbl_custom_status = QLabel(
            "● Active (Editing Custom Theme)" if is_custom_init 
            else "🔒 Inactive — Select 'Custom' theme above to enable palette editor"
        )
        self.lbl_custom_status.setStyleSheet(
            "color: #00adb5; font-size: 11px; font-weight: 600;" if is_custom_init 
            else "color: #8e96a3; font-size: 11px;"
        )
        studio_layout.addWidget(self.lbl_custom_status)

        lbl_custom_sub = QLabel("Fine-tune your personal palette or choose a starter preset:")
        lbl_custom_sub.setStyleSheet("font-size: 11px; color: #8e96a3;")
        studio_layout.addWidget(lbl_custom_sub)

        # Input fields grid
        fields_grid = QGridLayout()
        fields_grid.setSpacing(8)

        from themes import load_theme_prefs, save_theme_prefs
        saved_prefs = load_theme_prefs()
        custom_saved = saved_prefs.get("custom_colors", {})
        init_acc = custom_saved.get("accent", CUSTOM.accent)
        init_bg1 = custom_saved.get("bg_primary", CUSTOM.bg_primary)
        init_bg2 = custom_saved.get("bg_secondary", CUSTOM.bg_secondary)
        init_txt = custom_saved.get("text_primary", CUSTOM.text_primary)

        self.custom_inputs = {}
        color_defaults = [
            ("Accent Glow", "accent", init_acc),
            ("Primary Background", "bg_primary", init_bg1),
            ("Panel Surface", "bg_secondary", init_bg2),
            ("Text Color", "text_primary", init_txt),
        ]

        for idx, (label_text, key, default_val) in enumerate(color_defaults):
            lbl = QLabel(f"{label_text}:")
            lbl.setStyleSheet("font-size: 11px;")
            inp = QLineEdit(default_val)
            inp.setMaximumWidth(110)
            inp.setStyleSheet("padding: 5px 8px; font-family: monospace; font-size: 11px; border-radius: 6px;")
            self.custom_inputs[key] = inp

            chip = QPushButton()
            chip.setFixedSize(22, 22)
            chip.setStyleSheet(f"background-color: {default_val}; border-radius: 4px; border: 1px solid rgba(255,255,255,0.3);")

            def make_picker(k=key, i=inp, c=chip):
                def _pick():
                    chosen = QColorDialog.getColor(QColor(i.text()), self, "Select Color")
                    if chosen.isValid():
                        hex_c = chosen.name()
                        i.setText(hex_c)
                        c.setStyleSheet(f"background-color: {hex_c}; border-radius: 4px; border: 1px solid rgba(255,255,255,0.3);")
                return _pick

            chip.clicked.connect(make_picker(key, inp, chip))
            inp.textChanged.connect(lambda t, c=chip: c.setStyleSheet(f"background-color: {t}; border-radius: 4px; border: 1px solid rgba(255,255,255,0.3);") if QColor(t).isValid() else None)

            fields_grid.addWidget(lbl, idx // 2, (idx % 2) * 3)
            fields_grid.addWidget(inp, idx // 2, (idx % 2) * 3 + 1)
            fields_grid.addWidget(chip, idx // 2, (idx % 2) * 3 + 2)

        studio_layout.addLayout(fields_grid)

        # Quick preset pills
        presets_row = QHBoxLayout()
        presets_row.setSpacing(6)
        presets = [
            ("🟣 Cyber", "#bd93f9", "#0d0c1d", "#15132c"),
            ("🟢 Mint", "#00f5a0", "#090f0c", "#0e1713"),
            ("🔴 Ruby", "#ff4d6d", "#140b0f", "#1c1117"),
            ("🔵 Cyan", "#00adb5", "#0e1117", "#151922"),
            ("🟡 Gold", "#ffb703", "#14110d", "#1c1813"),
        ]
        for p_name, p_acc, p_bg1, p_bg2 in presets:
            btn_p = QPushButton(p_name)
            btn_p.setStyleSheet("font-size: 10px; padding: 4px 8px; border-radius: 6px;")
            def _make_preset_handler(a=p_acc, b1=p_bg1, b2=p_bg2):
                def _handle_preset():
                    self.custom_inputs["accent"].setText(a)
                    self.custom_inputs["bg_primary"].setText(b1)
                    self.custom_inputs["bg_secondary"].setText(b2)
                    self._apply_custom_theme()
                return _handle_preset
            btn_p.clicked.connect(_make_preset_handler(p_acc, p_bg1, p_bg2))
            presets_row.addWidget(btn_p)

        studio_layout.addLayout(presets_row)

        btn_apply_custom = QPushButton("✨ Apply Custom Palette")
        btn_apply_custom.setObjectName("btnApplyCustom")
        btn_apply_custom.clicked.connect(self._apply_custom_theme)
        studio_layout.addWidget(btn_apply_custom)

        # Set initial enabled state (greyed out unless Custom is chosen)
        self.custom_studio.setEnabled(is_custom_init)

        layout.addWidget(self.custom_studio)

        card.setLayout(layout)
        return card

    def _on_radio(self, checked: bool, name: str) -> None:
        if checked:
            is_custom = (name == "Custom")
            if hasattr(self, "custom_studio"):
                self.custom_studio.setEnabled(is_custom)
            if hasattr(self, "lbl_custom_status"):
                acc = getattr(self, "_theme_accent", "#00adb5")
                if is_custom:
                    self.lbl_custom_status.setText("● Active (Editing Custom Theme)")
                    self.lbl_custom_status.setStyleSheet(f"color: {acc}; font-size: 11px; font-weight: 600;")
                else:
                    self.lbl_custom_status.setText("🔒 Inactive — Select 'Custom' theme above to enable palette editor")
                    self.lbl_custom_status.setStyleSheet("color: #8e96a3; font-size: 11px;")
            self.theme_changed.emit(name)

    def _apply_custom_theme(self) -> None:
        acc = self.custom_inputs.get("accent", QLineEdit()).text().strip() or "#00adb5"
        bg1 = self.custom_inputs.get("bg_primary", QLineEdit()).text().strip() or "#0f1115"
        bg2 = self.custom_inputs.get("bg_secondary", QLineEdit()).text().strip() or "#161920"
        txt = self.custom_inputs.get("text_primary", QLineEdit()).text().strip() or "#ffffff"

        from themes import CUSTOM, ALL_THEMES, save_theme_prefs
        CUSTOM.accent = acc
        CUSTOM.accent_hover = acc
        CUSTOM.accent_pressed = acc
        CUSTOM.bg_primary = bg1
        CUSTOM.bg_secondary = bg2
        CUSTOM.bg_tertiary = bg2
        CUSTOM.bg_input = bg2
        CUSTOM.border = "rgba(255, 255, 255, 0.12)"
        CUSTOM.border_hover = acc
        CUSTOM.text_primary = txt
        CUSTOM.text_secondary = txt
        CUSTOM.text_muted = "rgba(255, 255, 255, 0.45)"
        CUSTOM.text_bright = "#ffffff"
        CUSTOM.scroll_bg = bg1
        CUSTOM.scroll_handle = "rgba(255, 255, 255, 0.2)"
        CUSTOM.scroll_hover = acc
        ALL_THEMES["Custom"] = CUSTOM

        if hasattr(self, "theme_mgr") and self.theme_mgr:
            self.theme_mgr.set_custom_colors(acc, bg1, bg2, txt)

        # Merge-save custom colors into theme_prefs.json preserving code editor preferences
        save_theme_prefs({
            "theme": "Custom",
            "custom_colors": {
                "accent": acc,
                "bg_primary": bg1,
                "bg_secondary": bg2,
                "text_primary": txt
            }
        })

        if "Custom" in self._radio_buttons:
            self._radio_buttons["Custom"].setChecked(True)
        self.theme_changed.emit("Custom")

    def _load_saved_settings(self) -> dict:
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_settings(self) -> None:
        data = {
            "server_url": self.server_fields.get("Server URL", QLineEdit()).text(),
            "api_key": self.server_fields.get("API Key", QLineEdit()).text(),
            "default_model": self.server_fields.get("Default Model", QLineEdit()).text(),
            "general_prefs": {
                name: cb.isChecked() for name, cb in self.pref_checkboxes.items()
            }
        }
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[Settings] Failed to save settings: {e}")

    # ── AI Server section ─────────────────────────────────────────────────────

    def _build_ai_server_section(self) -> QFrame:
        card = self._card()
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 20)
        layout.setSpacing(12)

        key_map = {
            "Server URL": "server_url",
            "API Key": "api_key",
            "Default Model": "default_model",
        }

        for label_text, placeholder in [
            ("Server URL",   "http://localhost:11434"),
            ("API Key",      "sk-… (Optional for local models)"),
            ("Default Model","llama3.2"),
        ]:
            lbl = QLabel(label_text)
            lbl.setObjectName("infoCardBody")
            field = QLineEdit()
            field.setPlaceholderText(placeholder)
            
            # Mask API key to prevent cleartext exposure
            if label_text == "API Key":
                field.setEchoMode(QLineEdit.EchoMode.Password)
                
            saved_val = self._saved_settings.get(key_map.get(label_text, ""))
            if saved_val:
                field.setText(saved_val)

            field.textChanged.connect(lambda _: self._save_settings())
            self.server_fields[label_text] = field

            layout.addWidget(lbl)
            layout.addWidget(field)

        card.setLayout(layout)
        return card

    # ── Code Prompts section ──────────────────────────────────────────────────

    def _build_code_prompts_section(self) -> QFrame:
        card = self._card()
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        desc = QLabel("Configure custom AI directives and quick-action prompt pills used when Code Mode is active in the AI Model Copilot.")
        desc.setObjectName("infoCardBody")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        self._prompts_container = QVBoxLayout()
        self._prompts_container.setSpacing(6)
        self._render_code_prompts_list()
        layout.addLayout(self._prompts_container)

        # Add New Prompt inputs
        add_frame = QFrame()
        add_frame.setStyleSheet("""
            QFrame {
                background: rgba(0, 0, 0, 0.2);
                border: 1px dashed rgba(255, 255, 255, 0.15);
                border-radius: 8px;
                padding: 10px;
            }
        """)
        add_layout = QVBoxLayout(add_frame)
        add_layout.setContentsMargins(8, 8, 8, 8)
        add_layout.setSpacing(8)

        lbl_add = QLabel("➕ Add New Code Model Directive")
        lbl_add.setObjectName("accentTitle")
        lbl_add.setStyleSheet("font-size: 12px; font-weight: bold;")
        add_layout.addWidget(lbl_add)

        self.input_prompt_title = QLineEdit()
        self.input_prompt_title.setPlaceholderText("Pill Label (e.g. 🔄 Convert to Async, 🔍 Profile Memory)...")
        add_layout.addWidget(self.input_prompt_title)

        self.input_prompt_text = QLineEdit()
        self.input_prompt_text.setPlaceholderText("AI Instruction Prompt (e.g. Analyze and refactor this code to use asyncio...)...")
        add_layout.addWidget(self.input_prompt_text)

        btn_add = QPushButton("✨ Add Code Directive to Model Panel")
        btn_add.setObjectName("btnAddPrompt")
        btn_add.clicked.connect(self._on_add_code_prompt)
        add_layout.addWidget(btn_add)

        layout.addWidget(add_frame)
        card.setLayout(layout)
        return card

    def _render_code_prompts_list(self):
        while self._prompts_container.count():
            item = self._prompts_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub = item.layout().takeAt(0)
                    if sub.widget():
                        sub.widget().deleteLater()

        acc = getattr(self, "_theme_accent", "#00adb5")
        for idx, item in enumerate(self.code_prompts):
            label = item[0] if len(item) > 0 else ""
            prompt_text = item[1] if len(item) > 1 else ""

            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(8)

            lbl_tag = QLabel(f"<b>{label}</b>")
            lbl_tag.setObjectName("promptTag")
            lbl_tag.setStyleSheet(f"color: {acc}; font-size: 11px; min-width: 140px;")
            row.addWidget(lbl_tag)

            lbl_txt = QLabel(prompt_text)
            lbl_txt.setStyleSheet("color: #a0a6b2; font-size: 11px;")
            lbl_txt.setWordWrap(True)
            row.addWidget(lbl_txt, 1)

            btn_del = QPushButton("✕")
            btn_del.setFixedSize(22, 22)
            btn_del.setToolTip("Remove this directive")
            btn_del.setStyleSheet("""
                QPushButton {
                    background: rgba(220, 53, 69, 0.15);
                    color: #ff6b6b;
                    border: 1px solid rgba(220, 53, 69, 0.3);
                    border-radius: 4px;
                    font-size: 10px;
                    font-weight: bold;
                    padding: 0px;
                }
                QPushButton:hover {
                    background: #dc3545;
                    color: #ffffff;
                }
            """)
            btn_del.clicked.connect(lambda _, i=idx: self._on_delete_code_prompt(i))
            row.addWidget(btn_del)

            wrapper = QFrame()
            wrapper.setStyleSheet("""
                QFrame {
                    background: rgba(255, 255, 255, 0.03);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 6px;
                    padding: 4px 8px;
                }
            """)
            wrapper.setLayout(row)
            self._prompts_container.addWidget(wrapper)

    def _on_add_code_prompt(self):
        title = self.input_prompt_title.text().strip()
        prompt = self.input_prompt_text.text().strip()
        if not title or not prompt:
            return

        self.code_prompts.append([title, prompt])
        self.input_prompt_title.clear()
        self.input_prompt_text.clear()
        self._saved_settings["code_prompts"] = self.code_prompts
        self._save_settings()
        self._render_code_prompts_list()
        self.code_prompts_changed.emit(self.code_prompts)

    def _on_delete_code_prompt(self, idx: int):
        if 0 <= idx < len(self.code_prompts):
            self.code_prompts.pop(idx)
            self._saved_settings["code_prompts"] = self.code_prompts
            self._save_settings()
            self._render_code_prompts_list()
            self.code_prompts_changed.emit(self.code_prompts)

    def get_code_prompts(self) -> list:
        return self.code_prompts

    # ── General section ───────────────────────────────────────────────────────

    def _build_general_section(self) -> QFrame:
        card = self._card()
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        saved_general = self._saved_settings.get("general_prefs", {})
        prefs = [
            ("Auto-save output documents",        True),
            ("Show tool-call trace in side panel", True),
            ("Enable streaming responses",         True),
            ("Send anonymous usage metrics",       False),
        ]
        for text, default in prefs:
            cb = QCheckBox(text)
            initial_val = saved_general.get(text, default)
            cb.setChecked(initial_val)
            cb.toggled.connect(lambda _: self._save_settings())
            self.pref_checkboxes[text] = cb
            layout.addWidget(cb)

        card.setLayout(layout)
        return card

    # ── Helpers ───────────────────────────────────────────────────────────────

    def set_active_theme(self, name: str) -> None:
        """Update the radio selection from outside (e.g. header dropdown)."""
        if name in self._radio_buttons:
            self._radio_buttons[name].setChecked(True)

    def set_theme_accent(self, accent_hex: str) -> None:
        """Dynamically updates active custom status color and directive pills."""
        self._theme_accent = accent_hex
        if hasattr(self, "lbl_custom_status") and hasattr(self, "custom_studio") and self.custom_studio.isEnabled():
            self.lbl_custom_status.setStyleSheet(f"color: {accent_hex}; font-size: 11px; font-weight: 600;")
        if hasattr(self, "_prompts_container"):
            self._render_code_prompts_list()

    @staticmethod
    def _page_header(title: str, subtitle: str) -> QWidget:
        w = QWidget()
        l = QVBoxLayout()
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(4)
        t = QLabel(title);   t.setObjectName("pageTitle")
        s = QLabel(subtitle); s.setObjectName("pageSubtitle"); s.setWordWrap(True)
        l.addWidget(t); l.addWidget(s)
        w.setLayout(l)
        return w

    @staticmethod
    def _section_title(text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("sectionTitle")
        return lbl

    @staticmethod
    def _card() -> QFrame:
        f = QFrame()
        f.setObjectName("infoCard")
        return f

    @staticmethod
    def _divider() -> QFrame:
        line = QFrame()
        line.setObjectName("divider")
        line.setFixedHeight(1)
        line.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        return line