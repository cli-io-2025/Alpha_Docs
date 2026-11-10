"""
document_io.py — Enterprise Multi-Format Import / Export Engine for Alpha Docs
Supports exporting and importing PDF, Markdown (with rich formatting), HTML5, and Plain Text,
plus a unified modern Export Dialog.
"""

import os
import re
from PySide6.QtCore import QMarginsF, Qt
from PySide6.QtGui import (
    QTextDocument, QTextCursor, QPageLayout, QFont,
    QTextBlock, QTextFragment
)
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton,
    QButtonGroup, QPushButton, QFileDialog, QMessageBox, QFrame
)

try:
    import docx
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False


class DocumentIOEngine:
    """Document Import / Export Engine."""

    @staticmethod
    def export_pdf(doc: QTextDocument, file_path: str, margin_in: float = 1.0) -> bool:
        """Exports the document to a PDF file using high-resolution QPrinter."""
        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(file_path)
            printer.setPageMargins(
                QMarginsF(margin_in, margin_in, margin_in, margin_in),
                QPageLayout.Unit.Inch
            )
            doc.print_(printer)
            return True
        except Exception as e:
            print(f"[DocumentIOEngine] PDF Export failed: {e}")
            return False

    @staticmethod
    def export_html(doc: QTextDocument, file_path: str) -> bool:
        """Exports document to styled, standalone HTML5."""
        try:
            body_html = doc.toHtml()
            # Wrap in clean responsive HTML template
            styled_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Alpha Docs Document</title>
<style>
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
    max-width: 850px;
    margin: 40px auto;
    padding: 0 20px;
    color: #24292e;
    background-color: #fafbfc;
  }}
  .document-card {{
    background: #ffffff;
    border: 1px solid #e1e4e8;
    border-radius: 8px;
    padding: 48px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 16px 0;
  }}
  th, td {{
    border: 1px solid #dfe2e5;
    padding: 8px 12px;
  }}
  blockquote {{
    border-left: 4px solid #00adb5;
    padding-left: 16px;
    color: #586069;
    margin-left: 0;
  }}
  img {{
    max-width: 100%;
    border-radius: 4px;
  }}
</style>
</head>
<body>
<div class="document-card">
{body_html}
</div>
</body>
</html>
"""
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(styled_html)
            return True
        except Exception as e:
            print(f"[DocumentIOEngine] HTML Export failed: {e}")
            return False

    @staticmethod
    def export_plain_text(doc: QTextDocument, file_path: str) -> bool:
        """Exports clean plain text."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(doc.toPlainText())
            return True
        except Exception as e:
            print(f"[DocumentIOEngine] Plain Text Export failed: {e}")
            return False

    @staticmethod
    def export_markdown(doc: QTextDocument, file_path: str) -> bool:
        """Converts document structure and rich formatting into clean Markdown."""
        try:
            md_lines = []
            block = doc.begin()

            while block.isValid():
                b_fmt = block.blockFormat()
                level = b_fmt.headingLevel()
                
                # Check for list
                is_list = block.textList() is not None
                list_prefix = "- " if is_list else ""

                # Build block content from fragments to capture bold, italic, links
                line_fragments = []
                it = block.begin()
                while not it.atEnd():
                    frag = it.fragment()
                    if frag.isValid():
                        text = frag.text()
                        f_fmt = frag.charFormat()
                        
                        # Style formatting
                        is_bold = f_fmt.font().bold() or f_fmt.fontWeight() >= 700
                        is_italic = f_fmt.fontItalic()
                        is_strike = f_fmt.fontStrikeOut()
                        is_link = f_fmt.isAnchor() and f_fmt.anchorHref()

                        if is_strike:
                            text = f"~~{text}~~"
                        if is_bold and is_italic:
                            text = f"***{text}***"
                        elif is_bold:
                            text = f"**{text}**"
                        elif is_italic:
                            text = f"*{text}*"

                        if is_link:
                            text = f"[{text}]({f_fmt.anchorHref()})"

                        line_fragments.append(text)
                    it += 1

                line_text = "".join(line_fragments).strip()

                if level > 0 and line_text:
                    prefix = "#" * min(level, 6)
                    md_lines.append(f"{prefix} {line_text}")
                elif is_list and line_text:
                    md_lines.append(f"{list_prefix}{line_text}")
                elif line_text:
                    md_lines.append(line_text)
                else:
                    md_lines.append("")

                block = block.next()

            md_content = "\n\n".join([l for l in md_lines if l != ""])
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(md_content + "\n")
            return True
        except Exception as e:
            print(f"[DocumentIOEngine] Markdown Export failed: {e}")
            return False

    @staticmethod
    def export_docx(doc: QTextDocument, file_path: str) -> bool:
        """Exports document to Microsoft Word (.docx) format."""
        if not HAS_DOCX:
            print("[DocumentIOEngine] python-docx is not installed. Falling back to HTML format.")
            return DocumentIOEngine.export_html(doc, file_path + ".html")
        try:
            d = docx.Document()
            block = doc.begin()
            while block.isValid():
                text = block.text()
                fmt = block.blockFormat()
                level = fmt.headingLevel()
                
                if level > 0 and text.strip():
                    d.add_heading(text, level=min(level, 3))
                elif text.strip():
                    d.add_paragraph(text)
                block = block.next()
                
            d.save(file_path)
            return True
        except Exception as e:
            print(f"[DocumentIOEngine] DOCX Export failed: {e}")
            return False

    @staticmethod
    def import_file(file_path: str, doc: QTextDocument) -> bool:
        """Imports a file (.docx, .html, .md, .txt) into the given QTextDocument."""
        if not os.path.exists(file_path):
            return False

        ext = os.path.splitext(file_path)[1].lower()
        try:
            if ext in [".html", ".htm"]:
                with open(file_path, "r", encoding="utf-8") as f:
                    doc.setHtml(f.read())
                return True
            elif ext in [".txt", ".md"]:
                with open(file_path, "r", encoding="utf-8") as f:
                    doc.setPlainText(f.read())
                return True
            elif ext == ".docx" and HAS_DOCX:
                d = docx.Document(file_path)
                paras = [p.text for p in d.paragraphs if p.text.strip()]
                doc.setPlainText("\n\n".join(paras))
                return True
            else:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    doc.setPlainText(f.read())
                return True
        except Exception as e:
            print(f"[DocumentIOEngine] Import failed: {e}")
            return False


