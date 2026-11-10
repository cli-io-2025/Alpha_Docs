import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QComboBox, QPushButton, QLabel, QFrame, QSplitter
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QShortcut, QKeySequence

# Import modularized components
from themes import ThemeManager
from nav_panel import NavPanel
from bottom_bar import BottomBar
from model_panel import ModelPanel
from page_home import HomePage
from page_settings import SettingsPage
from page_editor import DocumentEditorPage
from page_code_editor import CodeEditorPage
from page_history import HistoryPage
from page_help import HelpPage

# Stub pages for items without unique view files
class PlaceholderPage(QFrame):
    def __init__(self, title_text: str):
        super().__init__()
        self.setObjectName("pageContainer")
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        
        lbl = QLabel(title_text)
        lbl.setObjectName("pageTitle")
        layout.addWidget(lbl)
        
        sub = QLabel(f"This is the view container for the {title_text.lower()} subsystem.")
        sub.setObjectName("pageSubtitle")
        layout.addWidget(sub)
        
        layout.addStretch()
        self.setLayout(layout)


class DocumentProcessorApp(QMainWindow):
    """Main application window for the unified Alpha_Docs Document Suite."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alpha_Docs — Enterprise Document Suite")
        self.setGeometry(100, 100, 1400, 950)
        self.setMinimumSize(1200, 850)

        # Set Window Branding Icon
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "app_icon.ico")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "app_icon.png")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "alphatech_logo.jpg")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Initialize Theme Engine
        from themes import load_theme_prefs
        self.prefs_file = os.path.join(os.path.dirname(__file__), "theme_prefs.json")
        prefs = load_theme_prefs()
        saved_theme = prefs.get("theme", "Blue")
        self.theme_mgr = ThemeManager(saved_theme)
        
        self._build_ui()
        self._wire_signals()
        self.update_stylesheet()

    def _build_ui(self) -> None:
        # Central baseline widget
        self.main_container = QWidget()
        self.setCentralWidget(self.main_container)
        
        # Root layout for entire window
        self.root_layout = QVBoxLayout()
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)

        # ── Draggable Splitter between Workspace (Outlines/Canvas) and AI Model Panel
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.setObjectName("mainSplitter")
        
        # ── Left-to-Right App Space ──────────────────────────────────────────
        self.app_space = QWidget()
        self.app_layout = QVBoxLayout()
        self.app_layout.setContentsMargins(0, 0, 0, 0)
        self.app_layout.setSpacing(0)
        self.app_space.setLayout(self.app_layout)
        
        # ── Top Header Section ────────────────────────────────────────────────
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(12, 6, 12, 6)

        # Nav panel collapse / toggle button
        self.btn_toggle_nav = QPushButton("☰ Navigation")
        self.btn_toggle_nav.setObjectName("toggleNavButton")
        self.btn_toggle_nav.setToolTip("Toggle navigation sidebar (Ctrl+\\)")
        self.btn_toggle_nav.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle_nav.setFixedHeight(34)
        header_layout.addWidget(self.btn_toggle_nav)
        
        header_layout.addStretch()
        
        # Core Quick-Theme Selector in header
        self.theme_selector = QComboBox()
        self.theme_selector.setObjectName("themeSelector")
        self.theme_selector.addItems(self.theme_mgr.names)
        self.theme_selector.setCurrentText(self.theme_mgr.current.name)
        header_layout.addWidget(self.theme_selector)
        
        # Action pipeline button
        self.model_button = QPushButton("Call Model")
        self.model_button.setObjectName("modelButton")
        self.model_button.setFixedSize(140, 38)
        header_layout.addWidget(self.model_button)
        self.app_layout.addLayout(header_layout)
        
        # ── Middle Display Workspace ──────────────────────────────────────────
        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)
        
        # Core Left Navigation Panel
        self.nav_panel = NavPanel()
        content_layout.addWidget(self.nav_panel, 0)
        
        # Middle Stacked Widget for Page Subsystems
        self.page_stack = QStackedWidget()
        
        # Instantiate views
        init_t = self.theme_mgr.current
        self.page_home = HomePage(
            accent=init_t.accent,
            text_color=init_t.text_bright if init_t.text_bright else init_t.text_primary,
            subtext_color=init_t.text_secondary
        )
        self.page_settings = SettingsPage(current_theme_name=self.theme_mgr.current.name)
        self.page_settings.theme_mgr = self.theme_mgr
        self.page_editor = DocumentEditorPage()
        self.page_code_editor = CodeEditorPage()
        self.page_history = HistoryPage()
        self.page_help = HelpPage()
        
        # Track active views map
        self.pages: dict[str, QWidget] = {
            "home": self.page_home,
            "new_document": self.page_editor,
            "settings": self.page_settings,
            "code_editor": self.page_code_editor,
            "history": self.page_history,
            "help": self.page_help,
            "about": PlaceholderPage("About Alpha Tech Suite"),
        }
        # Mount views into system stack
        for key, widget in self.pages.items():
            self.page_stack.addWidget(widget)
            
        self.page_editor.ribbon.help_requested.connect(lambda: (self.nav_panel.set_active("help"), self.route_page("help")))
            
        content_layout.addWidget(self.page_stack, 1)
        self.app_layout.addLayout(content_layout, 1)
        
        # ── Bottom Bar Status Loop ────────────────────────────────────────────
        self.bottom_bar = BottomBar()
        self.app_layout.addWidget(self.bottom_bar)
        
        # Assemble Main Splitter
        self.main_splitter.addWidget(self.app_space)
        self.model_panel = ModelPanel()
        self.main_splitter.addWidget(self.model_panel)
        self.main_splitter.setCollapsible(0, False)
        self.main_splitter.setCollapsible(1, True)
        self.main_splitter.setStretchFactor(0, 1)
        self.main_splitter.setStretchFactor(1, 0)
        
        self.root_layout.addWidget(self.main_splitter)
        self.main_container.setLayout(self.root_layout)



    def handle_new_document_request(self):
        from PySide6.QtWidgets import QMessageBox
        
        # If we are not currently looking at the editor, just route to it.
        if self.page_stack.currentWidget() != self.page_editor:
            self.nav_panel.set_active("new_document")
            self.route_page("new_document")
            return
            
        # If we are on the editor page, check if there is content to save
        content = self.page_editor.editor.document().toPlainText().strip()
        if not content:
            self.create_new_document()
            return
            
        reply = QMessageBox.question(
            self, 'Save Document?',
            'Do you want to save the current document before creating a new one?',
            QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save
        )
        
        if reply == QMessageBox.StandardButton.Save:
            if self.page_editor._on_save_document():
                self.create_new_document()
        elif reply == QMessageBox.StandardButton.Discard:
            self.create_new_document()
        # If Cancel, do nothing

    # Inside DocumentProcessorApp in main.py
    def create_new_document(self):
        """Resets the editor canvas workspace and forces focus to the editor page."""
        # 1. Clear any lingering text buffers
        self.page_editor.editor.document().clear()
    
        # 2. Re-enforce standard double-spaced block configurations and text color
        cursor = self.page_editor.editor.cursor()
        cursor.setBlockFormat(self.page_editor.apa_body_format)
        
        char_fmt = cursor.charFormat()
        char_fmt.setForeground(Qt.GlobalColor.black)
        cursor.setCharFormat(char_fmt)
        
        self.page_editor.editor._set_cursor(cursor)
    
        # 3. Bring the workspace frame directly into view
        self.nav_panel.set_active("new_document")
        self.route_page("new_document")
        print("[ENGINE] New document initialized successfully.")    

    def import_document(self):
        """Opens a file dialog to import a text document into the editor."""
        from PySide6.QtWidgets import QFileDialog
        from document_io import DocumentIOEngine
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Document", "", "Supported Files (*.txt *.md *.html *.htm *.docx);;Text Files (*.txt *.md);;HTML Files (*.html *.htm);;All Files (*)"
        )
        if file_path:
            try:
                success = DocumentIOEngine.import_file(file_path, self.page_editor.editor.document())
                if not success:
                    print(f"[ENGINE] DocumentIOEngine failed to import: {file_path}")
                    return
                
                cursor = self.page_editor.editor.cursor()
                cursor.setPosition(0)
                from PySide6.QtGui import QTextCursor
                cursor.select(QTextCursor.SelectionType.Document)
                
                char_fmt = cursor.charFormat()
                char_fmt.setForeground(Qt.GlobalColor.black)
                cursor.setCharFormat(char_fmt)
                
                cursor.setBlockFormat(self.page_editor.apa_body_format)
                cursor.clearSelection()
                self.page_editor.editor._set_cursor(cursor)
                
                self.route_page("new_document")
                print(f"[ENGINE] Document imported successfully from {file_path}")
            except Exception as e:
                print(f"[ENGINE] Failed to import document: {e}")

    # ── Page Switching Logic ─────────────────────────────────────────
    def route_page(self, key: str) -> None:
        """Switches the central view to the requested subsystem page."""
        if key == "add_document":
            self.import_document()
            return

        if key in self.pages:
            target_widget = self.pages[key]
            self.page_stack.setCurrentWidget(target_widget)
            self.nav_panel.set_active(key)
            
            # Auto-align Model Panel mode with active workspace
            if key == "code_editor":
                self.model_panel.set_code_mode(True)
                self.model_panel.show()
            elif key in ("home", "new_document"):
                self.model_panel.set_code_mode(False)
                self.model_panel.show()
            elif key == "settings":
                self.model_panel.hide()
            else:
                self.model_panel.show()
                
            print(f"[NAVIGATOR] Routed window viewport to frame: {key}")


    def handle_collaborative_brainstorm(self, instructions):
        """Central handler for AI requests coming from the Editor Ribbon. 
           Opens the Model Panel and pre-populates the prompt."""
        if isinstance(instructions, dict):
            action = instructions.get("action", "AI Copilot")
            instruction = instructions.get("instruction", "Assist with editing")
            target_text = (
                instructions.get("selected_text")
                or instructions.get("current_paragraph")
                or instructions.get("full_document")
                or ""
            )
            doc_type = f"AI {action}"
            prompt = f"Instruction: {instruction}\n\nTarget Content:\n{target_text}" if target_text else instruction
        else:
            doc_type = "Collaborative Brainstorm"
            prompt = str(instructions)

        self.model_panel.open_panel(doc_type=doc_type)
        self.model_panel.set_prompt_text(prompt)
    

    def request_ai_expansion(self, instructions: str = "Expand this section by roughly 250 words"):
        """Packages editor state and hands it off to the model panel pipeline."""
        # Retrieve the state directly from your editor page component
        context = self.page_editor.get_prompt_context()
    
        # Construct a robust template prompt that forces APA semantic alignment
        system_prompt = (
            "You are an academic writing assistant.You must follow instructions closely. "
            "Maintain the exact tone, perspective, and tense of the provided essay. "
            "Do not include conversational filler like 'Sure, here is an expansion:'—return ONLY the essay text."
        )
    
        user_prompt = f"""
        Context Guidelines:
        Total Current Essay: \"\"\"{context['full_document']}\"\"\"
        Target Focus Paragraph: \"\"\"{context['current_paragraph']}\"\"\"
        Specific Selected Text (if any): \"\"\"{context['selected_text']}\"\"\"
    
        Task: {instructions}
        """
    
        # Send the payload directly over to your ModelPanel trace engine[cite: 3, 4]
        # You can update open_panel to accept the combined strings for processing
        self.model_panel.open_panel(doc_type="APA Essay Expansion") 
    
        # Once your simulated or real API call returns the text, you pipe it back:
        # self.page_editor.insert_model_generation(response_text)


    def _wire_signals(self) -> None:
        # Route left navigation inputs to stack index updates
        self.nav_panel.page_requested.connect(self.route_page)
        self.nav_panel.new_document_requested.connect(self.handle_new_document_request)
        self.page_editor.editor.new_document_requested.connect(self.handle_new_document_request)
        self.nav_panel.doc_type_changed.connect(self.on_global_doc_type_modified)
        
        # Navigation toggle controls
        self.btn_toggle_nav.clicked.connect(self.toggle_nav_panel)
        self.nav_panel.collapse_requested.connect(self.toggle_nav_panel)
        self.nav_shortcut = QShortcut(QKeySequence("Ctrl+\\"), self)
        self.nav_shortcut.activated.connect(self.toggle_nav_panel)
        
        # Interlock theme managers across views
        self.theme_selector.currentTextChanged.connect(self.change_theme)
        self.page_settings.theme_changed.connect(self.change_theme)
        
        # Hook action panel interactions
        self.model_button.clicked.connect(self.trigger_model_pipeline)
        self.model_panel.closed.connect(lambda: self.model_button.setEnabled(True))
        
        # Internal application event routing stubs
        self.page_home.artifact_selected.connect(self._on_home_template_selected)
        self.page_home.document_selected.connect(self._on_home_template_selected)
        self.page_home.recent_document_selected.connect(self._load_document_from_history)

        # ── Wire Editor & Code Collaboration Signals ──────────────────────
        self.page_editor.expansion_requested.connect(self.handle_collaborative_brainstorm)
        self.model_panel.insert_into_doc_requested.connect(self.page_editor.insert_generation)
        self.model_panel.replace_selection_requested.connect(self.page_editor.replace_selection)
        self.model_panel.insert_into_code_requested.connect(self.page_code_editor.insert_code_at_cursor)
        self.model_panel.replace_code_selection_requested.connect(self.page_code_editor.replace_code_selection)

        # ── Settings & Code Prompts Synchronization ───────────────────────
        self.page_settings.code_prompts_changed.connect(self.model_panel.update_custom_code_prompts)
        self.model_panel.update_custom_code_prompts(self.page_settings.get_code_prompts())
        
        # ── History Subsystem Wiring ───────────────────────────────────────
        self.page_editor.save_requested.connect(self.page_history.save_document)
        self.page_editor.save_requested.connect(lambda *_: self.page_home.refresh_recent_documents())
        self.page_history.document_restored.connect(self._load_document_from_history)
        self.model_panel.generation_started.connect(self._auto_save_document)

        # ── Bottom Bar Live Metrics & Filmstrip Synchronization ────────────
        self.page_editor.editor.document().contentsChanged.connect(self._sync_bottom_bar_metrics)
        self.page_editor.editor.zoom_changed.connect(lambda _: self._sync_bottom_bar_metrics())
        self.bottom_bar.filmstrip_page_clicked.connect(self._on_filmstrip_page_selected)
        self.bottom_bar.nexus_dock.filmstrip_refresh_requested.connect(self._refresh_filmstrip)
        self._sync_bottom_bar_metrics()
        self._refresh_filmstrip()

    # ── Controller Methods ────────────────────────────────────────────────────

    def _sync_bottom_bar_metrics(self) -> None:
        """Pulls statistical metrics from the active document view engine and updates the bottom status bar."""
        try:
            stats = self.page_editor.editor.get_document_statistics()
            self.bottom_bar.update_metrics(
                words=stats.get("words", 0),
                chars=stats.get("chars", 0),
                pages=stats.get("pages", 1),
                zoom_pct=stats.get("zoom", 100),
            )
            self._refresh_filmstrip()
        except Exception as e:
            print(f"[STATUS] Error syncing metrics: {e}")

    def _refresh_filmstrip(self) -> None:
        """Renders live page thumbnails of the document canvas into the Filmstrip dock."""
        try:
            pixmaps = self.page_editor.editor.get_all_page_thumbnails(target_h=46)
            active_page = self.page_editor.editor.current_page_index()
            self.bottom_bar.update_filmstrip_pages(pixmaps, active_page)
        except Exception as e:
            print(f"[FILMSTRIP] Error rendering filmstrip thumbnails: {e}")

    def _on_filmstrip_page_selected(self, page_idx: int) -> None:
        """Navigates the document editor canvas directly to the clicked filmstrip page."""
        if self.page_stack.currentWidget() != self.page_editor:
            self.nav_panel.set_active("new_document")
            self.route_page("new_document")
        self.page_editor.editor.scroll_to_page(page_idx)

    def open_resume_template_picker(self) -> None:
        """Opens the visual Resume Template Studio modal allowing user to choose and clone a template."""
        from template_picker import ResumeTemplatePicker
        acc = getattr(self.theme_mgr.current, "accent", "#00adb5")
        txt = getattr(self.theme_mgr.current, "text", "#f0f4f8")
        sub = getattr(self.theme_mgr.current, "subtext", "#9aa5b5")
        dialog = ResumeTemplatePicker(self, accent=acc, text_color=txt, subtext_color=sub)
        if dialog.exec():
            selected = dialog.selected_template_key
            if selected:
                self.load_template_copy(selected)

    def open_brochure_template_picker(self) -> None:
        """Opens the visual Brochure Template Studio modal allowing user to choose and clone a template."""
        from template_picker import BrochureTemplatePicker
        acc = getattr(self.theme_mgr.current, "accent", "#00adb5")
        txt = getattr(self.theme_mgr.current, "text", "#f0f4f8")
        sub = getattr(self.theme_mgr.current, "subtext", "#9aa5b5")
        dialog = BrochureTemplatePicker(self, accent=acc, text_color=txt, subtext_color=sub)
        if dialog.exec():
            selected = dialog.selected_template_key
            if selected:
                self.load_template_copy(selected)

    def load_template_copy(self, template_key: str) -> None:
        """Loads a fresh copy of the specified template into the editor canvas and focuses the workspace."""
        from document_presets import SAMPLE_TEMPLATES
        template_content = SAMPLE_TEMPLATES.get(template_key)
        if not template_content:
            for k, v in SAMPLE_TEMPLATES.items():
                if k.lower() == template_key.lower():
                    template_content = v
                    break

        if not template_content:
            template_content = f"# {template_key}\n\nStart writing your {template_key.lower()} draft here...\n"

        # Apply appropriate page margins (resumes and brochures use modern 12mm margins for full presentation)
        if "resume" in template_key.lower() or "brochure" in template_key.lower():
            self.page_editor.editor.setMarginsMM(12.0, 12.0, 12.0, 12.0)
        else:
            self.page_editor.editor.setMarginsMM(25.4, 25.4, 25.4, 25.4)

        doc = self.page_editor.editor.document()
        if template_content.strip().startswith("<"):
            doc.setHtml(template_content)
        else:
            doc.setMarkdown(template_content)

        from PySide6.QtGui import QTextCursor
        cursor = QTextCursor(doc)
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        self.page_editor.editor._set_cursor(cursor)

        self.nav_panel.set_active("new_document")
        self.route_page("new_document")
        self._sync_bottom_bar_metrics()
        print(f"[ENGINE] Produced working copy of template '{template_key}' in editor.")

    def _on_home_template_selected(self, template_key: str) -> None:
        """Loads a pre-formatted template or opens the editor with a structured draft."""
        if template_key.lower() == "resume":
            if os.environ.get("QT_QPA_PLATFORM") == "offscreen":
                self.load_template_copy("Resume - Strategic Marketing")
            else:
                self.open_resume_template_picker()
            return
        elif template_key.lower() == "brochure":
            if os.environ.get("QT_QPA_PLATFORM") == "offscreen":
                self.load_template_copy("Brochure - Bi-Fold Spread")
            else:
                self.open_brochure_template_picker()
            return

        self.load_template_copy(template_key)

    def _auto_save_document(self):
        content = self.page_editor.editor.document().toHtml()
        if content.strip():
            self.page_history.save_document("Autosave_Before_AI", content, is_autosave=True)
            self.page_home.refresh_recent_documents()
            
    def _load_document_from_history(self, title: str, content: str):
        if not content:
            content = ""
        doc = self.page_editor.editor.document()
        # If content contains HTML tags, render as HTML; otherwise render as plain text to preserve formatting
        stripped = content.strip()
        if stripped.startswith("<") and any(tag in stripped.lower() for tag in ("<html", "<p", "<div", "<body", "<span")):
            doc.setHtml(content)
        else:
            doc.setPlainText(content)
        
        from PySide6.QtGui import QTextCursor
        cursor = QTextCursor(self.page_editor.editor.document())
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        self.page_editor.editor._set_cursor(cursor)
        
        self.route_page("new_document")
        print(f"[ENGINE] Document '{title}' restored from history successfully.")

    def change_theme(self, theme_name: str) -> None:
        """Synchronizes and enforces QSS skin styles globally across components."""
        if self.theme_mgr.set_theme(theme_name):
            # Update local toggle widget selections without triggering cyclical signal feedback
            self.theme_selector.blockSignals(True)
            self.theme_selector.setCurrentText(theme_name)
            self.theme_selector.blockSignals(False)
            
            self.page_settings.blockSignals(True)
            self.page_settings.set_active_theme(theme_name)
            self.page_settings.blockSignals(False)
            
            self.update_stylesheet()
            print(f"[THEME] Switch verified. Interface runtime changed to: {theme_name}")
            self.theme_mgr.save_theme(theme_name)

    def update_stylesheet(self) -> None:
        """Regenerates and sets style matrix sheets over window tree."""
        self.setStyleSheet(self.theme_mgr.stylesheet())
        t = self.theme_mgr.current
        accent = t.accent
        text_color = t.text_bright if t.text_bright else t.text_primary
        subtext_color = t.text_secondary

        # Propagate dynamic theme accent glow to all views & sub-components
        if hasattr(self, "bottom_bar") and hasattr(self.bottom_bar, "set_theme_accent"):
            self.bottom_bar.set_theme_accent(accent)
        if hasattr(self, "model_panel") and hasattr(self.model_panel, "set_theme_accent"):
            self.model_panel.set_theme_accent(accent)
        if hasattr(self, "page_code_editor") and hasattr(self.page_code_editor, "set_theme_accent"):
            self.page_code_editor.set_theme_accent(accent)
        if hasattr(self, "page_editor") and hasattr(self.page_editor, "set_theme_accent"):
            self.page_editor.set_theme_accent(accent)
        if hasattr(self, "page_settings") and hasattr(self.page_settings, "set_theme_accent"):
            self.page_settings.set_theme_accent(accent)
        if hasattr(self, "page_home") and hasattr(self.page_home, "set_theme_accent"):
            self.page_home.set_theme_accent(accent, text_color, subtext_color)

    def toggle_nav_panel(self) -> None:
        """Toggles the left navigation panel visibility and synchronizes toggle button state."""
        visible = not self.nav_panel.isVisible()
        self.nav_panel.setVisible(visible)
        self.btn_toggle_nav.setText("☰ Navigation" if visible else "☰ Show Navigation")
        print(f"[NAVIGATOR] Navigation panel toggled -> visible={visible}")

    def trigger_model_pipeline(self) -> None:
        """Deactivates action control buttons and runs asynchronous model window slide-in."""
        self.model_button.setEnabled(False)
        active_doc = self.nav_panel.current_doc_type()
        self.model_panel.open_panel(active_doc)
        # Allocate appropriate space in splitter if currently collapsed
        sizes = self.main_splitter.sizes()
        if len(sizes) >= 2 and sizes[1] < 200:
            total = sum(sizes) if sum(sizes) > 0 else self.width()
            target_ai = 380
            self.main_splitter.setSizes([max(500, total - target_ai), target_ai])
        print(f"[PIPELINE] Invoking tool verification workflow targets for: {active_doc}")

    def on_global_doc_type_modified(self, doc_type: str) -> None:
        print(f"[ENGINE] Global working type focus reassigned -> {doc_type}")


def main():
    # Explicit Windows AppUserModelID decouples app from generic python.exe taskbar grouping
    if sys.platform == "win32":
        try:
            import ctypes
            myappid = "alphatech.alphadocsuite.app.1.0"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Configure Application-wide Taskbar and Dialog Icon
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "app_icon.ico")
    if not os.path.exists(icon_path):
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "app_icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    window = DocumentProcessorApp()
    # Default selection initialization path
    window.route_page("home")
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()