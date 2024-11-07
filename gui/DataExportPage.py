from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QListWidget, QStackedWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QGroupBox, QGridLayout
 
def clear_layout(layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()

class DataExportPage(QWidget):
    def __init__(self, pages):
        super().__init__()
        self.pages = pages
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setMinimumSize(400, 300)  # Width: 400, Height: 300
        self.export_button = QPushButton("Show Calculated Totals")
        self.export_button.setStyleSheet("background-color: rgb(196, 214, 0); font-size: 15px; font-weight: bold;")
        self.export_button.clicked.connect(self.update)
        self.layout.addWidget(self.export_button)
        self.results_label = QLabel("Results from Trip Calculation steps:")
        self.layout.addWidget(self.results_label)

    

    def update(self):
        clear_layout(self.layout)
        self.export_button = QPushButton("Show Calculated Totals")
        self.export_button.setStyleSheet("background-color: rgb(196, 214, 0); font-size: 15px; font-weight: bold;")
        self.export_button.clicked.connect(self.update)
        self.layout.addWidget(self.export_button)
        self.results_label = QLabel("Results from Trip Calculation steps:")
        self.results_label.setStyleSheet("font-weight: bold;")

        for i, page in enumerate(self.pages):
            result = page.calculate()
            label = QLabel(f"Instance {i+1}:")
            label.setStyleSheet("font-weight: bold;")
            self.layout.addWidget(label)
            self.layout.addWidget(QLabel(f"Employee Pedestrian Trips: {result['EmpPed']}"))
            self.layout.addWidget(QLabel(f"Employee Bike Trips: {result['EmpBike']}"))
            self.layout.addWidget(QLabel(f"Employee Public Transport Trips: {result['EmpPublic']}"))
            self.layout.addWidget(QLabel(f"Employee Car Trips: {result['EmpMotor']}"))
            self.layout.addWidget(QLabel(f"Total Commercial Car Trips: {result['CommMotor']}"))

            self.layout.addWidget(QLabel(f"Visitor Pedestrian Trips: {result['VisPed']}"))
            self.layout.addWidget(QLabel(f"Visitor Bike Trips: {result['VisBike']}"))
            self.layout.addWidget(QLabel(f"Visitor Public Transport Trips: {result['VisPublic']}"))
            self.layout.addWidget(QLabel(f"Visitor Car Trips: {result['VisMotor']}"))
            
            self.layout.addWidget(QLabel(f"Total Pedestrian Trips: {result['TotPed']}"))
            self.layout.addWidget(QLabel(f"Total Bike Trips: {result['TotBike']}"))
            self.layout.addWidget(QLabel(f"Total Public Transport Trips: {result['TotPublic']}"))
            self.layout.addWidget(QLabel(f"Total Car Trips: {result['TotMotor']}"))

            