class ExportDialog(QDialog):
    """Modern unified modal dialog for selecting output format and destination."""

    def __init__(self, doc: QTextDocument, parent=None):
        super().__init__(parent)
        self.doc = doc
        self.setWindowTitle("Export Document — Alpha Docs")
        self.setFixedWidth(400)
        self.setStyleSheet("""
            QDialog {
                background: #161920;
                color: #ffffff;
            }
            QLabel {
                color: #e0e0e0;
            }
            QRadioButton {
                color: #e0e0e0;
                font-size: 13px;
                padding: 6px;
            }
            QRadioButton::indicator:checked {
                background-color: #00adb5;
                border: 2px solid #ffffff;
                border-radius: 6px;
            }
            QPushButton {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 6px;
                color: #ffffff;
                padding: 8px 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.16);
            }
            QPushButton#btnExport {
                background: #00adb5;
                border: none;
            }
            QPushButton#btnExport:hover {
                background: #00c2cb;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        title = QLabel("Select Export Format")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #00adb5;")
        layout.addWidget(title)

        self.btn_group = QButtonGroup(self)
        self.rb_pdf = QRadioButton("📄 PDF Document (.pdf) — Publication Ready")
        self.rb_md = QRadioButton("📝 Markdown (.md) — Clean Formatted Text")
        self.rb_html = QRadioButton("🌐 HTML5 (.html) — Self-contained Web Page")
        self.rb_txt = QRadioButton("📃 Plain Text (.txt) — Raw ASCII/UTF-8")

        self.rb_pdf.setChecked(True)
        self.btn_group.addButton(self.rb_pdf, 1)
        self.btn_group.addButton(self.rb_md, 2)
        self.btn_group.addButton(self.rb_html, 3)
        self.btn_group.addButton(self.rb_txt, 4)

        layout.addWidget(self.rb_pdf)
        layout.addWidget(self.rb_md)
        layout.addWidget(self.rb_html)
        layout.addWidget(self.rb_txt)

        layout.addSpacing(10)

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(btn_cancel)

        btn_export = QPushButton("Export File…")
        btn_export.setObjectName("btnExport")
        btn_export.clicked.connect(self._do_export)
        btn_row.addWidget(btn_export)

        layout.addLayout(btn_row)

    def _do_export(self):
        selected_id = self.btn_group.checkedId()
        if selected_id == 1:
            ext_filter = "PDF Files (*.pdf)"
            default_name = "document.pdf"
            handler = DocumentIOEngine.export_pdf
        elif selected_id == 2:
            ext_filter = "Markdown Files (*.md)"
            default_name = "document.md"
            handler = DocumentIOEngine.export_markdown
        elif selected_id == 3:
            ext_filter = "HTML Files (*.html)"
            default_name = "document.html"
            handler = DocumentIOEngine.export_html
        else:
            ext_filter = "Text Files (*.txt)"
            default_name = "document.txt"
            handler = DocumentIOEngine.export_plain_text

        path, _ = QFileDialog.getSaveFileName(self, "Save Export File", default_name, ext_filter)
        if path:
            success = handler(self.doc, path)
            if success:
                QMessageBox.information(self, "Export Complete", f"Successfully exported to:\n{path}")
                self.accept()
            else:
                QMessageBox.critical(self, "Export Failed", f"Could not export file to:\n{path}")
