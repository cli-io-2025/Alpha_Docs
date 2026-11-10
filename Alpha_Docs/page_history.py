from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QListWidget, QListWidgetItem, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, Signal
import json
import os
import time

class HistoryPage(QWidget):
    document_restored = Signal(str, str) # title, content

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("pageContainer")
        
        # Load history
        self.history_dir = os.path.join(os.path.dirname(__file__), "history_data")
        os.makedirs(self.history_dir, exist_ok=True)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        self.card_frame = QFrame()
        self.card_frame.setObjectName("infoCard")
        root_layout = QVBoxLayout(self.card_frame)
        root_layout.setContentsMargins(24, 24, 24, 24)
        
        title = QLabel("Document History & Backups")
        title.setObjectName("pageTitle")
        root_layout.addWidget(title)
        
        self.list_widget = QListWidget()
        self.list_widget.setObjectName("modelOutputArea")
        self.list_widget.itemDoubleClicked.connect(self._on_item_double_clicked)
        root_layout.addWidget(self.list_widget)
        
        btn_layout = QHBoxLayout()
        self.btn_restore = QPushButton("Restore Selected")
        self.btn_restore.setObjectName("modelButton")
        self.btn_restore.clicked.connect(self._on_restore_clicked)
        
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.setObjectName("navButton")
        self.btn_delete.clicked.connect(self._on_delete_clicked)
        
        btn_layout.addWidget(self.btn_restore)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addStretch()
        
        root_layout.addLayout(btn_layout)
        main_layout.addWidget(self.card_frame)
        
        self.refresh_list()
        
    def save_document(self, title: str, content: str, is_autosave: bool = False):
        safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ' or c=='_']).rstrip()
        if not safe_title:
            safe_title = "Untitled"
        filename = f"{int(time.time())}_{safe_title}.json"
        filepath = os.path.join(self.history_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "title": title,
                "content": content,
                "is_autosave": is_autosave,
                "timestamp": time.time()
            }, f, indent=2)
            
        self.refresh_list()

    def refresh_list(self):
        self.list_widget.clear()
        if not os.path.exists(self.history_dir):
            return
            
        files = sorted(os.listdir(self.history_dir), reverse=True)
        for f in files:
            if f.endswith(".json"):
                filepath = os.path.join(self.history_dir, f)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        display = f"{'[AUTO] ' if data.get('is_autosave') else ''}{data.get('title')} - {time.ctime(data.get('timestamp'))}"
                        item = QListWidgetItem(display)
                        item.setData(Qt.ItemDataRole.UserRole, filepath)
                        self.list_widget.addItem(item)
                except Exception:
                    pass
                    
    def _on_item_double_clicked(self, item):
        self._restore(item)
        
    def _on_restore_clicked(self):
        item = self.list_widget.currentItem()
        if item:
            self._restore(item)
            
    def _restore(self, item):
        filepath = item.data(Qt.ItemDataRole.UserRole)
        if not filepath:
            return
        canonical_target = os.path.realpath(filepath)
        canonical_dir = os.path.realpath(self.history_dir)
        if os.path.commonpath([canonical_target, canonical_dir]) != canonical_dir or not os.path.exists(canonical_target):
            QMessageBox.warning(self, "Error", "Invalid history file location.")
            return

        try:
            with open(canonical_target, 'r', encoding='utf-8') as file:
                data = json.load(file)
                title = data.get('title') or "Untitled"
                content = data.get('content') or ""
                self.document_restored.emit(title, content)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to restore: {e}")

    def _on_delete_clicked(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        filepath = item.data(Qt.ItemDataRole.UserRole)
        if not filepath:
            return

        canonical_target = os.path.realpath(filepath)
        canonical_dir = os.path.realpath(self.history_dir)
        if os.path.commonpath([canonical_target, canonical_dir]) != canonical_dir or not os.path.exists(canonical_target):
            QMessageBox.warning(self, "Error", "Invalid history file location.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to permanently delete this backup?\n\n{item.text()}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(canonical_target)
                self.refresh_list()
            except Exception as e:
                QMessageBox.warning(self, "Delete Failed", f"Could not remove backup file: {e}")
