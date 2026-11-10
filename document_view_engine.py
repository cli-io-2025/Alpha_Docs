"""
document_view_engine.py — High-Performance Custom Paged Document View Engine
Renders pages with exact margins, pagination, zoom, typography, and editing cursor.
"""
import sys
import math
from typing import Optional, Tuple

from PySide6.QtWidgets import (
    QAbstractScrollArea, QWidget, QApplication, QMenu, QInputDialog,
    QColorDialog, QFileDialog, QStyleOptionFocusRect, QStyle
)
from PySide6.QtCore import Qt, QPointF, QRectF, QSizeF, QTimer, Signal, QMarginsF, QEvent
from PySide6.QtGui import (
    QPainter, QColor, QFont, QTextDocument, QTextCursor, QTextBlockFormat,
    QTextCharFormat, QPen, QBrush, QImage, QPainterPath, QKeySequence,
    QTextListFormat, QAbstractTextDocumentLayout, QPalette, QPixmap
)
from PySide6.QtPrintSupport import QPrinter, QPrintDialog


class _Viewport(QWidget):
    """Internal viewport canvas widget for rendering pages and managing mouse/keyboard events."""

    def __init__(self, engine: 'DocumentViewEngine'):
        super().__init__()
        self.engine = engine
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, True)
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.IBeamCursor)
        self._mouse_pressed = False

    # ------------------------------------------------------------------
    # Input Events – mapping viewport coordinates to document
    # ------------------------------------------------------------------
    def _map_to_document(self, pos: QPointF) -> Optional[Tuple[int, QTextCursor]]:
        """
        Convert a viewport position (with scroll) into a document position.
        Returns (position, temporary cursor) or None if outside any page.
        """
        engine = self.engine
        scroll_x = engine.horizontalScrollBar().value()
        scroll_y = engine.verticalScrollBar().value()
        x = pos.x() + scroll_x
        y = pos.y() + scroll_y

        zoom = engine.zoomFactor()
        page_w_pts = engine.pageSizePoints().width()
        page_h_pts = engine.pageSizePoints().height()
        margins = engine.marginsPoints()
        left_m = margins.left()
        top_m = margins.top()
        right_m = margins.right()
        content_w_pts = page_w_pts - left_m - right_m
        content_h_pts = page_h_pts - top_m - margins.bottom()
        gap = engine.gapPoints()

        page_w = page_w_pts * zoom
        page_h = page_h_pts * zoom
        total_step = (page_h + gap * zoom)

        page_idx = max(0, int(y // total_step))
        needed_pages = max(1, math.ceil(engine.document().size().height() / max(1.0, content_h_pts)))
        page_count = max(engine.document().pageCount(), needed_pages)
        page_idx = min(page_idx, page_count - 1)
        
        # Check if inside the page vertically
        y_in_step = y - page_idx * total_step
        if y_in_step >= page_h:
            y_in_step = page_h - 1  # clamp to bottom of page

        # Horizontal: find page origin
        canvas_w = max(self.width(), page_w)
        page_x = (canvas_w - page_w) / 2 if engine.centerPages() else 0
        x_in_page = x - page_x
        doc_x = (x_in_page - left_m * zoom) / zoom
        y_in_content = max(0.0, min(y_in_step - top_m * zoom, content_h_pts * zoom))
        doc_y = (page_idx * content_h_pts) + (y_in_content / zoom)
        doc_x = max(0.0, min(doc_x, content_w_pts))

        doc = engine.document()
        layout = doc.documentLayout()
        hit_pos = layout.hitTest(QPointF(doc_x, doc_y), Qt.HitTestAccuracy.FuzzyHit)
        if hit_pos < 0:
            block = doc.begin()
            while block.isValid():
                rect = layout.blockBoundingRect(block)
                if doc_y <= rect.bottom() or not block.next().isValid():
                    block_layout = block.layout()
                    if block_layout and block_layout.lineCount() > 0:
                        rel_y = doc_y - rect.top()
                        for i in range(block_layout.lineCount()):
                            line = block_layout.lineAt(i)
                            line_rect = line.rect()
                            if rel_y <= line_rect.bottom() or i == block_layout.lineCount() - 1:
                                rel_x = doc_x - rect.left() - line_rect.x()
                                hit_pos = block.position() + line.xToCursor(rel_x)
                                break
                    if hit_pos < 0:
                        hit_pos = block.position()
                    break
                block = block.next()
            if hit_pos < 0:
                hit_pos = 0
                
        # Use a temporary cursor to be safe
        cursor = QTextCursor(doc)
        cursor.setPosition(hit_pos)
        return hit_pos, cursor

    # ------------------------------------------------------------------
    # Mouse handling
    # ------------------------------------------------------------------
    def mousePressEvent(self, event):
        """Map mouse clicks to the document layout to set cursor position."""
        try:
            self.engine.setFocus()
            self.setFocus()
            engine = self.engine
            
            pos = event.position()
            mapped = self._map_to_document(pos)
            if not mapped:
                return
            
            pos_in_doc, temp_cursor = mapped
            
            if event.button() == Qt.MouseButton.LeftButton:
                modifiers = event.modifiers()
                new_cursor = engine.cursor()
                if modifiers & Qt.KeyboardModifier.ShiftModifier:
                    new_cursor.setPosition(pos_in_doc, QTextCursor.MoveMode.KeepAnchor)
                else:
                    new_cursor.setPosition(pos_in_doc, QTextCursor.MoveMode.MoveAnchor)
                engine._set_cursor(new_cursor)
            elif event.button() == Qt.MouseButton.RightButton:
                new_cursor = engine.cursor()
                start = min(new_cursor.selectionStart(), new_cursor.selectionEnd())
                end = max(new_cursor.selectionStart(), new_cursor.selectionEnd())
                if not (new_cursor.hasSelection() and start <= pos_in_doc <= end):
                    new_cursor.setPosition(pos_in_doc, QTextCursor.MoveMode.MoveAnchor)
                    engine._set_cursor(new_cursor)
            
            self._mouse_pressed = True
            self._last_mouse_pos = event.position()
            event.accept()
        except Exception as e:
            import sys, traceback
            print(f"[FATAL ERROR IN MOUSE] {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    def mouseMoveEvent(self, event):
        pos = event.position()
        engine = self.engine
        zoom = engine.zoomFactor()
        page_w = engine.pageSizePoints().width() * zoom
        canvas_w = max(self.width(), page_w)
        page_x = (canvas_w - page_w) / 2 if engine.centerPages() else 0
        
        pointer = getattr(engine, "_pointer_style", "Standard I-Beam")
        if page_x <= pos.x() <= page_x + page_w:
            if pointer == "Crosshair Pointer":
                self.setCursor(Qt.CursorShape.CrossCursor)
            elif pointer == "Pointing Hand":
                self.setCursor(Qt.CursorShape.PointingHandCursor)
            elif pointer == "Arrow Pointer":
                self.setCursor(Qt.CursorShape.ArrowCursor)
            else:
                self.setCursor(Qt.CursorShape.IBeamCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

        if self._mouse_pressed and (event.buttons() & Qt.MouseButton.LeftButton):
            result = self._map_to_document(pos)
            if result:
                pos_in_doc, _ = result
                cursor = engine.cursor()
                cursor.setPosition(pos_in_doc, QTextCursor.MoveMode.KeepAnchor)
                engine._set_cursor(cursor)
                self._last_mouse_pos = event.position()
                event.accept()
                return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self._mouse_pressed:
            self._mouse_pressed = False
            self.engine.viewport().update()
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            result = self._map_to_document(event.position())
            if result:
                _, cursor = result
                cursor.select(QTextCursor.SelectionType.WordUnderCursor)
                self.engine._set_cursor(cursor)
                event.accept()
                return
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event):
        pos = event.pos()
        mapped = self._map_to_document(pos)
        if mapped:
            pos_in_doc, _ = mapped
            cursor = self.engine.cursor()
            start = min(cursor.selectionStart(), cursor.selectionEnd())
            end = max(cursor.selectionStart(), cursor.selectionEnd())
            if not (cursor.hasSelection() and start <= pos_in_doc <= end):
                cursor.setPosition(pos_in_doc, QTextCursor.MoveMode.MoveAnchor)
                self.engine._set_cursor(cursor)

        menu = QMenu(self)
        engine = self.engine

        # 0. Real-time Spelling Suggestions
        try:
            from pyspell_integration import get_shared_checker
            checker = get_shared_checker()
            if checker.is_ready:
                cur = engine.cursor()
                block = cur.block()
                pos_in_block = cur.positionInBlock()
                misspelling = checker.get_word_at_pos(block.text(), pos_in_block)
                if misspelling:
                    bad_word, suggestion, start_idx = misspelling
                    if suggestion:
                        sugg_act = menu.addAction(f"💡 Suggestion: \"{suggestion}\"")
                        def _replace_word(orig_w=bad_word, new_w=suggestion, start_p=block.position() + start_idx):
                            c = QTextCursor(engine.document())
                            c.setPosition(start_p)
                            c.setPosition(start_p + len(orig_w), QTextCursor.MoveMode.KeepAnchor)
                            c.insertText(new_w)
                            engine._set_cursor(c)
                            engine.viewport().update()
                        sugg_act.triggered.connect(_replace_word)
                    
                    add_dict = menu.addAction(f"➕ Add \"{bad_word}\" to Dictionary")
                    def _add_to_dict(w=bad_word):
                        checker.add_to_dictionary(w)
                        engine.viewport().update()
                    add_dict.triggered.connect(_add_to_dict)
                    menu.addSeparator()
        except Exception:
            pass

        # 1. Clipboard operations
        act_cut = menu.addAction("Cut")
        act_cut.setShortcut("Ctrl+X")
        act_cut.setEnabled(self.engine.cursor().hasSelection())
        act_cut.triggered.connect(self.engine.cut)

        act_copy = menu.addAction("Copy")
        act_copy.setShortcut("Ctrl+C")
        act_copy.setEnabled(self.engine.cursor().hasSelection())
        act_copy.triggered.connect(self.engine.copy)

        act_paste = menu.addAction("Paste")
        act_paste.setShortcut("Ctrl+V")
        act_paste.triggered.connect(self.engine.paste)

        menu.addSeparator()

        act_select_all = menu.addAction("Select All")
        act_select_all.setShortcut("Ctrl+A")
        act_select_all.triggered.connect(self.engine.selectAll)

        menu.addSeparator()

        # 2. Undo / Redo
        undo_action = menu.addAction("Undo")
        undo_action.triggered.connect(engine.undo)
        redo_action = menu.addAction("Redo")
        redo_action.triggered.connect(engine.redo)

        menu.addSeparator()

        # 3. Formatting
        underline_action = menu.addAction("Underline")
        underline_action.triggered.connect(lambda: engine.setUnderline(not engine.cursor().charFormat().fontUnderline()))

        highlight_action = menu.addAction("Highlight Color...")
        def _highlight():
            color = QColorDialog.getColor(Qt.GlobalColor.yellow, self, "Select Highlight Color")
            if color.isValid():
                engine.setHighlightColor(color)
        highlight_action.triggered.connect(_highlight)

        menu.addSeparator()

        # 4. Insert Link / Image
        link_action = menu.addAction("Insert Link...")
        def _link():
            url, ok = QInputDialog.getText(self, "Insert Link", "URL:")
            if ok and url:
                engine.insertLink(url, url)
        link_action.triggered.connect(_link)

        img_action = menu.addAction("Insert Image...")
        def _img():
            path, _ = QFileDialog.getOpenFileName(self, "Insert Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
            if path:
                engine.insertImage(path)
        img_action.triggered.connect(_img)

        menu.addSeparator()

        # 5. Menus (Align, Lists, Headers, Fonts)
        align_menu = menu.addMenu("Align")
        align_menu.addAction("Left", lambda: engine.setAlignment(Qt.AlignmentFlag.AlignLeft))
        align_menu.addAction("Center", lambda: engine.setAlignment(Qt.AlignmentFlag.AlignCenter))
        align_menu.addAction("Right", lambda: engine.setAlignment(Qt.AlignmentFlag.AlignRight))
        align_menu.addAction("Justify", lambda: engine.setAlignment(Qt.AlignmentFlag.AlignJustify))

        indent_menu = menu.addMenu("Indent / List")
        indent_menu.addAction("Increase Indent", engine.indentList)
        indent_menu.addAction("Decrease Indent", engine.unindentList)
        indent_menu.addAction("Numbered List", engine.toggleNumberedList)

        header_menu = menu.addMenu("Headers")
        header_menu.addAction("H1", lambda: engine.setHeaderFormat(1))
        header_menu.addAction("H2", lambda: engine.setHeaderFormat(2))
        header_menu.addAction("H3", lambda: engine.setHeaderFormat(3))
        header_menu.addAction("Normal", lambda: engine.setHeaderFormat(0))

        fonts_menu = menu.addMenu("Fonts")
        for f in ["Arial", "Courier New", "Georgia", "Helvetica", "Times New Roman", "Verdana"]:
            fonts_menu.addAction(f, lambda font=f: engine.setFontFamily(font))

        menu.addSeparator()

        # 6. Document & Print Actions
        new_doc_action = menu.addAction("New Document")
        new_doc_action.triggered.connect(lambda: engine.new_document_requested.emit())

        print_action = menu.addAction("Print...")
        def _print():
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            dialog = QPrintDialog(printer, self)
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                engine.document().print_(printer)
        print_action.triggered.connect(_print)

        menu.exec(event.globalPos())

    def keyPressEvent(self, event):
        """Forcefully forward keyboard events to the engine."""
        self.engine.keyPressEvent(event)

    # ------------------------------------------------------------------
    # Focus & Cursor
    # ------------------------------------------------------------------
    def focusInEvent(self, event):
        self.engine._cursor_blink_on = True
        self.engine._blink_timer.start()
        self.update()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.engine._cursor_blink_on = False
        self.engine._blink_timer.stop()
        self.update()
        super().focusOutEvent(event)

    def wheelEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            current_zoom = self.engine.zoomFactor()
            step = 0.1 if delta > 0 else -0.1
            new_zoom = round(max(0.2, min(current_zoom + step, 3.5)), 1)
            self.engine.setZoomFactor(new_zoom)
            event.accept()
            return
        super().wheelEvent(event)

    # ------------------------------------------------------------------
    # Input Method (stub – full IME support can be added later)
    # ------------------------------------------------------------------
    def inputMethodEvent(self, event):
        # For simplicity, we ignore composition events.
        # To fully support IME, we would need to forward to the cursor.
        pass

    def inputMethodQuery(self, query):
        return None



# ----------------------------------------------------------------------
# Main DocumentViewEngine – public API and scroll/zoom logic
# ----------------------------------------------------------------------
class DocumentViewEngine(QAbstractScrollArea):
    """
    A paged document editor widget.

    Usage:
        editor = DocumentViewEngine()
        editor.setPageSizeMM(210, 297)   # A4
        editor.setMarginsMM(25.4, 25.4, 25.4, 25.4)
        editor.setGapPoints(20)
        editor.setZoomFactor(1.0)
        layout.addWidget(editor)
    """

    # Optional signal for external status bar updates
    cursorPositionChanged = Signal(int)
    new_document_requested = Signal()
    zoom_changed = Signal(float)

    def viewportEvent(self, event):
        etype = event.type()
        if etype in (QEvent.Type.MouseButtonPress,
                       QEvent.Type.MouseButtonRelease,
                       QEvent.Type.MouseButtonDblClick,
                       QEvent.Type.MouseMove,
                       QEvent.Type.ContextMenu,
                       QEvent.Type.Wheel):
            if self._viewport:
                return self._viewport.event(event)

        if etype == QEvent.Type.Paint:
            painter = QPainter(self.viewport())
            try:
                # Use proper PySide6 enum paths to avoid AttributeError
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
                
                # --- Coordinate configuration ---
                zoom = self.zoomFactor()
                scroll_x = self.horizontalScrollBar().value()
                scroll_y = self.verticalScrollBar().value()
                
                page_w_pts = self.pageSizePoints().width()
                page_h_pts = self.pageSizePoints().height()
                
                margins = self.marginsPoints()
                left_margin = margins.left()
                top_margin = margins.top()
                content_w_pts = page_w_pts - left_margin - margins.right()
                content_h_pts = page_h_pts - top_margin - margins.bottom()
                
                page_w = page_w_pts * zoom
                page_h = page_h_pts * zoom
                gap = self.gapPoints()
                total_page_step = page_h + gap * zoom
                
                canvas_w = max(self.viewport().width(), page_w)
                if self.centerPages():
                    page_x = (canvas_w - page_w) / 2.0
                else:
                    page_x = 0.0

                # Document layout
                doc = self.document()
                needed_pages = max(1, math.ceil(doc.size().height() / max(1.0, content_h_pts)))
                page_count = max(doc.pageCount(), needed_pages)

                # Determine visible region
                clip_rect = event.rect().translated(scroll_x, scroll_y)

                # Find visible pages
                first_page = max(0, int(clip_rect.y() // total_page_step))
                last_page = min(page_count - 1,
                                int((clip_rect.bottom()) // total_page_step))
                if last_page < 0:
                    last_page = 0  # Force at least page 0 to be drawn

                # Paint each visible page
                for page_idx in range(first_page, last_page + 1):
                    page_rect = QRectF(page_x,
                                       page_idx * total_page_step,
                                       page_w,
                                       page_h)
                    if not QRectF(clip_rect).intersects(page_rect):
                        continue

                    painter.save()
                    # Apply scroll offset
                    painter.translate(-scroll_x, -scroll_y)

                    # 1. Page background and shadow
                    self._draw_page_background(painter, page_rect)
                    
                    # Draw grey split (page separator) below this page if gap > 0
                    if gap > 0:
                        split_rect = QRectF(page_x, page_rect.bottom(), page_w, gap)
                        painter.fillRect(split_rect, QColor(220, 220, 220))

                    # 2. Content area coordinates
                    content_left = page_rect.left() + left_margin * zoom
                    content_top = page_rect.top() + top_margin * zoom
                    content_screen_rect = QRectF(
                        content_left, content_top,
                        content_w_pts * zoom, content_h_pts * zoom
                    )

                    # 3. Draw the document content for this page
                    painter.save()
                    
                    # Clip to the content area on screen to prevent bleed
                    painter.setClipRect(content_screen_rect)
                    
                    # Transform: move to content origin, scale, then offset for page
                    painter.translate(content_left, content_top)
                    painter.scale(zoom, zoom)
                    painter.translate(0, -page_idx * content_h_pts)
                    
                    # Prepare paint context
                    ctx = QAbstractTextDocumentLayout.PaintContext()
                    
                    # Clip in document coordinates: this page's content slice
                    ctx.clip = QRectF(0, page_idx * content_h_pts,
                                      content_w_pts, content_h_pts)

                    # Make base/window transparent so our custom background shows, 
                    # and set text color to black so default text is visible on white pages in dark mode.
                    doc_palette = QApplication.palette()
                    doc_palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.transparent)
                    doc_palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.transparent)
                    doc_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
                    doc_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
                    ctx.palette = doc_palette
                    
                    # Suppress Qt default cursor to prevent duplicate ghost cursor
                    ctx.cursorPosition = -1
                    ctx.selections = self._get_selections()

                    doc.documentLayout().draw(painter, ctx)

                    # Draw bold custom cursor line when cursor is active and blinking
                    if getattr(self, "_cursor_blink_on", True) and not self._cursor.hasSelection():
                        self._draw_custom_cursor(painter, page_idx, content_h_pts)

                    painter.restore()

                    # 4. Page number
                    self._draw_page_number(painter, page_rect, page_idx + 1, zoom)
                    painter.restore()
            except Exception as e:
                import sys
                import traceback
                print(f"[PAINT ERROR] {e}", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
            finally:
                painter.end()
            return True
        return super().viewportEvent(event)

    def _draw_page_background(self, painter: QPainter, rect: QRectF):
        """Draw a white page with a subtle drop shadow."""
        # Shadow
        shadow_offset = 4
        shadow_color = QColor(0, 0, 0, 40)
        painter.fillRect(rect.translated(shadow_offset, shadow_offset), shadow_color)
        # Page
        painter.fillRect(rect, Qt.GlobalColor.white)
        painter.setPen(QPen(QColor(200, 200, 200), 1))
        painter.drawRect(rect)

    def _draw_page_number(self, painter: QPainter, page_rect: QRectF,
                          number: int, zoom: float):
        """Draw the page number at the bottom centre of the page."""
        font = painter.font()
        font.setPointSizeF(9 * zoom)  # scale with zoom
        painter.setFont(font)
        painter.setPen(QColor(120, 120, 120))
        text = str(number)
        flags = Qt.AlignHCenter | Qt.AlignBottom
        # Draw inside the bottom margin, close to the page edge
        margin = 8 * zoom
        rect = page_rect.adjusted(0, 0, 0, -margin)
        painter.drawText(rect, flags, text)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Document & cursor
        self._document = QTextDocument(self)
        self._document.setDocumentMargin(0)  # We handle margins in paint
        self._cursor = QTextCursor(self._document)
        self._current_char_format = QTextCharFormat()

        # Page geometry (stored in points = 1/72 inch)
        self._page_size_mm = (210.0, 297.0)   # A4
        self._margins_mm = (25.4, 25.4, 25.4, 25.4)  # 1 inch all around
        
        self._apply_page_geometry()
        
        self._gap_points = 20.0
        self._zoom_factor = 1.0
        self._center_pages = True

        # Cursor blink
        self._cursor_blink_on = True
        self._blink_timer = QTimer(self)
        self._blink_timer.timeout.connect(self._toggle_blink)
        self._blink_timer.start(500)

        # Create and set the custom viewport
        self._viewport = _Viewport(self)
        self.setViewport(self._viewport)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Listen for document changes to update scroll bars and repaint
        self._document.contentsChanged.connect(self._on_contents_changed)
        self._document.documentLayout().documentSizeChanged.connect(self._on_contents_changed)

        # Initial scroll bar setup
        self._update_scroll_bars()

    # ------------------------------------------------------------------
    # Public configuration
    # ------------------------------------------------------------------
    def document(self) -> QTextDocument:
        return self._document

    def cursor(self) -> QTextCursor:
        return self._cursor

    def setDocument(self, doc: QTextDocument):
        """Replace the whole document. The old one is deleted."""
        old_doc = self._document
        self._document = doc
        self._document.setDocumentMargin(0)
        self._cursor = QTextCursor(doc)
        old_doc.deleteLater()
        self._document.contentsChanged.connect(self._on_contents_changed)
        self._document.documentLayout().documentSizeChanged.connect(self._on_contents_changed)
        self._apply_page_geometry()
        self._update_scroll_bars()
        self.viewport().update()

    def pageSizePoints(self) -> QSizeF:
        """Page size in points (72 dpi)."""
        return QSizeF(self._mm_to_points(self._page_size_mm[0]),
                      self._mm_to_points(self._page_size_mm[1]))

    def marginsPoints(self) -> QMarginsF:
        """Margins in points."""
        return QMarginsF(self._mm_to_points(self._margins_mm[0]),
                         self._mm_to_points(self._margins_mm[1]),
                         self._mm_to_points(self._margins_mm[2]),
                         self._mm_to_points(self._margins_mm[3]))

    def setPageSizeMM(self, width_mm: float, height_mm: float):
        self._page_size_mm = (width_mm, height_mm)
        self._apply_page_geometry()
        self._update_scroll_bars()
        self.viewport().update()

    def setMarginsMM(self, left: float, top: float, right: float, bottom: float):
        self._margins_mm = (left, top, right, bottom)
        self._apply_page_geometry()
        self._update_scroll_bars()
        self.viewport().update()

    def setGapPoints(self, gap: float):
        self._gap_points = gap
        self._update_scroll_bars()
        self.viewport().update()

    def gapPoints(self) -> float:
        return self._gap_points

    def centerPages(self) -> bool:
        return self._center_pages

    def setZoomFactor(self, factor: float):
        factor = max(0.2, min(factor, 3.5))
        self._zoom_factor = factor
        self._apply_page_geometry()
        self._update_scroll_bars()
        self.viewport().update()
        self.zoom_changed.emit(self._zoom_factor)

    def zoomFactor(self) -> float:
        return self._zoom_factor

    def zoomIn(self, step: float = 0.1):
        """Increase document zoom factor by step."""
        new_zoom = round(min(3.5, self._zoom_factor + step), 2)
        self.setZoomFactor(new_zoom)

    def zoomOut(self, step: float = 0.1):
        """Decrease document zoom factor by step."""
        new_zoom = round(max(0.3, self._zoom_factor - step), 2)
        self.setZoomFactor(new_zoom)

    def resetZoom(self):
        """Reset document zoom factor to 100% (1.0)."""
        self.setZoomFactor(1.0)

    def setCenterPages(self, center: bool):
        self._center_pages = center
        self._update_scroll_bars()
        self.viewport().update()

    # ------------------------------------------------------------------
    # Search & Replace Engine
    # ------------------------------------------------------------------
    def find_text(self, text: str, forward: bool = True, match_case: bool = False, whole_word: bool = False) -> tuple[int, int]:
        """Finds text in document and selects match. Returns (current_match_index, total_matches)."""
        if not text:
            return 0, 0

        flags = QTextDocument.FindFlag(0)
        if match_case:
            flags |= QTextDocument.FindFlag.FindCaseSensitively
        if whole_word:
            flags |= QTextDocument.FindFlag.FindWholeWords

        # Count total matches in document
        total = 0
        search_cursor = QTextCursor(self._document)
        all_positions = []
        while True:
            found = self._document.find(text, search_cursor, flags)
            if found.isNull():
                break
            all_positions.append(found.selectionStart())
            search_cursor = found
            total += 1

        if total == 0:
            return 0, 0

        # Perform actual move from active cursor position
        move_flags = flags
        if not forward:
            move_flags |= QTextDocument.FindFlag.FindBackward

        start_cursor = self.cursor()
        match_cursor = self._document.find(text, start_cursor, move_flags)
        if match_cursor.isNull():
            # Wrap around
            wrap_cursor = QTextCursor(self._document)
            if not forward:
                wrap_cursor.movePosition(QTextCursor.MoveOperation.End)
            match_cursor = self._document.find(text, wrap_cursor, move_flags)

        if not match_cursor.isNull():
            self._set_cursor(match_cursor)
            pos = match_cursor.selectionStart()
            current_idx = (all_positions.index(pos) + 1) if pos in all_positions else 1
            return current_idx, total

        return 0, total

    def replace_text(self, find_str: str, replace_str: str, match_case: bool = False, whole_word: bool = False) -> bool:
        cursor = self.cursor()
        if cursor.hasSelection():
            sel_text = cursor.selectedText()
            matches = (sel_text == find_str) if match_case else (sel_text.lower() == find_str.lower())
            if matches:
                cursor.insertText(replace_str)
                self._set_cursor(cursor)
                self.find_text(find_str, forward=True, match_case=match_case, whole_word=whole_word)
                return True
        idx, _ = self.find_text(find_str, forward=True, match_case=match_case, whole_word=whole_word)
        return idx > 0

    def replace_all(self, find_str: str, replace_str: str, match_case: bool = False, whole_word: bool = False) -> int:
        count = 0
        cursor = QTextCursor(self._document)
        cursor.beginEditBlock()
        while True:
            idx, total = self.find_text(find_str, forward=True, match_case=match_case, whole_word=whole_word)
            if idx == 0 or count >= 1000:
                break
            cur = self.cursor()
            cur.insertText(replace_str)
            self._set_cursor(cur)
            count += 1
        cursor.endEditBlock()
        return count

    def get_document_statistics(self) -> dict:
        text = self._document.toPlainText()
        import re, math
        words = len(re.findall(r"\b\w+\b", text))
        chars = len(text)
        chars_no_spaces = len(text.replace(" ", "").replace("\n", ""))
        pages = max(1, self._document.pageCount())
        read_time_mins = math.ceil(words / 200.0) if words > 0 else 0
        return {
            "words": words,
            "chars": chars,
            "chars_no_spaces": chars_no_spaces,
            "pages": pages,
            "read_time_mins": read_time_mins,
            "zoom": int(self._zoom_factor * 100)
        }

    # ------------------------------------------------------------------
    # Editing helpers (formatting)
    # ------------------------------------------------------------------
    def _apply_char_format(self, fmt: QTextCharFormat):
        cursor = self.cursor()
        if cursor.hasSelection():
            cursor.mergeCharFormat(fmt)
            self._current_char_format.merge(fmt)
        else:
            self._current_char_format.merge(fmt)
            cursor.setCharFormat(self._current_char_format)
        self._set_cursor(cursor)

    def setBold(self, bold: bool):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold if bold else QFont.Normal)
        self._apply_char_format(fmt)

    def setItalic(self, italic: bool):
        fmt = QTextCharFormat()
        fmt.setFontItalic(italic)
        self._apply_char_format(fmt)

    def setUnderline(self, underline: bool):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(underline)
        self._apply_char_format(fmt)

    def setFontFamily(self, family: str):
        fmt = QTextCharFormat()
        fmt.setFontFamily(family)
        self._apply_char_format(fmt)

    def setFontSize(self, points: float):
        fmt = QTextCharFormat()
        fmt.setFontPointSize(points)
        self._apply_char_format(fmt)
        
    def setTextColor(self, color: QColor):
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        self._apply_char_format(fmt)

    def setAlignment(self, alignment: Qt.AlignmentFlag):
        block_fmt = self._cursor.blockFormat()
        block_fmt.setAlignment(alignment)
        self._cursor.mergeBlockFormat(block_fmt)
        self.viewport().update()

    def setHighlightColor(self, color: QColor):
        fmt = QTextCharFormat()
        fmt.setBackground(color)
        self._apply_char_format(fmt)

    def insertLink(self, url: str, text: str = ""):
        if not text:
            text = url
        fmt = self._cursor.charFormat()
        fmt.setAnchor(True)
        fmt.setAnchorHref(url)
        fmt.setForeground(Qt.GlobalColor.blue)
        fmt.setFontUnderline(True)
        self._cursor.insertText(text, fmt)
        
        reset_fmt = QTextCharFormat()
        self._cursor.setCharFormat(reset_fmt)
        self._set_cursor(self._cursor)

    def insertImage(self, file_path: str):
        from PySide6.QtGui import QImage
        image = QImage(file_path)
        if not image.isNull():
            self._document.addResource(QTextDocument.ResourceType.ImageResource, file_path, image)
            self._cursor.insertImage(file_path)
            self._set_cursor(self._cursor)

    def toggleBulletList(self):
        cursor = self.cursor()
        if cursor.currentList():
            block_fmt = cursor.blockFormat()
            block_fmt.setObjectIndex(-1)
            cursor.setBlockFormat(block_fmt)
        else:
            list_fmt = QTextListFormat()
            list_fmt.setStyle(QTextListFormat.Style.ListDisc)
            cursor.createList(list_fmt)
        self._set_cursor(cursor)

    def toggleNumberedList(self):
        cursor = self.cursor()
        if cursor.currentList():
            block_fmt = cursor.blockFormat()
            block_fmt.setObjectIndex(-1)
            cursor.setBlockFormat(block_fmt)
        else:
            list_fmt = QTextListFormat()
            list_fmt.setStyle(QTextListFormat.Style.ListDecimal)
            cursor.createList(list_fmt)
        self._set_cursor(cursor)

    def insertTable(self, rows: int = 3, cols: int = 3):
        cursor = self.cursor()
        cursor.insertTable(rows, cols)
        self._set_cursor(cursor)

    def indentList(self):
        cursor = self.cursor()
        block_fmt = cursor.blockFormat()
        block_fmt.setIndent(block_fmt.indent() + 1)
        cursor.setBlockFormat(block_fmt)
        self._set_cursor(cursor)

    def unindentList(self):
        cursor = self.cursor()
        block_fmt = cursor.blockFormat()
        indent = block_fmt.indent()
        if indent > 0:
            block_fmt.setIndent(indent - 1)
            cursor.setBlockFormat(block_fmt)
            self._set_cursor(cursor)

    def setHeaderFormat(self, level: int):
        cursor = self.cursor()
        block_fmt = cursor.blockFormat()
        block_fmt.setHeadingLevel(level)
        
        char_fmt = QTextCharFormat()
        if level == 1:
            char_fmt.setFontPointSize(24)
            char_fmt.setFontWeight(QFont.Bold)
        elif level == 2:
            char_fmt.setFontPointSize(18)
            char_fmt.setFontWeight(QFont.Bold)
        elif level == 3:
            char_fmt.setFontPointSize(14)
            char_fmt.setFontWeight(QFont.Bold)
        else:
            char_fmt.setFontPointSize(12)
            char_fmt.setFontWeight(QFont.Normal)
            
        cursor.setBlockFormat(block_fmt)
        cursor.setBlockCharFormat(char_fmt)
        self._set_cursor(cursor)

    # ------------------------------------------------------------------
    # Clipboard & Undo/Redo
    # ------------------------------------------------------------------
    def undo(self):
        self._document.undo()
        self._ensure_cursor_visible()
        self.viewport().update()

    def redo(self):
        self._document.redo()
        self._ensure_cursor_visible()
        self.viewport().update()

    def cut(self):
        if self._cursor.hasSelection():
            self.copy()
            self._cursor.removeSelectedText()
            self.viewport().update()

    def copy(self):
        if self._cursor.hasSelection():
            QApplication.clipboard().setText(self._cursor.selectedText())

    def paste(self):
        text = QApplication.clipboard().text()
        if text:
            self._cursor.insertText(text)
            self._ensure_cursor_visible()
            self.viewport().update()


    # ------------------------------------------------------------------
    # Internal – cursor & viewport updates
    # ------------------------------------------------------------------
    def focusInEvent(self, event):
        """Forward focus to the custom viewport to capture key events."""
        if self._viewport:
            self._viewport.setFocus()
        super().focusInEvent(event)

    def _toggle_blink(self):
        self._cursor_blink_on = not getattr(self, "_cursor_blink_on", False)
        vp = self.viewport()
        if vp:
            vp.update()

    def setCaretStyle(self, style_name: str):
        """Set active text insertion caret shape (I-Beam Line, Thick Bar, Full Block Caret, Underline Caret)."""
        self._caret_style = style_name
        self.viewport().update()

    def caretStyle(self) -> str:
        return getattr(self, "_caret_style", "I-Beam Line")

    def setPointerStyle(self, style_name: str):
        """Set active mouse pointer shape (Standard I-Beam, Crosshair Pointer, Pointing Hand, Arrow Pointer)."""
        self._pointer_style = style_name
        self.viewport().update()

    def pointerStyle(self) -> str:
        return getattr(self, "_pointer_style", "Standard I-Beam")

    def setCursorStyle(self, style_name: str):
        """Backwards compatibility method."""
        if "Pointer" in style_name or "Hand" in style_name:
            self.setPointerStyle(style_name)
        else:
            self.setCaretStyle(style_name)

    def cursorStyle(self) -> str:
        return self.caretStyle()

    def _draw_custom_cursor(self, painter: QPainter, page_idx: int, content_h_pts: float):
        """Draw custom blinking caret according to selected caret style."""
        cursor = self.cursor()
        block = cursor.block()
        if not block.isValid():
            return
        layout = self.document().documentLayout()
        b_rect = layout.blockBoundingRect(block)
        pos_in_block = cursor.position() - block.position()
        block_layout = block.layout()
        if not block_layout or block_layout.lineCount() == 0:
            return
            
        line = block_layout.lineForTextPosition(pos_in_block)
        if not line.isValid():
            return
            
        x_pos = line.cursorToX(pos_in_block)[0]
        cursor_x = b_rect.left() + x_pos
        cursor_y = b_rect.top() + line.y()

        if content_h_pts > 0 and int(cursor_y // content_h_pts) != page_idx:
            return
        cursor_h = line.height()
        if cursor_h <= 0:
            cursor_h = 14.0

        caret = getattr(self, "_caret_style", "I-Beam Line")
        cursor_color = QColor(0, 0, 0)

        if caret == "Thick Bar":
            painter.fillRect(QRectF(cursor_x, cursor_y, 4.0, cursor_h), cursor_color)
        elif caret == "Full Block Caret":
            next_pos = min(pos_in_block + 1, block.length() - 1)
            char_w = line.cursorToX(next_pos)[0] - x_pos
            if char_w <= 2.0:
                char_w = 8.0
            painter.fillRect(QRectF(cursor_x, cursor_y, char_w, cursor_h), QColor(0, 120, 215, 180))
        elif caret == "Underline Caret":
            painter.fillRect(QRectF(cursor_x, cursor_y + cursor_h - 2.5, 10.0, 2.5), cursor_color)
        else:
            # I-Beam Line
            painter.fillRect(QRectF(cursor_x, cursor_y, 2.0, cursor_h), cursor_color)

    def _set_cursor(self, cursor: QTextCursor):
        """Replace the engine cursor and update viewport."""
        self._cursor = QTextCursor(cursor)  # keep a copy
        self._cursor_blink_on = True  # reset blink state so cursor line is immediately visible
        if not self._cursor.hasSelection():
            self._current_char_format = self._cursor.charFormat()
        self.cursorPositionChanged.emit(self._cursor.position())
        self._ensure_cursor_visible()
        self.viewport().update()

    def _ensure_cursor_visible(self):
        """Scroll to make the cursor visible."""
        layout = self._document.documentLayout()
        block_rect = layout.blockBoundingRect(self._cursor.block())
        doc_y = block_rect.top()
        
        zoom = self._zoom_factor
        page_h_pts = self.pageSizePoints().height()
        margins = self.marginsPoints()
        content_h_pts = page_h_pts - margins.top() - margins.bottom()
        
        if content_h_pts <= 0: return
        
        page_idx = int(doc_y // content_h_pts)
        local_y = doc_y - page_idx * content_h_pts
        
        gap = self._gap_points
        total_step = (page_h_pts * zoom) + (gap * zoom)
        
        abs_y = page_idx * total_step + (margins.top() * zoom) + (local_y * zoom)
        
        vbar = self.verticalScrollBar()
        if abs_y < vbar.value():
            vbar.setValue(int(abs_y - 20))
        elif abs_y > vbar.value() + self.viewport().height() - 50:
            vbar.setValue(int(abs_y - self.viewport().height() + 50))

    def _on_contents_changed(self):
        """Called whenever the document changes."""
        self._update_scroll_bars()
        self.viewport().update()

    # ------------------------------------------------------------------
    # Keyboard handling
    # ------------------------------------------------------------------
    def keyPressEvent(self, event):
        """Handle basic text insertion and navigation."""
        try:
            cursor = self.cursor()
            key = event.key()
            modifiers = event.modifiers()

            # Zoom keyboard shortcuts: Ctrl + +, Ctrl + -, Ctrl + 0
            if modifiers & Qt.KeyboardModifier.ControlModifier:
                if key in (Qt.Key.Key_Plus, Qt.Key.Key_Equal):
                    self.zoomIn()
                    event.accept()
                    return
                elif key in (Qt.Key.Key_Minus, Qt.Key.Key_Underscore):
                    self.zoomOut()
                    event.accept()
                    return
                elif key == Qt.Key.Key_0:
                    self.resetZoom()
                    event.accept()
                    return

            # 1. Navigation
            move_op = None
            if key == Qt.Key_Left:
                move_op = QTextCursor.WordLeft if modifiers & Qt.ControlModifier else QTextCursor.Left
            elif key == Qt.Key_Right:
                move_op = QTextCursor.WordRight if modifiers & Qt.ControlModifier else QTextCursor.Right
            elif key == Qt.Key_Up:
                move_op = QTextCursor.Up
            elif key == Qt.Key_Down:
                move_op = QTextCursor.Down
            elif key == Qt.Key_Home:
                move_op = QTextCursor.StartOfBlock
            elif key == Qt.Key_End:
                move_op = QTextCursor.EndOfBlock
            elif key == Qt.Key_PageUp:
                move_op = QTextCursor.Up  # simplify for now
            elif key == Qt.Key_PageDown:
                move_op = QTextCursor.Down

            if move_op is not None:
                mode = QTextCursor.KeepAnchor if modifiers & Qt.ShiftModifier else QTextCursor.MoveAnchor
                cursor.movePosition(move_op, mode)
                self._set_cursor(cursor)
                event.accept()
                return

            # 2. Key Actions
            if key == Qt.Key_Backspace:
                if cursor.hasSelection():
                    cursor.removeSelectedText()
                else:
                    cursor.deletePreviousChar()
                self._set_cursor(cursor)
                event.accept()
                return
            elif key == Qt.Key_Delete:
                if cursor.hasSelection():
                    cursor.removeSelectedText()
                else:
                    cursor.deleteChar()
                self._set_cursor(cursor)
                event.accept()
                return
            elif key == Qt.Key_Return or key == Qt.Key_Enter:
                cursor.insertBlock()
                self._set_cursor(cursor)
                event.accept()
                return
            elif key == Qt.Key_Tab:
                cursor.insertText("\t")
                self._set_cursor(cursor)
                event.accept()
                return

            # Clipboard shortcuts
            if modifiers & Qt.ControlModifier:
                if key == Qt.Key_C:
                    self.copy()
                    event.accept()
                    return
                elif key == Qt.Key_X:
                    self.cut()
                    event.accept()
                    return
                elif key == Qt.Key_V:
                    self.paste()
                    event.accept()
                    return
                elif key == Qt.Key_Z:
                    self.undo()
                    event.accept()
                    return
                elif key == Qt.Key_Y:
                    self.redo()
                    event.accept()
                    return
                elif key == Qt.Key_A:
                    self.selectAll()
                    event.accept()
                    return

            # 3. Text Insertion
            text = event.text()
            if text and not (modifiers & (Qt.ControlModifier | Qt.AltModifier)):
                if cursor.hasSelection():
                    cursor.removeSelectedText()
                cursor.insertText(text, self._current_char_format)
                self._set_cursor(cursor)
                event.accept()
                return

            super().keyPressEvent(event)
        except Exception as e:
            import sys, traceback
            print(f"[ERROR in keyPressEvent] {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)



    def _update_scroll_bars(self):
        """Calculate total content size and set scroll bar ranges."""
        zoom = self._zoom_factor
        page_w = self.pageSizePoints().width() * zoom
        page_h = self.pageSizePoints().height() * zoom
        gap = self._gap_points * zoom
        total_step = page_h + gap

        margins = self.marginsPoints()
        content_h_pts = self.pageSizePoints().height() - margins.top() - margins.bottom()
        needed_pages = max(1, math.ceil(self._document.size().height() / max(1.0, content_h_pts)))
        page_count = max(self._document.pageCount(), needed_pages)
        if page_count == 0:
            self.verticalScrollBar().setRange(0, 0)
            return

        total_height = page_count * total_step - gap
        canvas_w = max(self.viewport().width(), page_w)
        if self._center_pages:
            page_x = (canvas_w - page_w) / 2.0
        else:
            page_x = 0.0

        # Vertical scroll
        viewport_h = self.viewport().height()
        max_scroll = max(0.0, total_height - viewport_h)
        vbar = self.verticalScrollBar()
        vbar.setRange(0, int(max_scroll))
        vbar.setPageStep(int(viewport_h))
        vbar.setSingleStep(20)

        # Horizontal scroll (enabled when content width exceeds viewport)
        viewport_w = self.viewport().width()
        max_h_scroll = max(0.0, page_w - viewport_w)
        hbar = self.horizontalScrollBar()
        hbar.setRange(0, int(max_h_scroll))
        hbar.setPageStep(int(viewport_w))
        hbar.setSingleStep(20)

    def resizeEvent(self, event):
        self._update_scroll_bars()
        super().resizeEvent(event)

    # ------------------------------------------------------------------
    # Internal – selection for paint context
    # ------------------------------------------------------------------
    def selectAll(self):
        cursor = self.cursor()
        cursor.select(QTextCursor.SelectionType.Document)
        self._set_cursor(cursor)

    def _get_selections(self):
        """Return a list of QAbstractTextDocumentLayout.Selection objects."""
        selections = []
        if self._cursor.hasSelection():
            sel = QAbstractTextDocumentLayout.Selection()
            sel.cursor = QTextCursor(self._cursor)
            # High-contrast vivid blue selection highlight for clear visibility
            fmt = QTextCharFormat()
            fmt.setBackground(QColor(0, 120, 215, 180))
            fmt.setForeground(QColor(255, 255, 255))
            sel.format = fmt
            selections.append(sel)
        return selections

    def _update_viewport(self):
        """Force a repaint of the viewport."""
        self.viewport().update()

    # ------------------------------------------------------------------
    # Conversion helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _mm_to_points(mm: float) -> float:
        """Convert millimetres to points (1 point = 1/72 inch, 1 inch = 25.4 mm)."""
        return mm * 72.0 / 25.4

    def _content_size_points(self) -> QSizeF:
        """Return the size of the content area (page minus margins) in points."""
        pw = self._mm_to_points(self._page_size_mm[0])
        ph = self._mm_to_points(self._page_size_mm[1])
        left = self._mm_to_points(self._margins_mm[0])
        top = self._mm_to_points(self._margins_mm[1])
        right = self._mm_to_points(self._margins_mm[2])
        bottom = self._mm_to_points(self._margins_mm[3])
        return QSizeF(pw - left - right, ph - top - bottom)

    def _apply_page_geometry(self):
        """Set the document's page size and text width from current page/margin settings.
        
        pageSize height must equal the CONTENT height (page minus top+bottom
        margins) so that QTextDocument's pagination aligns with the paint
        code's per-page vertical offsets.  textWidth is the content width
        so lines wrap at the right margin.
        """
        content = self._content_size_points()
        # pageSize height = content height so pagination matches paint slicing
        self._document.setPageSize(QSizeF(content.width(), content.height()))
        self._document.setTextWidth(content.width())

    # ------------------------------------------------------------------
    # Filmstrip Navigation & Live Page Thumbnails
    # ------------------------------------------------------------------
    def get_all_page_thumbnails(self, target_h: int = 46) -> list:
        """Generates thumbnails for all pages of the document."""
        self._apply_page_geometry()
        page_count = max(1, self._document.pageCount())
        content_w = max(1.0, self.pageSizePoints().width())
        content_h = max(1.0, self.pageSizePoints().height())
        target_w = max(32, int(target_h * (content_w / content_h)))

        thumbnails = []
        for page_idx in range(page_count):
            pm = QPixmap(target_w, target_h)
            pm.fill(QColor(255, 255, 255))
            p = QPainter(pm)
            p.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Draw subtle page border
            p.setPen(QColor(200, 200, 200))
            p.drawRect(0, 0, target_w - 1, target_h - 1)

            scale_x = (target_w - 4) / content_w
            scale_y = (target_h - 4) / content_h
            p.translate(2, 2)
            p.scale(scale_x, scale_y)
            p.translate(0, -page_idx * content_h)

            ctx = QAbstractTextDocumentLayout.PaintContext()
            ctx.clip = QRectF(0, page_idx * content_h, content_w, content_h)
            self._document.documentLayout().draw(p, ctx)
            p.end()
            thumbnails.append(pm)

        return thumbnails

    def current_page_index(self) -> int:
        """Estimates the 0-based page index currently in the upper visible viewport."""
        zoom = self._zoom_factor
        page_h_pts = self.pageSizePoints().height() * zoom
        gap = self._gap_points * zoom
        total_step = max(1.0, page_h_pts + gap)
        scroll_y = self.verticalScrollBar().value()
        return max(0, int((scroll_y + 80) // total_step))

    def scroll_to_page(self, page_idx: int) -> None:
        """Smoothly scrolls canvas to the specified 0-based page index."""
        zoom = self._zoom_factor
        page_h_pts = self.pageSizePoints().height() * zoom
        gap = self._gap_points * zoom
        total_step = page_h_pts + gap
        target_y = int(page_idx * total_step)
        self.verticalScrollBar().setValue(target_y)