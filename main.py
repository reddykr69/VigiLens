import sys
from PyQt5.QtWidgets import QApplication
from gui.login_window import LoginWindow
from gui.dashboard_window import DashboardWindow

def main():
    app = QApplication(sys.argv)

    dashboard = DashboardWindow()

    def on_login_success():
        dashboard.show()

    login = LoginWindow(on_login_success)
    login.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()