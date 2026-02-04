import os
import sys
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QFileDialog, QMessageBox, QFrame, QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

class TreeGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Tree Generator PRO - L.DOUADI")
        self.resize(800, 850) 
        
        self.setStyleSheet("""
            QWidget { background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', sans-serif; }
            
            QFrame#AboutFrame { 
                background-color: #161b22; 
                border-radius: 15px; 
                padding: 20px; 
                border: 1px solid #30363d;
            }
            
            QLabel#Header { font-size: 30px; font-weight: bold; color: #ffffff; }
            
            
            QListWidget { 
                background-color: #010409; 
                border: 1px solid #30363d; 
                border-radius: 10px; 
                padding: 10px;
                font-size: 14px;
                min-height: 300px; 
            }
            QListWidget::item { 
                padding: 10px; 
                border-bottom: 1px solid #21262d; 
            }
            QListWidget::item:hover { background-color: #161b22; }

            QLineEdit { background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 10px; color: white; }
            QPushButton { background-color: #21262d; border-radius: 6px; padding: 10px 20px; font-weight: 600; border: 1px solid #30363d; }
            QPushButton:hover { border-color: #58a6ff; }
            QPushButton#RunBtn { background-color: #238636; color: white; font-size: 18px; border: none; }
            QPushButton#RunBtn:hover { background-color: #2ea043; }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Header
        header = QLabel("Tree Generator")
        header.setObjectName("Header")
        layout.addWidget(header, alignment=Qt.AlignCenter)

        # About Box
        about_frame = QFrame()
        about_frame.setObjectName("AboutFrame")
        about_v = QVBoxLayout(about_frame)
        about_v.addWidget(QLabel("<b>About This Tool</b>"), alignment=Qt.AlignLeft)
        about_v.addWidget(QLabel("Select folders to ignore. Checked items will not appear in the final tree.\nDesigned for clean project documentation."))
        
        self.github = QLabel("<a href='#' style='color: #58a6ff;'> My GitHub</a>")
        self.github.setCursor(QCursor(Qt.PointingHandCursor))
        self.github.mousePressEvent = lambda e: webbrowser.open("https://github.com/getsuyubi-beep")
        about_v.addWidget(self.github)
        layout.addWidget(about_frame)

        # 1. Project Folder
        layout.addWidget(QLabel("<b>1. Select Project Folder:</b>"))
        h1 = QHBoxLayout()
        self.path_in = QLineEdit()
        self.btn_in = QPushButton("Browse")
        self.btn_in.clicked.connect(self.browse_in)
        h1.addWidget(self.path_in); h1.addWidget(self.btn_in)
        layout.addLayout(h1)

        # 2. Ignore List (The Large Area)
        layout.addWidget(QLabel("<b>2. Folders to Ignore (Large View):</b>"))
        self.ignore_list = QListWidget()
        
        layout.addWidget(self.ignore_list, stretch=1) 

        # 3. Save Settings
        layout.addWidget(QLabel("<b>3. Save Settings:</b>"))
        h2 = QHBoxLayout()
        self.path_out = QLineEdit()
        self.btn_out = QPushButton("Browse")
        self.btn_out.clicked.connect(self.browse_out)
        h2.addWidget(self.path_out); h2.addWidget(self.btn_out)
        layout.addLayout(h2)

        h3 = QHBoxLayout()
        self.file_name = QLineEdit(); self.file_name.setText("project_tree.txt")
        h3.addWidget(QLabel("File Name: ")); h3.addWidget(self.file_name)
        layout.addLayout(h3)

        # Run Button
        self.run_btn = QPushButton(" GENERATE ARCHITECTURE")
        self.run_btn.setObjectName("RunBtn")
        self.run_btn.clicked.connect(self.run_process)
        layout.addWidget(self.run_btn)

        self.setLayout(layout)

   
    def browse_in(self):
        f = QFileDialog.getExistingDirectory(self, "Select Project")
        if f:
            self.path_in.setText(f)
            self.path_out.setText(f)
            self.fill_list(f)

    def browse_out(self):
        f = QFileDialog.getExistingDirectory(self, "Select Save Location")
        if f: self.path_out.setText(f)

    def fill_list(self, f):
        self.ignore_list.clear()
        try:
            dirs = [d for d in os.listdir(f) if os.path.isdir(os.path.join(f, d))]
            auto = ["node_modules", ".next", ".git", "dist", "bin", "__pycache__", "venv", "build"]
            for d in sorted(dirs):
                item = QListWidgetItem(f" Folder:  {d}")
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Checked if d in auto else Qt.Unchecked)
                self.ignore_list.addItem(item)
        except: pass

    def run_process(self):
        p, d, fn = self.path_in.text(), self.path_out.text(), self.file_name.text()
        if not p or not d: return
        
        ignore = {self.ignore_list.item(i).text().replace(" Folder:  ", "") 
                  for i in range(self.ignore_list.count()) 
                  if self.ignore_list.item(i).checkState() == Qt.Checked}

        try:
            res = self.get_tree(p, "", ignore)
            with open(os.path.join(d, fn), "w", encoding="utf-8") as f:
                f.write(f"PROJECT ARCHITECTURE\nROOT: {p}\n{'='*40}\n{res}\n{'='*40}\nBy L.DOUADI")
            QMessageBox.information(self, "Done", "Tree successfully generated!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def get_tree(self, p, ind, ign):
        out = ""
        try:
            items = sorted(os.listdir(p))
            for i in items:
                if i in ign and ind == "": continue
                fp = os.path.join(p, i)
                if os.path.isdir(fp):
                    if i in ign: continue
                    out += f"{ind}+-- [{i}]\n"
                    out += self.get_tree(fp, ind + "|   ", ign)
                else:
                    out += f"{ind}|-- {i}\n"
        except: pass
        return out

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TreeGeneratorApp()
    win.show()
    sys.exit(app.exec_())