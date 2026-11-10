"""
Alpha Docs Tool - Help & Keyboard Shortcuts Documentation Page
Provides interactive instructions, workflow guides, and a searchable keyboard shortcuts reference.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTabWidget, QScrollArea, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon


class ShortcutItem:
    def __init__(self, category: str, keys: str, description: str):
        self.category = category
        self.keys = keys
        self.description = description


SHORTCUTS_DATA = [
    # Navigation & Interface
    ShortcutItem("Navigation", "Ctrl + \\", "Toggle Left Navigation Sidebar collapse/expand"),
    ShortcutItem("Navigation", "F1", "Open System Help & Documentation"),

    # Document & Editor Zoom
    ShortcutItem("Zoom", "Ctrl + + / Ctrl + =", "Zoom in document canvas and active code editor"),
    ShortcutItem("Zoom", "Ctrl + -", "Zoom out document canvas and active code editor"),
    ShortcutItem("Zoom", "Ctrl + 0", "Reset zoom scale to 100% / default font size"),
    ShortcutItem("Zoom", "Ctrl + MouseWheel", "Smoothly zoom canvas between 50% and 300%"),

    # Multi-Tab Code Workspace
    ShortcutItem("Code Tabs", "Ctrl + T", "Open new code editor tab buffer"),
    ShortcutItem("Code Tabs", "Ctrl + W", "Close active code editor tab"),

    # Search & Replace
    ShortcutItem("Search", "Ctrl + F", "Open Find & Replace bar (Search mode)"),
    ShortcutItem("Search", "Ctrl + H", "Open Find & Replace bar (Replace mode)"),
    ShortcutItem("Search", "F3 / Enter", "Find next occurrence"),
    ShortcutItem("Search", "Shift + F3", "Find previous occurrence"),
    ShortcutItem("Search", "Esc", "Dismiss Find & Replace bar"),

    # Export & Files
    ShortcutItem("Files", "Ctrl + E", "Open Document Export Center (Markdown, HTML, PDF)"),
    ShortcutItem("Files", "Ctrl + N", "Create new document workspace"),
    ShortcutItem("Files", "Ctrl + O", "Import existing file (*.txt, *.md, *.docx)"),
    ShortcutItem("Files", "Ctrl + S", "Save snapshot to Version History"),

    # Selection & Navigation
    ShortcutItem("Selection", "Ctrl + A", "Select all text in the document"),
    ShortcutItem("Selection", "Shift + Mouse Click", "Extend text selection from active cursor to click position"),
    ShortcutItem("Selection", "Double-Click", "Select word under mouse cursor"),
    ShortcutItem("Selection", "Right-Click", "Open context menu (Cut, Copy, Paste, Select All)"),
    ShortcutItem("Selection", "Click Outside Selection", "Deselect active text and place cursor"),

    # Clipboard & History
    ShortcutItem("Clipboard", "Ctrl + C", "Copy selected text to clipboard"),
    ShortcutItem("Clipboard", "Ctrl + X", "Cut selected text to clipboard"),
    ShortcutItem("Clipboard", "Ctrl + V", "Paste clipboard text into document"),
    ShortcutItem("History", "Ctrl + Z", "Undo last editing operation"),
    ShortcutItem("History", "Ctrl + Y", "Redo last undone operation"),

    # Text Formatting
    ShortcutItem("Formatting", "Ctrl + B", "Toggle Bold text formatting"),
    ShortcutItem("Formatting", "Ctrl + I", "Toggle Italic text formatting"),
    ShortcutItem("Formatting", "Ctrl + U", "Toggle Underline text formatting"),
    ShortcutItem("Formatting", "Tab", "Insert indent tab spacing"),
    ShortcutItem("Formatting", "Shift + Tab", "Outdent paragraph spacing"),
]


class HelpPage(QWidget):
    """Full-screen interactive help, instructions, and keyboard shortcuts guide."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("pageHelp")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Header Title Banner
        header_frame = QFrame()
        header_frame.setFrameShape(QFrame.Shape.StyledPanel)
        header_frame.setStyleSheet("border-radius: 8px; padding: 12px;")
        header_layout = QHBoxLayout(header_frame)
        
        title_label = QLabel("❓ System Documentation & Keyboard Shortcuts")
        title_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        main_layout.addWidget(header_frame)

        # Tab Widget: Instructions vs Keyboard Shortcuts
        self.tabs = QTabWidget()

        self.tabs.addTab(self._build_instructions_tab(), "📖 Basic Instructions & User Guide")
        self.tabs.addTab(self._build_shortcuts_tab(), "⌨️ Keyboard Shortcuts Reference")

        main_layout.addWidget(self.tabs, 1)

    # ── TAB 1: USER GUIDE & INSTRUCTIONS ───────────────────────────────────────
    def _build_instructions_tab(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(16)

        # Section 1: Document Editing, Zoom & Formatting
        grp_fmt = QGroupBox("1. Document Editing, Zoom & Formatting")
        fmt_layout = QVBoxLayout(grp_fmt)
        lbl_fmt = QLabel(
            "• <b>Font Styles & Scaler:</b> Highlight text in the document editor and choose any font family or point size from the top ribbon without overlapping formatting controls.\n"
            "• <b>Text & Highlight Colors:</b> Use the <b>A</b> button for font color or <b>🖍</b> for background highlighter color.\n"
            "• <b>Canvas Zooming:</b> Press <b>Ctrl + +</b> (or <b>Ctrl + =</b>) to zoom in, <b>Ctrl + -</b> to zoom out, and <b>Ctrl + 0</b> to reset to 100%. You can also hold <b>Ctrl</b> and rotate the mouse wheel to scale smoothly between 50% and 300%.\n"
            "• <b>Live Spell Checking:</b> Inline spell checking flags typographical errors in real time with red underlines.\n"
            "• <b>Academic Presets:</b> Select APA 7th, MLA 9th, or IEEE formatting presets under the <i>Page Layout</i> ribbon tab."
        )
        lbl_fmt.setWordWrap(True)
        lbl_fmt.setStyleSheet("font-size: 12px; line-height: 1.5;")
        fmt_layout.addWidget(lbl_fmt)
        layout.addWidget(grp_fmt)

        # Section 2: Mouse Controls & Cursor Customization
        grp_mouse = QGroupBox("2. Mouse Controls & Cursor Customization")
        mouse_layout = QVBoxLayout(grp_mouse)
        lbl_mouse = QLabel(
            "• <b>Selecting Text:</b> Click and drag the left mouse button across text to highlight it with a vivid blue background.\n"
            "• <b>Deselecting Text:</b> Left-click anywhere on the canvas to clear the selection and place the typing cursor.\n"
            "• <b>Right-Click Context Menu:</b> Right-clicking inside or outside selection pops up a menu with <b>Cut</b>, <b>Copy</b>, <b>Paste</b>, and <b>Select All</b>.\n"
            "• <b>Cursor & Caret Customization:</b> On the <i>Page Layout</i> tab in the top ribbon, customize both your Caret and Mouse cursors:\n"
            "   - <i>I-Beam Line:</i> Classic vertical bar caret.\n"
            "   - <i>Thick Bar:</i> Bold 4px high-visibility vertical bar.\n"
            "   - <i>Full Block Caret:</i> Terminal-style solid block caret.\n"
            "   - <i>Underline Caret:</i> Horizontal underline caret beneath the character.\n"
            "   - <i>Crosshair Pointer:</i> Precision crosshair mouse cursor."
        )
        lbl_mouse.setWordWrap(True)
        lbl_mouse.setStyleSheet("font-size: 12px; line-height: 1.5;")
        mouse_layout.addWidget(lbl_mouse)
        layout.addWidget(grp_mouse)

        # Section 3: History & Quick Access Drafts
        grp_hist = QGroupBox("3. History & Quick Access Drafts")
        hist_layout = QVBoxLayout(grp_hist)
        lbl_hist = QLabel(
            "• <b>Quick Access on Home Page:</b> The Home view features a dynamic <i>Quick Access — Recent & Unfinished Drafts</i> panel showing live autosaves, timestamps, and word counts. Clicking any draft card resumes your editing session instantly.\n"
            "• <b>Version Restoration:</b> Navigate to the <b>History</b> page from the sidebar to inspect complete historical revisions, view diffs, and restore prior versions with one click.\n"
            "• <b>Autosave Safety Net:</b> Documents are automatically preserved before AI operations and major structural changes."
        )
        lbl_hist.setWordWrap(True)
        lbl_hist.setStyleSheet("font-size: 12px; line-height: 1.5;")
        hist_layout.addWidget(lbl_hist)
        layout.addWidget(grp_hist)

        # Section 4: Dual-Mode AI Copilot & Settings Directives
        grp_tools = QGroupBox("4. Dual-Mode AI Copilot (Document & Code Modes)")
        tools_layout = QVBoxLayout(grp_tools)
        lbl_tools = QLabel(
            "• <b>Dual Modes:</b> The AI Copilot operates in two distinct operational contexts:\n"
            "   - <i>📄 Document Mode:</i> Summarize, Polish, Expand, Proofread, and Outline with direct cursor insertion or replacement.\n"
            "   - <i>💻 Code Mode:</i> Unit Tests, Refactor, Security Audit, Type Annotations, and Algorithmic Optimization with clean code extraction directly into the active code buffer.\n"
            "• <b>Mode Toggle:</b> Click the <b>[💻 Code Mode]</b> / <b>[📄 Doc Mode]</b> button in the Copilot header to switch at any time. When you navigate to the Code Workspace, the Copilot automatically switches to Code Mode.\n"
            "• <b>Custom Code Directives in Settings:</b> Add your own custom prompt pills and AI directives under <i>Settings → Code Editor AI Prompts & Directives</i>. Your saved directives immediately appear in the Copilot's quick action bar."
        )
        lbl_tools.setWordWrap(True)
        lbl_tools.setStyleSheet("font-size: 12px; line-height: 1.5;")
        tools_layout.addWidget(lbl_tools)
        layout.addWidget(grp_tools)

        # Section 5: Multi-Tab Code Workspace & Custom Themes
        grp_code = QGroupBox("5. Multi-Tab Code Workspace & Custom Editor Themes")
        code_layout = QVBoxLayout(grp_code)
        lbl_code = QLabel(
            "• <b>Multi-Tab Buffer:</b> Manage multiple files simultaneously with closable, movable tabs. Press <b>Ctrl + T</b> to open a new tab and <b>Ctrl + W</b> to close the active tab.\n"
            "• <b>Pygments Syntax Highlighting:</b> Full lexical token styling for Python, JavaScript, TypeScript, C++, Rust, Go, HTML, CSS, SQL, JSON, YAML, and Markdown.\n"
            "• <b>Editor Background Themes:</b> Switch between Monokai Dark, VS Code Dark+, Dracula, Cyberpunk, GitHub Light, and Solarized Dark.\n"
            "• <b>Custom Background Palette:</b> Select <i>🎨 Custom Color...</i> to open the interactive color picker and set any background hue you desire. Gutter, cursor line, and text contrast adjust automatically.\n"
            "• <b>Code Zooming:</b> Press <b>Ctrl + +</b> or <b>Ctrl + -</b> to adjust code font size, or <b>Ctrl + 0</b> to reset."
        )
        lbl_code.setWordWrap(True)
        lbl_code.setStyleSheet("font-size: 12px; line-height: 1.5;")
        code_layout.addWidget(lbl_code)
        layout.addWidget(grp_code)

        # Section 6: Alpha Nexus Command Dock — Live Telemetry & Readability HUD
        grp_telemetry = QGroupBox("6. Alpha Nexus Command Dock — Live Telemetry & Readability HUD")
        telemetry_layout = QVBoxLayout(grp_telemetry)
        lbl_telemetry = QLabel(
            "• <b>Live Telemetry HUD:</b> Situated in the bottom status dock, the Alpha Nexus HUD computes real-time compositional metrics:\n"
            "   - <i>Typing Cadence:</i> Real-time Words Per Minute (WPM) speed measurement and estimated reading duration.\n"
            "   - <i>Readability Indices:</i> Computes the <b>Flesch-Kincaid Grade Level</b> and <b>Coleman-Liau Index</b> to verify target audience suitability.\n"
            "   - <i>Lexical Diversity:</i> Measures vocabulary richness (unique word ratio) and syllable complexity.\n"
            "• <b>HUD Popover:</b> Click on the telemetry pill in the bottom bar to open the expanded statistical breakdown dashboard."
        )
        lbl_telemetry.setWordWrap(True)
        lbl_telemetry.setStyleSheet("font-size: 12px; line-height: 1.5;")
        telemetry_layout.addWidget(lbl_telemetry)
        layout.addWidget(grp_telemetry)

        # Section 7: Focus Soundscape Audio & Real-time Equalizer Waveform
        grp_audio = QGroupBox("7. Focus Soundscape Audio & Real-time Waveform Equalizer")
        audio_layout = QVBoxLayout(grp_audio)
        lbl_audio = QLabel(
            "• <b>Calm & Relaxing Psychoacoustic Soundscapes:</b> Integrated procedural audio synthesizer designed for flow-state writing and deep focus. Choose from:\n"
            "   - <i>🎧 40Hz Gamma Focus Waves:</i> 432Hz golden harmonic tone + 108Hz grounding sub-bass with gentle 40Hz sinusoidal gamma focus pulsation.\n"
            "   - <i>🌧️ Cyberpunk Rain on Skylight:</i> Warm 2-stage low-pass filtered rainfall below 500Hz with delicate glass droplet transients and 50Hz distant shelter rumble.\n"
            "   - <i>🌌 Deep Space White Noise:</i> Pure velvety Brownian 1/f² noise with a slow 0.08Hz cosmic tide breathing swell.\n"
            "   - <i>☕ Ambient Lo-Fi Coffeehouse:</i> Warm analog Rhodes-style D Major 9 chord drone with gentle tape warmth.\n"
            "• <b>44-Bar Stretched Waveform Equalizer:</b> An expansive 44-bar visualizer dynamically animates across the bottom command dock, with distinctive rhythm patterns specifically tailored to each soundscape.\n"
            "• <b>Controls & Volume:</b> Use the track dropdown, play/pause toggle, and volume slider directly inside the dock."
        )
        lbl_audio.setWordWrap(True)
        lbl_audio.setStyleSheet("font-size: 12px; line-height: 1.5;")
        audio_layout.addWidget(lbl_audio)
        layout.addWidget(grp_audio)

        # Section 8: Interactive Multi-Page Filmstrip
        grp_filmstrip = QGroupBox("8. Interactive Multi-Page Filmstrip")
        filmstrip_layout = QVBoxLayout(grp_filmstrip)
        lbl_filmstrip = QLabel(
            "• <b>Live Visual Overview:</b> Click the <b>📑 Filmstrip</b> button in the bottom Alpha Nexus dock to view real-time rendered thumbnail cards for every page of your document.\n"
            "• <b>Instant Navigation:</b> Click any thumbnail card in the filmstrip to scroll the document viewer directly to that page.\n"
            "• <b>Active Page Indicator:</b> The currently visible page is highlighted with a glowing theme-colored accent border."
        )
        lbl_filmstrip.setWordWrap(True)
        lbl_filmstrip.setStyleSheet("font-size: 12px; line-height: 1.5;")
        filmstrip_layout.addWidget(lbl_filmstrip)
        layout.addWidget(grp_filmstrip)

        layout.addStretch()
        scroll.setWidget(container)
        return scroll

    # ── TAB 2: KEYBOARD SHORTCUTS REFERENCE ──────────────────────────────────
    def _build_shortcuts_tab(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Filter Search Bar
        filter_layout = QHBoxLayout()
        lbl_search = QLabel("🔍 Search Shortcuts:")
        lbl_search.setStyleSheet("font-weight: bold;")
        filter_layout.addWidget(lbl_search)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type key name, action, or category (e.g. Copy, Ctrl, Selection)...")
        self.search_input.textChanged.connect(self._filter_shortcuts)
        filter_layout.addWidget(self.search_input, 1)

        layout.addLayout(filter_layout)

        # Shortcuts Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Category", "Shortcut Keys", "Action Description"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 140)
        self.table.setColumnWidth(1, 200)

        self._populate_shortcuts(SHORTCUTS_DATA)
        layout.addWidget(self.table, 1)

        return container

    def _populate_shortcuts(self, items: list[ShortcutItem]):
        self.table.setRowCount(len(items))
        for row, item in enumerate(items):
            cat_item = QTableWidgetItem(item.category)
            cat_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            
            key_item = QTableWidgetItem(item.keys)
            key_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            key_item.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
            
            desc_item = QTableWidgetItem(item.description)
            desc_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            self.table.setItem(row, 0, cat_item)
            self.table.setItem(row, 1, key_item)
            self.table.setItem(row, 2, desc_item)

    def _filter_shortcuts(self, query: str):
        query = query.strip().lower()
        if not query:
            filtered = SHORTCUTS_DATA
        else:
            filtered = [
                item for item in SHORTCUTS_DATA
                if query in item.category.lower() or query in item.keys.lower() or query in item.description.lower()
            ]
        self._populate_shortcuts(filtered)
