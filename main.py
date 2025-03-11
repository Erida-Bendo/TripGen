from PyQt5.QtWidgets import QApplication
from gui.MainWindow import MainWindow
from PyQt5.QtGui import QFont
from PyQt5 import QtCore, QtWidgets
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 9))
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())