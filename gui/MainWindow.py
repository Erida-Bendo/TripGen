from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QListWidget, QStackedWidget, QScrollArea
from PyQt5 import QtGui
from gui.InitializationPage import InitializationPage
from gui.DataExportPage import DataExportPage
from gui.TripCalculationPage import TripCalculationPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TripGen")
        self.setWindowIcon(QtGui.QIcon('resources/logo.png'))

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        self.central_widget = QWidget()
        scroll_area.setWidget(self.central_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(500)
        scroll_area.setMinimumWidth(1000)
        self.setCentralWidget(scroll_area)

        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.sidebar = QListWidget()
        self.sidebar.addItems(["Initialization"])
        self.sidebar.currentRowChanged.connect(self.display_content)
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("background-color: rgb(196, 214, 0); color: white; font-weight: bold;")

        self.stack = QStackedWidget()
        self.init_page = InitializationPage()
        self.init_page.continue_button.clicked.connect(self.go_to_trip_calculation )
        self.stack.addWidget(self.init_page)

        self.trip_pages = []
        self.results = []

        self.layout.addWidget(self.sidebar)
        self.layout.addWidget(self.stack)
        self.setStyleSheet("background-color: white;")

    def display_content(self, i):
        self.stack.setCurrentIndex(i)

    def go_to_trip_calculation(self):
        num_instances = int(self.init_page.instances_combo.currentText())
        for i in range(num_instances):
            trip_page = TripCalculationPage(i + 1) 
            self.central_widget.setFixedHeight(2000)
            trip_page.calculate_button.clicked.connect(lambda _, page=trip_page: self.calculate_trip(page))
            self.trip_pages.append(trip_page)
            self.stack.addWidget(trip_page)
            self.sidebar.addItem(f"Trip Calculation {i + 1}")
        self.sidebar.addItem("Data Export")
        data_export_page = DataExportPage(self.trip_pages)
        self.stack.addWidget(data_export_page)
        self.stack.setCurrentIndex(1)

    def calculate_trip(self, page):
        result = page.calculate()
        self.results.append(result)
        