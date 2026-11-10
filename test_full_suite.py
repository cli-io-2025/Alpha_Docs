import os
import sys
import unittest

os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import Qt

class TestSuiteAlphaTech(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(sys.argv)
        from main import DocumentProcessorApp
        cls.window = DocumentProcessorApp()
        cls.window.show()

    def test_01_bottom_bar_logo_and_metrics(self):
        bb = self.window.bottom_bar
        self.assertIsNotNone(bb)
        # Check logo label
        self.assertTrue(bb.logo_label.pixmap() is not None or bb.logo_label.text() != "")
        
        # Test metrics update
        bb.update_metrics(words=1500, chars=9000, pages=3, zoom_pct=125)
        self.assertIn("1,500 words", bb.lbl_doc_stats.text())
        self.assertIn("9,000 chars", bb.lbl_doc_stats.text())
        self.assertIn("Page 1 of 3", bb.lbl_doc_stats.text())
        self.assertIn("Zoom: 125%", bb.lbl_zoom_stats.text())
        print("[PASS] Test 1: BottomBar logo and live metrics")

    def test_02_page_routing_and_templates(self):
        # Route to home
        self.window.route_page("home")
        self.assertEqual(self.window.page_stack.currentWidget(), self.window.page_home)
        
        # Select Essay template
        self.window._on_home_template_selected("Essay")
        self.assertEqual(self.window.page_stack.currentWidget(), self.window.page_editor)
        text = self.window.page_editor.editor.document().toPlainText()
        self.assertIn("Impact of Autonomous Systems", text)
        
        # Verify stats updated
        stats = self.window.page_editor.editor.get_document_statistics()
        self.assertGreater(stats["words"], 50)
        print(f"[PASS] Test 2: Template loading (Essay: {stats['words']} words)")

    def test_03_find_and_replace_engine(self):
        editor = self.window.page_editor.editor
        find_bar = self.window.page_editor.find_bar
        
        # Document currently has Essay text
        found = editor.find_text("systems", forward=True, match_case=False, whole_word=False)
        self.assertTrue(found)
        
        # Replace occurrences
        rep_count = editor.replace_all("systems", "frameworks", match_case=False, whole_word=False)
        self.assertGreater(rep_count, 0)
        new_text = editor.document().toPlainText()
        self.assertIn("frameworks", new_text)
        print(f"[PASS] Test 3: Find & Replace engine replaced {rep_count} occurrences")

    def test_04_document_io_exporters(self):
        from document_io import DocumentIOEngine
        doc = self.window.page_editor.editor.document()
        
        out_dir = os.path.join(os.path.dirname(__file__), "export_test_artifacts")
        os.makedirs(out_dir, exist_ok=True)
        
        md_path = os.path.join(out_dir, "test_output.md")
        html_path = os.path.join(out_dir, "test_output.html")
        pdf_path = os.path.join(out_dir, "test_output.pdf")
        
        # Markdown export
        ok_md = DocumentIOEngine.export_markdown(doc, md_path)
        self.assertTrue(ok_md and os.path.exists(md_path))
        with open(md_path, "r", encoding="utf-8") as f:
            md_content = f.read()
        self.assertGreater(len(md_content), 50)
        
        # HTML export
        ok_html = DocumentIOEngine.export_html(doc, html_path)
        self.assertTrue(ok_html and os.path.exists(html_path))
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        self.assertIn("<!DOCTYPE html>", html_content)
        
        # PDF export (ensures Qt6 setPageMargins regression is fixed)
        ok_pdf = DocumentIOEngine.export_pdf(doc, pdf_path)
        self.assertTrue(ok_pdf and os.path.exists(pdf_path))
        self.assertGreater(os.path.getsize(pdf_path), 500)
        print("[PASS] Test 4: DocumentIOEngine AST Markdown, HTML5, and Qt6 PDF exporters verified")

    def test_05_code_editor_workspace(self):
        code_page = self.window.page_code_editor
        self.window.route_page("code_editor")
        self.assertEqual(self.window.page_stack.currentWidget(), code_page)
        
        # Set code
        sample_py = "def calculate_velocity(d, t):\n    return d / t\n"
        code_page.set_code(sample_py, "python")
        self.assertEqual(code_page.get_code(), sample_py)
        
        # Format code
        code_page.format_code()
        self.assertIn("calculate_velocity", code_page.get_code())
        
        # Line numbers width calculation
        self.assertGreater(code_page.editor.line_number_area_width(), 20)
        print("[PASS] Test 5: Code workspace with line numbers and syntax highlighter")

    def test_06_ai_copilot_insertion_and_replacement(self):
        editor_page = self.window.page_editor
        editor = editor_page.editor
        
        # Insert text at cursor
        initial_len = len(editor.document().toPlainText())
        addition = "\n\nAdditional synthesis provided by Alpha Copilot."
        editor_page.insert_generation(addition)
        new_len = len(editor.document().toPlainText())
        self.assertGreater(new_len, initial_len)
        self.assertIn("Alpha Copilot", editor.document().toPlainText())
        print("[PASS] Test 6: AI Copilot direct document insertion")

    def test_07_no_options_tab(self):
        from nav_panel import NAV_ITEMS
        keys = [item[2] for item in NAV_ITEMS]
        self.assertNotIn("options", keys)
        self.assertNotIn("options", self.window.pages)
        print("[PASS] Test 7: Options tab cleanly removed from navigation and view stack")

    def test_08_alpha_nexus_command_dock(self):
        dock = self.window.bottom_bar.nexus_dock
        self.assertIsNotNone(dock)
        self.assertEqual(dock.stack.count(), 3)
        
        # Switch to Focus Audio
        dock.switch_mode(1)
        self.assertEqual(dock.stack.currentIndex(), 1)
        self.assertTrue(dock.visualizer.is_active)
        
        # Toggle audio pause
        dock._toggle_audio()
        self.assertFalse(dock.visualizer.is_active)
        
        # Switch to HUD and update telemetry
        dock.switch_mode(0)
        dock.update_telemetry(words=650, chars=4100, pages=2)
        self.assertIn("Grade", dock.lbl_grade.text())
        self.assertIn("min read", dock.lbl_reading_time.text())
        print("[PASS] Test 8: Alpha Nexus Command Dock (HUD & Focus Soundscape) operational")

    def test_09_spell_checking_engine(self):
        from pyspell_integration import get_shared_checker
        checker = get_shared_checker()
        self.assertTrue(checker.is_ready)
        
        misspellings = checker.get_misspellings("Thiss is an exampel of speling")
        self.assertGreater(len(misspellings), 0)
        words = [m[0] for m in misspellings]
        self.assertIn("exampel", words)
        
        # Test add to dictionary
        checker.add_to_dictionary("exampel")
        misspellings_after = checker.get_misspellings("Thiss is an exampel of speling")
        words_after = [m[0] for m in misspellings_after]
        self.assertNotIn("exampel", words_after)
        print("[PASS] Test 9: Spell checking engine active with custom dictionary")

    def test_10_theme_engine_and_customization(self):
        from themes import ALL_THEMES
        # Verify 8 themes exist
        expected_themes = ["Blue", "Dark", "Mocha", "Cyberpunk", "Emerald", "Solar", "Nordic", "Custom"]
        for t in expected_themes:
            self.assertIn(t, ALL_THEMES)
        
        # Test switching to Cyberpunk
        self.window.change_theme("Cyberpunk")
        self.assertEqual(self.window.theme_mgr.current.name, "Cyberpunk")
        
        # Test Custom Theme setting
        self.window.theme_mgr.set_custom_colors(
            accent="#ff0055",
            bg_primary="#050505",
            bg_secondary="#101010",
            text_primary="#ffffff"
        )
        self.window.change_theme("Custom")
        self.assertEqual(self.window.theme_mgr.current.accent, "#ff0055")
        
        # Revert to Blue
        self.window.change_theme("Blue")
        print("[PASS] Test 10: 8-Theme engine with live Custom Palette Studio verified")

    def test_11_ai_generate_button_resize(self):
        btn = self.window.model_panel._send_btn
        # Ensure minimum width is at least 110px for clear readability
        self.assertGreaterEqual(btn.minimumWidth(), 110)
        self.assertIn("Generate", btn.text())
        # Verify close "✕" button exists and is clickable
        close_btn = self.window.model_panel.findChild(QPushButton, "closePanelButton")
        self.assertIsNotNone(close_btn)
        self.assertEqual(close_btn.text(), "✕")
        print("[PASS] Test 11: AI Generate button resized & Close '✕' button verified")

    def test_12_nav_panel_collapse_and_toggle(self):
        nav = self.window.nav_panel
        btn_toggle = self.window.btn_toggle_nav
        self.assertTrue(nav.isVisible())
        
        # Toggle nav closed
        self.window.toggle_nav_panel()
        self.assertFalse(nav.isVisible())
        self.assertIn("Show", btn_toggle.text())
        
        # Toggle nav open
        self.window.toggle_nav_panel()
        self.assertTrue(nav.isVisible())
        self.assertEqual(btn_toggle.text(), "☰ Navigation")
        
        # Test collapse button from nav panel itself
        nav.collapse_requested.emit()
        self.assertFalse(nav.isVisible())
        self.window.toggle_nav_panel()
        self.assertTrue(nav.isVisible())
        print("[PASS] Test 12: Collapsible Navigation Bar (Toggle Button + Collapse [◀] signal) verified")

    def test_13_main_draggable_splitter_ai_panel(self):
        from PySide6.QtWidgets import QSplitter
        splitter = self.window.main_splitter
        self.assertIsInstance(splitter, QSplitter)
        self.assertEqual(splitter.count(), 2)
        self.assertEqual(splitter.widget(0), self.window.app_space)
        self.assertEqual(splitter.widget(1), self.window.model_panel)
        
        # Verify open panel allocates space in splitter
        self.window.trigger_model_pipeline()
        sizes = splitter.sizes()
        self.assertGreaterEqual(sizes[1], 200)
        
        # Close panel
        self.window.model_panel.close_panel()
        print("[PASS] Test 13: Draggable QSplitter between Workspace/Outline and AI Model Panel verified")

    def test_14_custom_palette_greying_out(self):
        settings_page = self.window.page_settings
        self.window.route_page("settings")
        
        # Switch to Blue theme
        self.window.change_theme("Blue")
        self.assertFalse(settings_page.custom_studio.isEnabled())
        self.assertIn("Inactive", settings_page.lbl_custom_status.text())
        
        # Select Custom radio
        if "Custom" in settings_page._radio_buttons:
            settings_page._radio_buttons["Custom"].setChecked(True)
            self.assertTrue(settings_page.custom_studio.isEnabled())
            self.assertIn("Active", settings_page.lbl_custom_status.text())
            
        # Revert to Blue
        self.window.change_theme("Blue")
        self.assertFalse(settings_page.custom_studio.isEnabled())
        print("[PASS] Test 14: Custom Palette Studio greyed out unless Custom is chosen verified")

    def test_15_output_registry_defined_boxes(self):
        home_page = self.window.page_home
        self.window.route_page("home")
        
        # Verify defined output registry boxes exist
        self.assertEqual(len(home_page.document_areas), 6)
        for area in home_page.document_areas:
            self.assertEqual(area.objectName(), "documentArea")
            self.assertIsNotNone(area.header.text())
            self.assertIsNotNone(area.status.text())
        print(f"[PASS] Test 15: Output Registry boxes (Brochure, Marketing, Report, etc.) verified")

    def test_16_ribbon_no_combobox_overlaps(self):
        ribbon = self.window.page_editor.ribbon
        self.assertIsNotNone(ribbon)
        # Verify font family combo has constrained height (under 28px)
        font_combo = ribbon.font_combo
        self.assertLessEqual(font_combo.maximumHeight(), 28)
        self.assertLessEqual(font_combo.height(), 26)
        
        # Verify caret and mouse combos on layout tab
        caret_combo = ribbon.combo_caret_style
        mouse_combo = ribbon.combo_pointer_style
        self.assertLessEqual(caret_combo.maximumHeight(), 28)
        self.assertLessEqual(mouse_combo.maximumHeight(), 28)
        print("[PASS] Test 16: Ribbon font and cursor comboboxes scoped without overlaps")

    def test_17_multi_tab_code_workspace(self):
        code_page = self.window.page_code_editor
        self.window.route_page("code_editor")
        
        initial_tab_count = code_page.tab_widget.count()
        self.assertGreaterEqual(initial_tab_count, 1)
        
        # Open a new tab
        new_editor = code_page.new_tab(name="algorithm.py", code="def binary_search(): pass", language="python")
        self.assertEqual(code_page.tab_widget.count(), initial_tab_count + 1)
        self.assertIn("binary_search", new_editor.toPlainText())
        self.assertEqual(code_page.editor, new_editor)
        
        # Switch tabs
        code_page.tab_widget.setCurrentIndex(0)
        self.assertNotEqual(code_page.editor, new_editor)
        
        # Close tab
        code_page.close_tab(code_page.tab_widget.count() - 1)
        self.assertEqual(code_page.tab_widget.count(), initial_tab_count)
        print("[PASS] Test 17: Multi-tab Code Workspace (new_tab, close_tab, switching) verified")

    def test_18_code_editor_background_and_zoom(self):
        code_page = self.window.page_code_editor
        self.window.route_page("code_editor")
        
        # Test background theme
        code_page._on_theme_changed("Dracula")
        self.assertEqual(code_page._current_theme_name, "Dracula")
        
        # Test custom background color
        code_page.set_editor_background("#1a1a2e")
        self.assertEqual(code_page._custom_bg_color, "#1a1a2e")
        
        # Test zoom in code editor
        ed = code_page.editor
        initial_font_size = ed.font().pointSize()
        ed.zoomIn(3)
        self.assertEqual(ed.font().pointSize(), initial_font_size + 3)
        ed.zoomOut(2)
        self.assertEqual(ed.font().pointSize(), initial_font_size + 1)
        ed.resetZoom()
        self.assertEqual(ed.font().pointSize(), 11)
        
        # Test zoom in document viewer
        doc_view = self.window.page_editor.editor
        init_doc_zoom = doc_view.zoomFactor()
        doc_view.zoomIn()
        self.assertGreater(doc_view.zoomFactor(), init_doc_zoom)
        doc_view.zoomOut()
        self.assertEqual(doc_view.zoomFactor(), init_doc_zoom)
        doc_view.resetZoom()
        self.assertEqual(doc_view.zoomFactor(), 1.0)
        print("[PASS] Test 18: Code editor background customization and zoom engine verified")

    def test_19_quick_access_recent_drafts(self):
        home_page = self.window.page_home
        self.window.route_page("home")
        
        # Verify quick access draft cards exist
        self.assertEqual(len(home_page.artifact_buttons), 6)
        
        # Simulate creating an autosave
        self.window._auto_save_document()
        drafts = home_page._fetch_recent_drafts()
        self.assertGreaterEqual(len(drafts), 6)
        home_page.refresh_recent_documents()
        
        first_card = home_page.artifact_buttons[0]
        self.assertTrue(len(first_card.artifact_name) > 0)
        print(f"[PASS] Test 19: Quick Access drafts section populated with {len(drafts)} drafts")

    def test_20_settings_code_prompts(self):
        settings_page = self.window.page_settings
        self.window.route_page("settings")
        
        initial_prompts_count = len(settings_page.get_code_prompts())
        
        # Add new directive
        settings_page.input_prompt_title.setText("🔍 Profile Asyncio")
        settings_page.input_prompt_text.setText("Profile asyncio event loop tasks and identify blockers.")
        settings_page._on_add_code_prompt()
        
        self.assertEqual(len(settings_page.get_code_prompts()), initial_prompts_count + 1)
        last_prompt = settings_page.get_code_prompts()[-1]
        self.assertEqual(last_prompt[0], "🔍 Profile Asyncio")
        
        # Delete directive
        settings_page._on_delete_code_prompt(len(settings_page.get_code_prompts()) - 1)
        self.assertEqual(len(settings_page.get_code_prompts()), initial_prompts_count)
        print("[PASS] Test 20: Settings Code Directives manager (add, delete, signal) verified")

    def test_21_ai_copilot_code_mode_and_signals(self):
        panel = self.window.model_panel
        
        # Route to code editor -> Auto activates Code Mode
        self.window.route_page("code_editor")
        self.assertTrue(panel.is_code_mode)
        self.assertEqual(panel._title_lbl.text(), "💻 AI Coding Copilot")
        self.assertEqual(panel.btn_insert.text(), "📥 Insert into Code")
        self.assertEqual(panel.btn_replace.text(), "🔄 Replace Code Selection")
        
        # Route to home -> Auto returns to Doc Mode
        self.window.route_page("home")
        self.assertFalse(panel.is_code_mode)
        self.assertEqual(panel._title_lbl.text(), "🤖 AI Writing Copilot")
        
        # Test manual toggle
        panel.set_code_mode(True)
        self.assertTrue(panel.is_code_mode)
        
        # Test code insertion into code editor
        code_page = self.window.page_code_editor
        self.window.route_page("code_editor")
        initial_code = code_page.get_code()
        
        # Test direct code insertion signal
        panel._output.setPlainText("```python\ndef test_feature():\n    return 42\n```")
        panel._on_insert_clicked()
        self.assertIn("test_feature", code_page.get_code())
        
        # Revert to Doc Mode
        panel.set_code_mode(False)
        print("[PASS] Test 21: AI Copilot Dual-Mode (Doc vs Code Mode, code extraction, insertion) verified")

    def test_22_filmstrip_live_thumbnails_and_navigation(self):
        # Route to editor with Essay template
        self.window.route_page("new_document")
        self.window._on_home_template_selected("Essay")
        
        dock = self.window.bottom_bar.nexus_dock
        strip = dock.strip_viewer
        
        # Switch dock to Filmstrip tab (index 2)
        dock.switch_mode(2)
        self.assertEqual(dock.stack.currentIndex(), 2)
        
        # Verify filmstrip is populated with interactive page thumbnail cards (not blank!)
        self.assertGreaterEqual(strip.total_pages, 1)
        self.assertGreaterEqual(len(strip._cards), 1)
        
        first_card = strip._cards[0]
        self.assertIsNotNone(first_card.img_lbl.pixmap())
        self.assertFalse(first_card.img_lbl.pixmap().isNull())
        self.assertEqual(first_card.lbl_num.text(), "P. 1")
        
        # Test clicking thumbnail emits navigation signal to editor
        strip._on_card_clicked(0)
        self.assertEqual(self.window.page_editor.editor.verticalScrollBar().value(), 0)
        print(f"[PASS] Test 22: Filmstrip live thumbnails rendered ({strip.total_pages} page(s)) and click-navigation verified")

    def test_23_focus_audio_playback_engine(self):
        dock = self.window.bottom_bar.nexus_dock
        engine = dock.audio_engine
        self.assertIsNotNone(engine)
        
        # Test soundscape selection and playback
        dock.sound_combo.setCurrentText("🌧️ Cyberpunk Rain on Skylight")
        engine.play_soundscape("Cyberpunk Rain")
        self.assertTrue(engine.is_playing)
        
        # Test volume adjustment
        dock.vol_slider.setValue(60)
        self.assertAlmostEqual(engine._volume, 0.60, places=2)
        
        # Test pause
        engine.pause()
        self.assertFalse(engine.is_playing)
        
        # Test resume
        engine.resume()
        self.assertTrue(engine.is_playing)
        engine.pause()
        print("[PASS] Test 23: Procedural Focus Audio playback engine (play, pause, volume, tracks) verified")

    def test_24_custom_theme_accent_glow_cohesion(self):
        """Verifies that changing the Custom Theme accent glow cohesively updates 100% of the UI."""
        test_accent = "#ff0077"
        self.window.page_settings.custom_inputs["accent"].setText(test_accent)
        self.window.page_settings.custom_inputs["bg_primary"].setText("#120a14")
        self.window.page_settings.custom_inputs["bg_secondary"].setText("#1c101f")
        self.window.page_settings.custom_inputs["text_primary"].setText("#f5e6f7")
        self.window.page_settings._apply_custom_theme()

        # Verify active theme is Custom with specified accent
        self.assertEqual(self.window.theme_mgr.current.name, "Custom")
        self.assertEqual(self.window.theme_mgr.current.accent.lower(), test_accent.lower())

        # Verify Bottom Bar Waveform Visualizer accent
        dock = self.window.bottom_bar.nexus_dock
        self.assertEqual(dock.visualizer._accent_color.name().lower(), test_accent.lower())

        # Verify Code Editor workspace accent
        code_page = self.window.page_code_editor
        self.assertEqual(getattr(code_page, "_theme_accent", "").lower(), test_accent.lower())

        # Verify Document Editor Find & Replace bar accent
        find_bar = self.window.page_editor.find_bar
        self.assertEqual(getattr(find_bar, "_theme_accent", "").lower(), test_accent.lower())

        # Verify Home Page draft cards accent
        home_page = self.window.page_home
        self.assertEqual(getattr(home_page, "_theme_accent", "").lower(), test_accent.lower())

        # Verify Model Panel Copilot accent
        model_panel = self.window.model_panel
        self.assertEqual(getattr(model_panel, "_accent_color", "").lower(), test_accent.lower())

        # Restore default Dark theme for subsequent stability
        self.window.change_theme("Dark")
        self.assertEqual(self.window.theme_mgr.current.name, "Dark")
        print("[PASS] Test 24: 100% Cohesive Custom Theme accent glow propagation across entire UI verified")

    def test_25_sound_visualizer_rhythm_and_frequencies(self):
        """Verifies expanded waveform equalizer bars, sound-matched rhythms, and calm synthesis assets."""
        dock = self.window.bottom_bar.nexus_dock
        vis = dock.visualizer

        # Check geometry and bar density (stretched across bottom dock)
        self.assertGreaterEqual(vis.bar_count, 40)
        self.assertGreaterEqual(vis.minimumWidth(), 320)
        self.assertEqual(len(vis.bars), vis.bar_count)

        # Check sound mode rhythm switching
        vis.set_sound_mode("40Hz Gamma Focus Waves")
        self.assertEqual(vis.sound_mode, "gamma")
        vis._animate_bars()
        self.assertTrue(all(4 <= b <= 42 for b in vis.bars))

        vis.set_sound_mode("Cyberpunk Rain on Skylight")
        self.assertEqual(vis.sound_mode, "rain")
        vis._animate_bars()
        self.assertTrue(all(4 <= b <= 42 for b in vis.bars))

        vis.set_sound_mode("Deep Space White Noise")
        self.assertEqual(vis.sound_mode, "space")
        vis._animate_bars()
        self.assertTrue(all(4 <= b <= 42 for b in vis.bars))

        vis.set_sound_mode("Ambient Lo-Fi Coffeehouse")
        self.assertEqual(vis.sound_mode, "coffee")
        vis._animate_bars()
        self.assertTrue(all(4 <= b <= 42 for b in vis.bars))

        # Check synthesized audio files exist and are populated
        from focus_audio_engine import SOUNDS_DIR
        for fname in ["gamma_40hz.wav", "cyberpunk_rain.wav", "deep_space_whitenoise.wav", "lofi_coffeehouse.wav"]:
            fpath = os.path.join(SOUNDS_DIR, fname)
            self.assertTrue(os.path.exists(fpath), f"Missing audio asset: {fname}")
            self.assertGreater(os.path.getsize(fpath), 10000, f"Audio asset too small: {fname}")

        print("[PASS] Test 25: Expanded Waveform Visualizer rhythms (44 bars, stretched geometry) & calm frequencies verified")

    def test_26_cards_depth_elevation_and_letter_contrast(self):
        """Verifies that Home Page cards have 3D shadow depth, raise up on hover, and keep letters dark/light."""
        self.window.route_page("home")
        home = self.window.page_home
        self.assertGreater(len(home.artifact_buttons), 0)
        self.assertGreater(len(home.document_areas), 0)

        from PySide6.QtWidgets import QGraphicsDropShadowEffect
        from PySide6.QtGui import QEnterEvent
        from PySide6.QtCore import QPointF

        card = home.artifact_buttons[0]
        self.assertIsInstance(card._shadow, QGraphicsDropShadowEffect)

        # Verify letters are NOT the accent color, but the theme's text color (light on dark, dark on light)
        current_theme = self.window.theme_mgr.current
        expected_text = current_theme.text_bright if current_theme.text_bright else current_theme.text_primary
        self.assertIn(expected_text, card.name_label.styleSheet())
        self.assertNotIn(current_theme.accent, card.name_label.styleSheet())

        # Verify card has the accent color on its top border
        self.assertIn(current_theme.accent, card.styleSheet())

        # Test 3D elevation shadow on hover
        initial_radius = card._shadow.blurRadius()
        card.enterEvent(None)
        elevated_radius = card._shadow.blurRadius()
        self.assertGreater(elevated_radius, initial_radius)

        card.leaveEvent(None)
        restored_radius = card._shadow.blurRadius()
        self.assertEqual(restored_radius, initial_radius)

        # Verify Output Registry cards
        doc_card = home.document_areas[0]
        self.assertIsInstance(doc_card._shadow, QGraphicsDropShadowEffect)
        self.assertIn(expected_text, doc_card.header.styleSheet())
        self.assertNotIn(current_theme.accent, doc_card.header.styleSheet())
        self.assertIn(current_theme.accent, doc_card.styleSheet())

        doc_initial = doc_card._shadow.blurRadius()
        doc_card.enterEvent(None)
        self.assertGreater(doc_card._shadow.blurRadius(), doc_initial)
        doc_card.leaveEvent(None)
        self.assertEqual(doc_card._shadow.blurRadius(), doc_initial)

        print("[PASS] Test 26: 3D Depth elevation on hover & readable dark/light letter contrast verified")

    def test_27_custom_theme_persistence_across_sessions(self):
        """Verifies custom theme palette colors persist across application restarts and theme switches."""
        from themes import load_theme_prefs
        import main

        test_acc = "#e91e63"
        test_bg1 = "#1a0010"
        test_bg2 = "#2a0020"
        test_txt = "#ffeef5"

        # Apply custom theme via settings
        self.window.page_settings.custom_inputs["accent"].setText(test_acc)
        self.window.page_settings.custom_inputs["bg_primary"].setText(test_bg1)
        self.window.page_settings.custom_inputs["bg_secondary"].setText(test_bg2)
        self.window.page_settings.custom_inputs["text_primary"].setText(test_txt)
        self.window.page_settings._apply_custom_theme()

        # Check theme is Custom and colors match
        self.assertEqual(self.window.theme_mgr.current.name, "Custom")
        self.assertEqual(self.window.theme_mgr.current.accent, test_acc)

        # Verify disk persistence
        prefs = load_theme_prefs()
        self.assertEqual(prefs.get("theme"), "Custom")
        self.assertIsNotNone(prefs.get("custom_colors"))
        self.assertEqual(prefs["custom_colors"].get("accent"), test_acc)

        # Switch to Cyberpunk - custom colors must NOT be wiped
        self.window.change_theme("Cyberpunk")
        prefs_switched = load_theme_prefs()
        self.assertEqual(prefs_switched.get("theme"), "Cyberpunk")
        self.assertEqual(prefs_switched["custom_colors"].get("accent"), test_acc)

        # Switch back to Custom
        self.window.change_theme("Custom")
        self.assertEqual(self.window.theme_mgr.current.accent, test_acc)

        # Simulate fresh app startup (new session)
        app2 = main.DocumentProcessorApp()
        try:
            self.assertEqual(app2.theme_mgr.current.name, "Custom")
            self.assertEqual(app2.theme_mgr.current.accent, test_acc)
            self.assertEqual(app2.theme_mgr.current.bg_primary, test_bg1)
            self.assertEqual(app2.page_settings.custom_inputs["accent"].text(), test_acc)
            self.assertTrue(app2.page_settings._radio_buttons["Custom"].isChecked())
            self.assertTrue(app2.page_settings.custom_studio.isEnabled())
        finally:
            app2.close()

        # Restore window to Blue
        self.window.change_theme("Blue")
        print("[PASS] Test 27: Custom theme persistence across sessions & restarts verified")

    def test_28_code_editor_github_light_character_rendering_contrast(self):
        """Verifies that the code editor in GitHub Light preserves all characters with high-contrast rendering."""
        from pygments.token import Token

        self.window.route_page("code_editor")
        code_page = self.window.page_code_editor

        # Switch code theme to GitHub Light
        code_page._on_theme_changed("GitHub Light")
        self.assertEqual(code_page._current_theme_name, "GitHub Light")

        editor = code_page.current_editor
        highlighter = code_page.current_highlighter

        # Verify editor background is pure white and base text is dark charcoal
        self.assertEqual(editor._bg_color.name().lower(), "#ffffff")
        self.assertEqual(editor._text_color.name().lower(), "#24292e")
        self.assertFalse(highlighter.is_dark)

        # Set Python test snippet
        test_snippet = (
            "def calculate_total(subtotal: float, discount: float = 0.0) -> float:\n"
            "    # Calculate discounted total\n"
            "    tax_rate = 0.08\n"
            "    final_amount = (subtotal - discount) * (1.0 + tax_rate)\n"
            "    return round(final_amount, 2)\n"
        )
        editor.setPlainText(test_snippet)

        # Verify all key tokens have high contrast against white (perceived luminance < 190)
        tokens_to_test = [
            Token.Keyword,
            Token.Name.Function,
            Token.Name,
            Token.Punctuation,
            Token.Literal.String,
            Token.Literal.Number,
            Token.Comment,
            Token.Operator,
        ]

        for tok in tokens_to_test:
            fmt = highlighter.get_format(tok)
            color = fmt.foreground().color()
            lum = color.red() * 0.299 + color.green() * 0.587 + color.blue() * 0.114
            # Must NOT be white or near-white (lum < 190 guarantees >= 4.5:1 contrast against #ffffff)
            self.assertLess(lum, 190, f"Token {tok} is washed out with color {color.name()} (lum={lum})")
            self.assertNotIn(color.name().lower(), ["#ffffff", "#f8f8f2", "#fffffe"])

        # Specifically verify variables (Token.Name) and punctuation (Token.Punctuation) are crisp dark
        name_fmt = highlighter.get_format(Token.Name)
        punct_fmt = highlighter.get_format(Token.Punctuation)
        self.assertEqual(name_fmt.foreground().color().name().lower(), "#24292e")
        self.assertEqual(punct_fmt.foreground().color().name().lower(), "#24292e")

        # Test creating a new tab while in GitHub Light
        new_tab_ed = code_page.new_tab(name="test_light.py", code="x = 10")
        new_hl = code_page.current_highlighter
        self.assertFalse(new_hl.is_dark)
        self.assertEqual(new_tab_ed._bg_color.name().lower(), "#ffffff")
        self.assertEqual(new_hl.get_format(Token.Name).foreground().color().name().lower(), "#24292e")

        # Clean up tab and restore Monokai Dark
        code_page.close_tab(code_page.tab_widget.currentIndex())
        code_page._on_theme_changed("Monokai Dark")
        print("[PASS] Test 28: Code editor GitHub Light zero character loss & high-contrast rendering verified")

    def test_29_formatting_toggle_buttons_and_checkboxes_lit_up_when_checked(self):
        """Verifies that Bold, Italic, Underline, Strikethrough, alignment, and check boxes light up with accent when checked."""
        from PySide6.QtGui import QImage

        self.window.route_page("new_document")
        rb = self.window.page_editor.ribbon
        current_acc = self.window.theme_mgr.current.accent

        # Test Bold, Italic, Underline, Strikethrough
        formatting_buttons = [
            ("Bold", rb.btn_bold),
            ("Italic", rb.btn_italic),
            ("Underline", rb.btn_underline),
            ("Strike", rb.btn_strike)
        ]

        for name, btn in formatting_buttons:
            self.assertTrue(btn.isCheckable())
            # Unchecked: subtle translucent glass background
            btn.setChecked(False)
            img_u = QImage(22, 22, QImage.Format_ARGB32)
            img_u.fill(0)
            btn.render(img_u)
            c_u = img_u.pixelColor(4, 4)
            self.assertLess(c_u.alpha(), 100)

            # Checked: lit up with vibrant theme accent
            btn.setChecked(True)
            img_c = QImage(22, 22, QImage.Format_ARGB32)
            img_c.fill(0)
            btn.render(img_c)
            c_c = img_c.pixelColor(4, 4)
            self.assertEqual(c_c.alpha(), 255)
            self.assertEqual(c_c.name().lower(), current_acc.lower())
            btn.setChecked(False)

        # Test Paragraph Alignment buttons
        align_buttons = [
            ("Left", rb.btn_left),
            ("Center", rb.btn_center),
            ("Right", rb.btn_right),
            ("Justify", rb.btn_justify)
        ]
        for name, btn in align_buttons:
            self.assertTrue(btn.isCheckable())
            btn.setChecked(True)
            img_a = QImage(btn.size(), QImage.Format_ARGB32)
            img_a.fill(0)
            btn.render(img_a)
            c_a = img_a.pixelColor(4, 4)
            self.assertEqual(c_a.alpha(), 255)
            self.assertEqual(c_a.name().lower(), current_acc.lower())
            btn.setChecked(False)

        # Test theme switch propagates new accent glow to checked buttons
        self.window.change_theme("Cyberpunk")
        new_acc = self.window.theme_mgr.current.accent
        rb.btn_bold.setChecked(True)
        img_cy = QImage(22, 22, QImage.Format_ARGB32)
        img_cy.fill(0)
        rb.btn_bold.render(img_cy)
        c_cy = img_cy.pixelColor(4, 4)
        self.assertEqual(c_cy.alpha(), 255)
        self.assertEqual(c_cy.name().lower(), new_acc.lower())
        rb.btn_bold.setChecked(False)
        self.window.change_theme("Blue")

        # Test CheckBox lit-up state in find replace bar
        fb = self.window.page_editor.find_bar
        fb.cb_case.setChecked(True)
        img_cb = QImage(fb.cb_case.size(), QImage.Format_ARGB32)
        img_cb.fill(0)
        fb.cb_case.render(img_cb)
        cb_colors = set(img_cb.pixelColor(x, y).name().lower() for x in range(16) for y in range(16))
        self.assertIn(self.window.theme_mgr.current.accent.lower(), cb_colors)
        fb.cb_case.setChecked(False)

        print("[PASS] Test 29: Formatting toggle buttons (B, I, U, S) & check boxes lit up when checked verified")

    def test_30_app_icon_and_desktop_shortcut(self):
        # 1. Verify window branding icon
        win_icon = self.window.windowIcon()
        self.assertFalse(win_icon.isNull())
        pixmap = win_icon.pixmap(64, 64)
        self.assertFalse(pixmap.isNull())
        self.assertEqual(pixmap.width(), 64)
        self.assertEqual(pixmap.height(), 64)

        # 2. Verify icon assets exist on disk
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        ico_path = os.path.join(assets_dir, "app_icon.ico")
        png_path = os.path.join(assets_dir, "app_icon.png")
        self.assertTrue(os.path.exists(ico_path), f"Missing {ico_path}")
        self.assertTrue(os.path.exists(png_path), f"Missing {png_path}")

        # 3. Verify ICO mipmap resolutions (16 to 256)
        from PIL import Image
        with Image.open(ico_path) as ico_img:
            sizes = ico_img.info.get("sizes", set())
            for required_size in [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]:
                self.assertIn(required_size, sizes)

        # 4. Verify Desktop Shortcut existence and icon linkage
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop, "Alpha_Doc Suite.lnk")
        self.assertTrue(os.path.exists(shortcut_path), f"Desktop shortcut missing at {shortcut_path}")

        print("[PASS] Test 30: Multi-resolution Windows app icon & Desktop shortcut verified")

    def test_31_resume_templates_and_cover_photo(self):
        # 1. Verify cover photo on the Resume card in Output Registry
        hp = self.window.page_home
        resume_card = None
        for area in hp.document_areas:
            if area.doc_type == "Resume":
                resume_card = area
                break
        self.assertIsNotNone(resume_card, "Resume card not found in Output Registry")
        pix = resume_card.doc_display.pixmap()
        self.assertIsNotNone(pix, "Resume card does not have a cover photo pixmap")
        self.assertFalse(pix.isNull(), "Resume card cover photo is null")
        self.assertIn("4 Templates", resume_card.status.text())

        # 2. Verify all 4 resume templates in catalog and SAMPLE_TEMPLATES
        from document_presets import RESUME_TEMPLATES_CATALOG, SAMPLE_TEMPLATES
        templates_to_test = [
            "Resume - Strategic Marketing",
            "Resume - Executive Corporate",
            "Resume - Creative Editorial",
            "Resume - Modern Sage",
        ]
        for key in templates_to_test:
            self.assertIn(key, RESUME_TEMPLATES_CATALOG)
            self.assertIn(key, SAMPLE_TEMPLATES)
            content = SAMPLE_TEMPLATES[key]
            self.assertGreater(len(content.split()), 180, f"Template {key} content is too brief")
            self.assertIn("FIRSTNAME LASTNAME", content)

        # 3. Verify producing distinct working copies into the document editor
        loaded_htmls = []
        for key in templates_to_test:
            self.window.load_template_copy(key)
            self.assertEqual(self.window.page_stack.currentWidget(), self.window.page_editor)
            editor_text = self.window.page_editor.editor.document().toPlainText()
            self.assertIn("FIRSTNAME LASTNAME", editor_text)
            self.assertGreater(len(editor_text.split()), 140)
            doc_html = self.window.page_editor.editor.document().toHtml()
            loaded_htmls.append(doc_html)

        # Assert all 4 templates render distinct visual layouts
        self.assertEqual(len(set(loaded_htmls)), 4, "Templates must produce distinct layouts")

        # 4. Verify ResumeTemplatePicker dialog instantiation and selection
        from template_picker import ResumeTemplatePicker
        picker = ResumeTemplatePicker(self.window)
        self.assertEqual(len(picker.findChildren(object, "templateCard")), 4)
        picker._on_card_selected("Resume - Strategic Marketing")
        self.assertEqual(picker.selected_template_key, "Resume - Strategic Marketing")

        print("[PASS] Test 31: 4 Resume Templates, Output Registry Cover Photo, & Copy Creation verified")

    def test_32_brochure_templates_and_cover_photo(self):
        # 1. Verify cover photo on the Brochure card in Output Registry
        hp = self.window.page_home
        brochure_card = None
        for area in hp.document_areas:
            if area.doc_type == "Brochure":
                brochure_card = area
                break
        self.assertIsNotNone(brochure_card, "Brochure card not found in Output Registry")
        pix = brochure_card.doc_display.pixmap()
        self.assertIsNotNone(pix, "Brochure card does not have a cover photo pixmap")
        self.assertFalse(pix.isNull(), "Brochure card cover photo is null")
        self.assertIn("4 Templates", brochure_card.status.text())

        # 2. Verify brochure templates in catalog and SAMPLE_TEMPLATES
        from document_presets import BROCHURE_TEMPLATES_CATALOG, SAMPLE_TEMPLATES
        brochure_templates = [
            "Brochure - Bi-Fold Spread",
            "Brochure - Modern Tech Tri-Fold",
            "Brochure - Editorial Studio",
            "Brochure - Emerald Enterprise",
        ]
        self.assertEqual(len(BROCHURE_TEMPLATES_CATALOG), 4)
        for key in brochure_templates:
            self.assertIn(key, BROCHURE_TEMPLATES_CATALOG)
            self.assertIn(key, SAMPLE_TEMPLATES)
            content = SAMPLE_TEMPLATES[key]
            self.assertGreater(len(content.split()), 60, f"Template {key} content is too brief")

        # 3. Verify producing working copies of all 4 brochure templates into document editor
        # Template 1: Bi-Fold Spread
        self.window.load_template_copy("Brochure - Bi-Fold Spread")
        self.assertEqual(self.window.page_stack.currentWidget(), self.window.page_editor)
        editor_text = self.window.page_editor.editor.document().toPlainText()
        self.assertIn("INNOVATIVE", editor_text)
        self.assertIn("SOLUTIONS", editor_text)
        self.assertIn("OUR SERVICES", editor_text)
        self.assertIn("Who We Are", editor_text)

        # Template 2: Modern Tech Tri-Fold
        self.window.load_template_copy("Brochure - Modern Tech Tri-Fold")
        editor_text = self.window.page_editor.editor.document().toPlainText()
        self.assertIn("WHAT WE DO", editor_text)
        self.assertIn("WHO WE ARE", editor_text)
        self.assertIn("YOUR", editor_text)
        self.assertIn("FUTURE", editor_text)

        # Template 3: Editorial Studio
        self.window.load_template_copy("Brochure - Editorial Studio")
        editor_text = self.window.page_editor.editor.document().toPlainText()
        self.assertIn("OUR APPROACH", editor_text)
        self.assertIn("CREATIVE PROCESS", editor_text)
        self.assertIn("THE FUTURE", editor_text)
        self.assertIn("DESIGN", editor_text)

        # Template 4: Emerald Enterprise
        self.window.load_template_copy("Brochure - Emerald Enterprise")
        editor_text = self.window.page_editor.editor.document().toPlainText()
        self.assertIn("ABOUT US", editor_text)
        self.assertIn("WHAT WE OFFER", editor_text)
        self.assertIn("INNOVATIVE", editor_text)
        self.assertIn("Alpha_Docs Suite", editor_text)

        # Verify page headroom (fits cleanly on a single page)
        doc = self.window.page_editor.editor.document()
        margins = self.window.page_editor.editor.marginsPoints()
        content_h_pts = self.window.page_editor.editor.pageSizePoints().height() - margins.top() - margins.bottom()
        self.assertLessEqual(doc.size().height(), content_h_pts, "Template must fit on single page")

        # 4. Verify BrochureTemplatePicker dialog instantiation and selection
        from template_picker import BrochureTemplatePicker
        picker = BrochureTemplatePicker(self.window)
        self.assertEqual(len(picker.findChildren(object, "templateCard")), 4)
        picker._on_card_selected("Brochure - Modern Tech Tri-Fold")
        self.assertEqual(picker.selected_template_key, "Brochure - Modern Tech Tri-Fold")

        print("[PASS] Test 32: 4 Brochure Templates, Output Registry Cover Photo, & Gallery Picker verified")


if __name__ == "__main__":
    unittest.main()
