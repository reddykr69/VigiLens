import cv2
import sys
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout,
    QListWidget, QFileDialog,
    QComboBox, QStackedWidget,
    QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QSizePolicy
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QFont, QColor

sys.path.append("..")
from detection import ObjectDetector
from ownership import OwnershipTracker
from alert import AlertSystem

def get_available_cameras():
    available = []
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available.append(f"Camera {i}")
            cap.release()
    return available

class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VigiLens - Smart Surveillance System")
        self.showMaximized()
        self.setStyleSheet("background-color: #0F172A;")

        self.detector = ObjectDetector()
        self.tracker = OwnershipTracker()
        self.alert_system = AlertSystem()

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_frame)

        self.setup_ui()

    def setup_ui(self):
        root = QHBoxLayout()
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #1E293B;")
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(12, 20, 12, 20)
        sidebar_layout.setSpacing(8)

        logo = QLabel("VigiLens")
        logo.setFont(QFont("Arial", 20, QFont.Bold))
        logo.setStyleSheet("color: #4DB5E6;")
        logo.setAlignment(Qt.AlignCenter)

        sub = QLabel("AI Surveillance System")
        sub.setStyleSheet("color: #64748B; font-size: 11px;")
        sub.setAlignment(Qt.AlignCenter)

        self.dashboard_btn = self.nav_btn("Dashboard", True)
        self.history_btn = self.nav_btn("Alert History", False)

        self.dashboard_btn.clicked.connect(
            lambda: self.switch_page(0)
        )
        self.history_btn.clicked.connect(
            lambda: self.switch_page(1)
        )

        sidebar_layout.addWidget(logo)
        sidebar_layout.addWidget(sub)
        sidebar_layout.addSpacing(30)
        sidebar_layout.addWidget(self.dashboard_btn)
        sidebar_layout.addWidget(self.history_btn)
        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)

        # Main content area
        self.stack = QStackedWidget()
        self.stack.addWidget(self.build_dashboard_page())
        self.stack.addWidget(self.build_history_page())

        root.addWidget(sidebar)
        root.addWidget(self.stack)
        self.setLayout(root)

    def nav_btn(self, text, active):
        btn = QPushButton(text)
        btn.setFixedHeight(42)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(self.nav_style(active))
        return btn

    def nav_style(self, active):
        bg = "#2563EB" if active else "transparent"
        return f"""
            QPushButton {{
                background: {bg};
                color: white;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                padding-left: 14px;
                text-align: left;
            }}
            QPushButton:hover {{
                background: #2563EB;
            }}
        """

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)
        self.dashboard_btn.setStyleSheet(
            self.nav_style(index == 0)
        )
        self.history_btn.setStyleSheet(
            self.nav_style(index == 1)
        )
        if index == 1:
            self.update_history_stats()

    def build_dashboard_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: #0F172A;")
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Top bar
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        cam_label = QLabel("Camera:")
        cam_label.setStyleSheet(
            "color: white; font-size: 13px; font-weight: bold;"
        )

        self.camera_selector = QComboBox()
        self.camera_selector.setFixedHeight(40)
        self.camera_selector.setFixedWidth(160)
        self.camera_selector.setStyleSheet("""
            QComboBox {
                background: #1E293B;
                color: white;
                border: 1px solid #334155;
                border-radius: 8px;
                padding-left: 10px;
                font-size: 13px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background: #1E293B;
                color: white;
                selection-background-color: #2563EB;
            }
        """)
        cameras = get_available_cameras()
        self.camera_selector.addItems(
            cameras if cameras else ["No Camera Found"]
        )

        refresh_btn = self.action_btn("Refresh", "#475569")
        refresh_btn.clicked.connect(self.refresh_cameras)

        self.open_btn = self.action_btn("Open Video", "#2563EB")
        self.start_btn = self.action_btn("Start Monitoring", "#16A34A")
        self.stop_btn = self.action_btn("Stop", "#DC2626")
        self.reset_btn = self.action_btn("Reset Alert", "#D97706")

        self.open_btn.clicked.connect(self.open_video)
        self.start_btn.clicked.connect(self.start_monitoring)
        self.stop_btn.clicked.connect(self.stop_monitoring)
        self.reset_btn.clicked.connect(self.reset_alerts)

        top_bar.addWidget(cam_label)
        top_bar.addWidget(self.camera_selector)
        top_bar.addWidget(refresh_btn)
        top_bar.addStretch()
        top_bar.addWidget(self.open_btn)
        top_bar.addWidget(self.start_btn)
        top_bar.addWidget(self.stop_btn)
        top_bar.addWidget(self.reset_btn)

        # Content row
        content = QHBoxLayout()
        content.setSpacing(12)

        # Video feed
        self.video_label = QLabel(
            "Camera Feed — Click Start Monitoring"
        )
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.video_label.setStyleSheet(
            "color: #94A3B8; font-size: 15px;"
            "background-color: #1E293B;"
            "border-radius: 10px;"
        )

        # Right panel
        right = QVBoxLayout()
        right.setSpacing(12)
        right.setContentsMargins(0, 0, 0, 0)

        # Alert panel
        alert_frame = QFrame()
        alert_frame.setFixedWidth(300)
        alert_frame.setSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Expanding
        )
        alert_frame.setStyleSheet(
            "background: #1E293B; border-radius: 10px;"
        )
        alert_layout = QVBoxLayout()
        alert_layout.setContentsMargins(10, 10, 10, 10)
        alert_layout.setSpacing(8)

        alert_title = QLabel("Alert Panel")
        alert_title.setFont(QFont("Arial", 13, QFont.Bold))
        alert_title.setStyleSheet("color: white;")

        self.alert_list = QListWidget()
        self.alert_list.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.alert_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                color: white;
                border: none;
                font-size: 12px;
            }
            QListWidget::item {
                background: #DC2626;
                border-radius: 6px;
                padding: 6px;
                margin-bottom: 4px;
                color: white;
            }
        """)

        alert_layout.addWidget(alert_title)
        alert_layout.addWidget(self.alert_list)
        alert_frame.setLayout(alert_layout)

        # Object status panel
        status_frame = QFrame()
        status_frame.setFixedWidth(300)
        status_frame.setFixedHeight(180)
        status_frame.setStyleSheet(
            "background: #1E293B; border-radius: 10px;"
        )
        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(10, 10, 10, 10)
        status_layout.setSpacing(8)

        status_title = QLabel("Object Status")
        status_title.setFont(QFont("Arial", 13, QFont.Bold))
        status_title.setStyleSheet("color: white;")

        self.status_label = QLabel("No objects detected")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet(
            "color: #94A3B8; font-size: 12px;"
        )

        status_layout.addWidget(status_title)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_frame.setLayout(status_layout)

        right.addWidget(alert_frame)
        right.addWidget(status_frame)

        content.addWidget(self.video_label)
        content.addLayout(right)

        layout.addLayout(top_bar)
        layout.addLayout(content)
        page.setLayout(layout)
        return page

    def build_history_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: #0F172A;")
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Header
        header = QHBoxLayout()
        title = QLabel("Alert History")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: white;")

        clear_btn = self.action_btn("Clear History", "#DC2626")
        clear_btn.setFixedWidth(150)
        clear_btn.clicked.connect(self.clear_history)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(clear_btn)

        # Stats
        stats = QHBoxLayout()
        stats.setSpacing(16)
        self.total_label = self.stat_card("Total Alerts", "0")
        self.today_label = self.stat_card("Today", "0")
        self.last_label = self.stat_card("Last Object", "-")
        stats.addWidget(self.total_label[0])
        stats.addWidget(self.today_label[0])
        stats.addWidget(self.last_label[0])
        stats.addStretch()

        # Table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels([
            "Time", "Object Type", "Camera", "Status"
        ])
        self.history_table.horizontalHeader(
        ).setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setStyleSheet("""
            QTableWidget {
                background: #1E293B;
                color: white;
                border-radius: 10px;
                font-size: 13px;
                gridline-color: #334155;
                border: none;
            }
            QHeaderView::section {
                background: #0F172A;
                color: #4DB5E6;
                font-weight: bold;
                padding: 10px;
                border: none;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget::item:alternate {
                background: #243044;
            }
            QTableWidget::item:selected {
                background: #2563EB;
            }
        """)

        layout.addLayout(header)
        layout.addLayout(stats)
        layout.addWidget(self.history_table)
        page.setLayout(layout)
        return page

    def stat_card(self, label, value):
        frame = QFrame()
        frame.setFixedSize(170, 85)
        frame.setStyleSheet(
            "background: #1E293B; border-radius: 10px;"
        )
        fl = QVBoxLayout()
        fl.setContentsMargins(10, 8, 10, 8)

        val = QLabel(value)
        val.setFont(QFont("Arial", 24, QFont.Bold))
        val.setStyleSheet("color: #4DB5E6;")
        val.setAlignment(Qt.AlignCenter)

        lbl = QLabel(label)
        lbl.setStyleSheet("color: #94A3B8; font-size: 11px;")
        lbl.setAlignment(Qt.AlignCenter)

        fl.addWidget(val)
        fl.addWidget(lbl)
        frame.setLayout(fl)
        return frame, val

    def action_btn(self, text, color):
        btn = QPushButton(text)
        btn.setFixedHeight(40)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {color};
                color: white;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                padding: 0 14px;
            }}
            QPushButton:hover {{ opacity: 0.85; }}
        """)
        return btn

    def refresh_cameras(self):
        self.camera_selector.clear()
        cameras = get_available_cameras()
        self.camera_selector.addItems(
            cameras if cameras else ["No Camera Found"]
        )

    def open_video(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Video File", "",
            "Video Files (*.mp4 *.avi *.mkv)"
        )
        if path:
            if self.cap:
                self.cap.release()
            self.cap = cv2.VideoCapture(path)

    def start_monitoring(self):
        if self.cap:
            self.cap.release()
        selected = self.camera_selector.currentText()
        if "No Camera" not in selected:
            idx = int(selected.split(" ")[1])
            self.cap = cv2.VideoCapture(idx)
        else:
            self.cap = cv2.VideoCapture(0)
        self.timer.start(30)

    def stop_monitoring(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        self.video_label.setText(
            "Camera Feed — Click Start Monitoring"
        )

    def reset_alerts(self):
        self.alert_system.reset()
        self.alert_list.clear()
        self.tracker.abandoned_timers.clear()
        self.status_label.setText("No objects detected")

    def clear_history(self):
        self.history_table.setRowCount(0)
        self.alert_system.alert_log.clear()
        self.today_label[1].setText("0")
        self.total_label[1].setText("0")
        self.last_label[1].setText("-")

    def update_history_stats(self):
        total = len(self.alert_system.alert_log)
        self.total_label[1].setText(str(total))
        self.today_label[1].setText(str(total))
        if self.alert_system.alert_log:
            self.last_label[1].setText(
                self.alert_system.alert_log[-1]["object"].title()
            )

    def add_to_history(self, entry, camera):
        row = self.history_table.rowCount()
        self.history_table.insertRow(row)
        items = [
            entry["time"],
            entry["object"].title(),
            camera,
            "Alert"
        ]
        for col, text in enumerate(items):
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)
            if col == 3:
                item.setForeground(QColor("#DC2626"))
            self.history_table.setItem(row, col, item)

    def process_frame(self):
        if self.cap is None:
            return
        ret, frame = self.cap.read()
        if not ret:
            self.stop_monitoring()
            return

        persons, bags = self.detector.detect(frame)
        alerts = self.tracker.check_abandonment(bags, persons)

        for person in persons:
            frame = self.alert_system.draw_person(frame, person)
        for bag in bags:
            frame = self.alert_system.draw_normal(frame, bag)
        for alert_info in alerts:
            frame = self.alert_system.draw_alert(
                frame, alert_info["bag"], alert_info["elapsed"]
            )
            entry = self.alert_system.log_alert(alert_info["bag"])
            self.alert_list.addItem(
                f"{entry['time']} — {entry['object'].title()} ALERT"
            )
            self.add_to_history(
                entry, self.camera_selector.currentText()
            )

        if bags:
            txt = ""
            for bag in bags:
                txt += (
                    f"Object: {bag['label'].title()}\n"
                    f"Confidence: {bag['conf']:.2f}\n\n"
                )
            self.status_label.setText(txt)
        else:
            self.status_label.setText("No objects detected")

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.video_label.setPixmap(
            QPixmap.fromImage(img).scaled(
                self.video_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )