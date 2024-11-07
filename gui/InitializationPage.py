from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QListWidget, QStackedWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton


class InitializationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.instances_label = QLabel("How many instances do you need to calculate?")
        layout.addWidget(self.instances_label)

        self.instances_combo = QComboBox()
        self.instances_combo.addItems([str(i) for i in range(1, 16)])
        layout.addWidget(self.instances_combo)

        self.continue_button = QPushButton("Continue")
        self.continue_button.clicked.connect(self.freeze_page)
        layout.addWidget(self.continue_button)

    def freeze_page(self):
        self.continue_button.setDisabled(True)