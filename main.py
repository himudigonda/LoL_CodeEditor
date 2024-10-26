import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def run_editor():
    """Entry point to start the LightCode editor."""
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_editor()
