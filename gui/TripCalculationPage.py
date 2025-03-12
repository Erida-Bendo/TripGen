from PyQt5.QtWidgets import  QWidget, QCheckBox, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QGroupBox, QFrame, QGridLayout, QTableView, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractScrollArea
from helper_functions.projectSite  import Site
from helper_functions.tripProp import tripProp
from helper_functions.propCheck import propBounds
from helper_functions.hourlyGraphFunct import load_excel, table_view_to_dataframe, calculateDataForGraph
from helper_functions.pandasModel import PandasModel
from gui.GraphWindow import GraphWindow


datasetPath="./resources/Trip Generation Old Tool.xlsm"
datasetSheet="NF-Sets"

class TripCalculationPage(QWidget):
    def __init__(self, instance_number):
        super().__init__()
        self.instance_number = instance_number
        self.initUI()
    

    def initUI(self):
        
        

        layout = QVBoxLayout()  # Single vertical layout for all widgets
        self.setLayout(layout)
        
        self.input_box = QGroupBox(f"Site properties for Instance {self.instance_number}")
        self.input_box.setObjectName("input_box")
        self.input_box.setStyleSheet("#input_box {background-color: white; border: 3px solid rgb(196, 214, 0); font-size: 18px; font-weight: bold; border-radius: 6px; margin-top: 12px;} QGroupBox::title {subcontrol-origin: margin; left: 3px; padding: 0px 0px 5px 0px;}")
        box_layout = QVBoxLayout()
        self.input_box.setLayout(box_layout)

        self.category = QComboBox()
        self.category.addItems(["BüroNutzung", "Discounter", "kleinfl. Einzelhandel", "Einkaufszentrum", "großfl. Einzelhandel", "Getränkemarkt", "Möbelmarkt", "Logistikzentrum",
                                "Baumarkt", "Handwerksbetrieb", "Autohaus", "Produktionsbetrieb", "Lagerhaus", "Dienstleistungsbetrieb", "Fitnesscenter", "Sport und Freizeit",
                                "Fastfood", "Restaurant", "Hotel", "Tankstelle", "Wohnen", "Wohnen (in ha)"])
        box_layout.addWidget(QLabel("Category:"))
        box_layout.addWidget(self.category)

        self.area = QLineEdit()
        box_layout.addWidget(QLabel("Area (m2)"))
        box_layout.addWidget(self.area)
        

        self.employeeRate = QLineEdit()
        box_layout.addWidget(QLabel("1 Employee per ______ m2"))
        box_layout.addWidget(self.employeeRate)
        self.employee_value = QLabel("")
        self.employee_value.setStyleSheet("background-color: rgb(196, 214, 0)")
        self.employee_value.hide()
        box_layout.addWidget(self.employee_value)

        self.visitorRate = QLineEdit()
        box_layout.addWidget(QLabel("Visitor per 1 m2"))
        box_layout.addWidget(self.visitorRate)
        self.visitor_value = QLabel("")
        self.visitor_value.setStyleSheet("background-color: rgb(196, 214, 0)")
        self.visitor_value.hide()
        box_layout.addWidget(self.visitor_value)

        self.trip_box = QGroupBox(f"Trip properties for Instance {self.instance_number}")
        self.trip_box.setObjectName("trip_box")
        self.trip_box.setStyleSheet("#trip_box {background-color: white; border: 3px solid rgb(196, 214, 0); font-size: 18px; font-weight: bold; border-radius: 6px; margin-top: 12px;} QGroupBox::title {subcontrol-origin: margin; left: 3px; padding: 0px 0px 5px 0px;}")
        
        trip_layout=QVBoxLayout()

        # Create layout with proper spacing and margins
        trip_layout = QVBoxLayout()
        
        self.trip_box.setLayout(trip_layout)

        self.freqEmployee = QLineEdit()
        trip_layout.addWidget(QLabel("Ways per Employee"))
        trip_layout.addWidget(self.freqEmployee)
        self.freqEmployee_value = QLabel("")
        self.freqEmployee_value.setStyleSheet("background-color: rgb(196, 214, 0)")
        self.freqEmployee_value.hide()
        trip_layout.addWidget(self.freqEmployee_value)

        self.freqVisitor = QLineEdit()
        trip_layout.addWidget(QLabel("Ways per Visitor"))
        trip_layout.addWidget(self.freqVisitor)
        self.freqVisitor_value = QLabel("")
        self.freqVisitor_value.setStyleSheet("background-color: rgb(196, 214, 0)")
        self.freqVisitor_value.hide()
        trip_layout.addWidget(self.freqVisitor_value)

        ##########################
        Empfrac_widget = QWidget()

        Empfrac_frame = QFrame()
        Empfrac_frame.setFrameShape(QFrame.StyledPanel)
        Empfrac_frame.setFrameShadow(QFrame.Raised)

        Empfrac_layout = QGridLayout(Empfrac_frame)

        
        trip_layout.addWidget(QLabel("Means Share for Employees (0.1 - 0.9)"))

        EmpFracPed_label = QLabel('Pedestrian')
        EmpFracPed_label.setFixedWidth(80)
        self.pedShareEmployee = QLineEdit()
        self.pedShareEmployee.setFixedWidth(50)

        Empfrac_layout.addWidget(EmpFracPed_label, 0,0)
        Empfrac_layout.addWidget(self.pedShareEmployee, 0,1)

        Empfrac_widget.setLayout(Empfrac_layout)

        EmpFracBike_label = QLabel('Bike')
        EmpFracBike_label.setFixedWidth(30)
        self.bikeShareEmployee = QLineEdit()
        self.bikeShareEmployee.setFixedWidth(50)

        Empfrac_layout.addWidget(EmpFracBike_label, 0,2)
        Empfrac_layout.addWidget(self.bikeShareEmployee, 0,3)

        EmpFracBus_label = QLabel('Bus')
        EmpFracBus_label.setFixedWidth(30)
        self.publicShareEmployee = QLineEdit()
        self.publicShareEmployee.setFixedWidth(50)

        Empfrac_layout.addWidget(EmpFracBus_label, 0,4)
        Empfrac_layout.addWidget(self.publicShareEmployee, 0,5)

        EmpFracMotor_label = QLabel('Private Vehicle')
        EmpFracMotor_label.setFixedWidth(120)
        self.motorEmployee = QLineEdit()
        self.motorEmployee.setFixedWidth(50)

        Empfrac_layout.addWidget(EmpFracMotor_label, 0,6)
        Empfrac_layout.addWidget(self.motorEmployee, 0,7)
        self.motorEmployee_value = QLabel("")
        self.motorEmployee_value.setStyleSheet("background-color: rgb(196, 214, 0)")
        self.motorEmployee_value.hide()
        Empfrac_layout.addWidget(self.motorEmployee_value, 1,7)
        
        trip_layout.addWidget(Empfrac_widget)


        self.pedShareVisitor = QLineEdit()
        trip_layout.addWidget(QLabel("Means Share for Visitors (0.1 - 0.9)"))

        ########
        Visfrac_widget = QWidget()

        Visfrac_frame = QFrame()
        Visfrac_frame.setFrameShape(QFrame.StyledPanel)
        Visfrac_frame.setFrameShadow(QFrame.Raised)

        Visfrac_layout = QGridLayout(Visfrac_frame)

        VisFracPed_label = QLabel('Pedestrian')
        VisFracPed_label.setFixedWidth(80)
        self.pedShareVisitor = QLineEdit()
        self.pedShareVisitor.setFixedWidth(50)

        Visfrac_layout.addWidget(VisFracPed_label, 0,0)
        Visfrac_layout.addWidget(self.pedShareVisitor, 0,1)

        Visfrac_widget.setLayout(Visfrac_layout)

        VisFracBike_label = QLabel('Bike')
        VisFracBike_label.setFixedWidth(20)
        self.bikeShareVisitor = QLineEdit()   
        self.bikeShareVisitor.setFixedWidth(50)

        Visfrac_layout.addWidget(VisFracBike_label, 0,2)
        Visfrac_layout.addWidget(self.bikeShareVisitor, 0,3)

        VisFracBus_label = QLabel('Bus')
        VisFracBus_label.setFixedWidth(20)
        self.publicShareVisitor = QLineEdit()
        self.publicShareVisitor.setFixedWidth(50)

        Visfrac_layout.addWidget(VisFracBus_label, 0,4)
        Visfrac_layout.addWidget(self.publicShareVisitor, 0,5)

        VisFracMotor_label = QLabel('Private Vehicle')
        VisFracMotor_label.setFixedWidth(120)
        self.motorVisitor = QLineEdit()
        self.motorVisitor.setFixedWidth(50)

        Visfrac_layout.addWidget(VisFracMotor_label, 0,6)
        Visfrac_layout.addWidget(self.motorVisitor, 0,7)

        self.motorVisitor_value = QLabel("")
        self.motorVisitor_value.setStyleSheet("background-color: rgb(196, 214, 0)")
        self.motorVisitor_value.hide()
        Visfrac_layout.addWidget(self.motorVisitor_value, 1,7)

        
        trip_layout.addWidget(Visfrac_widget)


        ########

        self.vehiclesEmployee = QLineEdit()
        trip_layout.addWidget(QLabel("Employee per Private Vehicle"))
        trip_layout.addWidget(self.vehiclesEmployee)
        self.vehiclesEmployee_value = QLabel("")
        self.vehiclesEmployee_value.setStyleSheet("background-color: rgb(196, 214, 0)")
        self.vehiclesEmployee_value.hide()
        trip_layout.addWidget(self.vehiclesEmployee_value)

        self.vehiclesVisitor = QLineEdit()
        trip_layout.addWidget(QLabel("Visitor per Private Vehicle"))
        trip_layout.addWidget(self.vehiclesVisitor)
        self.vehiclesVisitor_value = QLabel("")
        self.vehiclesVisitor_value.setStyleSheet("background-color: rgb(196, 214, 0)")
        self.vehiclesVisitor_value.hide()
        trip_layout.addWidget(self.vehiclesVisitor_value)

        self.commercial = QLineEdit()
        trip_layout.addWidget(QLabel("Commercial Trips per 100 m2"))
        trip_layout.addWidget(self.commercial)
        self.commercial_value = QLabel("")
        self.commercial_value.setStyleSheet("background-color: rgb(196, 214, 0)")
        self.commercial_value.hide()
        trip_layout.addWidget(self.commercial_value)
        self.trip_box.adjustSize()

        self.effects_box = QGroupBox(f"Effects for Instance {self.instance_number}")
        self.effects_box.setMinimumWidth(350)
        self.effects_box.setObjectName("effects_box")
        self.effects_box.setStyleSheet("#effects_box {background-color: white; border: 3px solid rgb(196, 214, 0); font-size: 18px; font-weight: bold; border-radius: 6px; margin-top: 12px;} QGroupBox::title {subcontrol-origin: margin; left: 3px; padding: 0px 0px 5px 0px;}")
        effects_layout=QVBoxLayout()
        self.effects_box.setLayout(effects_layout)

        self.effect1 = QLineEdit()
        effects_layout.addWidget(QLabel("Effect 1"))
        effects_layout.addWidget(self.effect1)
        self.effect1_value = QLabel("")
        self.effect1_value.setStyleSheet("background-color: rgb(196, 214, 0)")
        self.effect1_value.hide()
        effects_layout.addWidget(self.effect1_value)

        self.effect2 = QLineEdit()
        effects_layout.addWidget(QLabel("Effect 2"))
        effects_layout.addWidget(self.effect2)
        self.effect2_value = QLabel("")
        self.effect2_value.setStyleSheet("background-color: rgb(196, 214, 0)")
        self.effect2_value.hide()
        effects_layout.addWidget(self.effect2_value)

        self.effect3 = QLineEdit()
        effects_layout.addWidget(QLabel("Effect 3"))
        effects_layout.addWidget(self.effect3)
        self.effect3_value = QLabel("")
        self.effect3_value.setStyleSheet("background-color: rgb(196, 214, 0)")
        self.effect3_value.hide()
        effects_layout.addWidget(self.effect3_value)

        layout.addWidget(self.input_box)
        layout.addWidget(self.trip_box)
        layout.addWidget(self.effects_box)

        self.checkbox = QCheckBox("Show Bound Values for selected Category")
        self.checkbox.stateChanged.connect(self.toggle_values)
        layout.addWidget(self.checkbox)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.setStyleSheet("background-color: rgb(196, 214, 0); font-size: 15px; font-weight: bold;")
        self.calculate_button.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_button)

        self.EmpTitle= QLabel("Employee Trips")
        self.EmpTitle.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.EmpTitle)
        self.EmpPed= QLabel("Pedestrian Trips:")
        layout.addWidget(self.EmpPed)
        self.EmpBike= QLabel("Bike Trips:")
        layout.addWidget(self.EmpBike)
        self.EmpPublic= QLabel("Public Transport Trips:")
        layout.addWidget(self.EmpPublic)
        self.EmpMotor= QLabel("Motor Trips:")
        layout.addWidget(self.EmpMotor)
        self.Comm= QLabel("Commercial Motor Trips:")
        layout.addWidget(self.Comm)

        self.VisTitle= QLabel("Visitor Trips")
        self.VisTitle.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.VisTitle)
        self.VisPed= QLabel("Pedestrian Trips:")
        layout.addWidget(self.VisPed)
        self.VisBike= QLabel("Bike Trips:")
        layout.addWidget(self.VisBike)
        self.VisPublic= QLabel("Public Transport Trips:")
        layout.addWidget(self.VisPublic)
        self.VisMotor= QLabel("Motor Trips:")
        layout.addWidget(self.VisMotor)

        self.TotTitle= QLabel("Total Trips")
        self.TotTitle.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.TotTitle)
        self.TotPed= QLabel("Pedestrian Trips:")
        layout.addWidget(self.TotPed)
        self.TotBike= QLabel("Bike Trips:")
        layout.addWidget(self.TotBike)
        self.TotPublic= QLabel("Public Transport Trips:")
        layout.addWidget(self.TotPublic)
        self.TotMotor= QLabel("Motor Trips:")
        layout.addWidget(self.TotMotor)
        self.space= QLabel("")
        layout.addWidget(self.space)
        #######################################################################################################################################
    
        self.graph_box = QGroupBox(f"Graph Generation for Instance {self.instance_number}")
        self.graph_box.setMinimumWidth(350)
        self.graph_box.setObjectName("graph_box")
        self.graph_box.setStyleSheet("#graph_box {background-color: white; border: 3px solid rgb(196, 214, 0); font-size: 18px; font-weight: bold; border-radius: 6px; margin-top: 12px;} QGroupBox::title {subcontrol-origin: margin; left: 3px; padding: 0px 0px 5px 0px;}")
        graph_layout=QVBoxLayout()
        self.graph_box.setLayout(graph_layout)

        self.Ganglinien= QLabel("Hourly Graphs")
        self.Ganglinien.setStyleSheet("font-weight: bold;")
        graph_layout.addWidget(self.Ganglinien)

        self.hourly_standarts = QComboBox()
        self.hourly_standarts.addItems(["Wohnnutzung", "kleinflächige gewerbliche Nutzung", "großflächige gewerbliche Nutzung", "Freizeiteinrichtung allgemein", "Kur- und Heilbad ", "Spaß- und Erlebnisbad ", "Großkino", "Discounter (Eigenkreation)", "Tankstellen", "Tegel-Center"])
        graph_layout.addWidget(QLabel("Choose Standard:"))
        graph_layout.addWidget(self.hourly_standarts)

        self.get_button = QPushButton("Get Data for Hourly Graph")
        self.get_button.setStyleSheet("background-color: rgb(196, 214, 0); font-size: 15px; font-weight: bold;")
        self.get_button.clicked.connect(self.get_data)
        graph_layout.addWidget(self.get_button)

        self.table_view = QTableView()
        self.load_data()
        self.table_view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_view.resizeRowsToContents()
        self.table_view.resizeColumnsToContents()
        graph_layout.addWidget(self.table_view)

        self.trip_type = QComboBox()
        self.trip_type.addItems(["Visitor", "Employee", "Commercial", "All Types"])
        graph_layout.addWidget(QLabel("Choose Trip Type:"))
        graph_layout.addWidget(self.trip_type)

        self.means_type = QComboBox()
        self.means_type.addItems(["Pedestrian","Bike","Public","Car"])
        graph_layout.addWidget(QLabel("Choose Means:"))
        graph_layout.addWidget(self.means_type)

        self.graph_button = QPushButton("Create Hourly Graph")
        self.graph_button.setStyleSheet("background-color: rgb(196, 214, 0); font-size: 15px; font-weight: bold;")
        self.graph_button.clicked.connect(self.createGraph)
        graph_layout.addWidget(self.graph_button)
        
        layout.addWidget(self.graph_box)

    def load_data(self):
        
        # Call the imported function
        self.df = load_excel("./resources/Trip Generation Old Tool.xlsm", self.hourly_standarts.currentIndex())
        
        # Create model and connect to view
        model = PandasModel(self.df)
        self.table_view.setModel(model)
        for column in range(model.columnCount()):
            self.table_view.setColumnWidth(column, 150)
        self.table_view.verticalHeader().setFixedWidth(150)
        
        # Configure view to show row titles
        self.table_view.verticalHeader().setVisible(True)

    def toggle_values(self, state):
        boundsToggle = propBounds()
        boundsToggle.retrieveValuesFromExcel(self.category.currentIndex(), datasetPath, datasetSheet)
        if state == Qt.Checked:
            self.employee_value.setText(f"Bounds for Category: {boundsToggle.employee[0]}-{boundsToggle.employee[1]}")
            self.employee_value.show()
            self.visitor_value.setText(f"Bounds for Category: {boundsToggle.visitor[0]}-{boundsToggle.visitor[1]}")
            self.visitor_value.show()
            self.freqEmployee_value.setText(f"Bounds for Category: {boundsToggle.freqEmployee[0]}-{boundsToggle.freqEmployee[1]}")
            self.freqEmployee_value.show()
            self.freqVisitor_value.setText(f"Bounds for Category: {boundsToggle.freqVisitor[0]}-{boundsToggle.freqVisitor[1]}")
            self.freqVisitor_value.show()
            self.motorEmployee_value.setText(f"Bounds for Category: {boundsToggle.motorShareEmployee[0]}-{boundsToggle.motorShareEmployee[1]}")
            self.motorEmployee_value.show()
            self.motorVisitor_value.setText(f"Bounds for Category: {boundsToggle.motorShareVisitor[0]}-{boundsToggle.motorShareVisitor[1]}")
            self.motorVisitor_value.show()
            self.vehiclesEmployee_value.setText(f"Bounds for Category: {boundsToggle.vehicleEmployee[0]}-{boundsToggle.vehicleEmployee[1]}")
            self.vehiclesEmployee_value.show()
            self.vehiclesVisitor_value.setText(f"Bounds for Category: {boundsToggle.vehicleVisitor[0]}-{boundsToggle.vehicleVisitor[1]}")
            self.vehiclesVisitor_value.show()
            self.commercial_value.setText(f"Bounds for Category: {boundsToggle.commercial[0]}-{boundsToggle.commercial[1]}")
            self.commercial_value.show()

            self.effect1_value.setText(f"Bounds for Category: {boundsToggle.effect1[0]}-{boundsToggle.effect1[1]}")
            self.effect1_value.show()
            self.effect2_value.setText(f"Bounds for Category: {boundsToggle.effect2[0]}-{boundsToggle.effect2[1]}")
            self.effect2_value.show()
            self.effect3_value.setText(f"Bounds for Category: {boundsToggle.effect3[0]}-{boundsToggle.effect3[1]}")
            self.effect3_value.show()
        else:
            self.employee_value.hide()
            self.visitor_value.hide()
            self.freqEmployee_value.hide()
            self.freqVisitor_value.hide()
            self.motorEmployee_value.hide()
            self.motorVisitor_value.hide()
            self.vehiclesEmployee_value.hide()
            self.vehiclesVisitor_value.hide()
            self.employee_value.hide()
            self.commercial_value.hide()
            self.effect1_value.hide()
            self.effect2_value.hide()
            self.effect3_value.hide()

    def get_data(self):
        self.load_data()
        return

    
    def createGraph(self):
        hourlyData=table_view_to_dataframe(self.table_view)
        hourlyData = hourlyData.drop(hourlyData.index[-1])
        chosenProps=None
        if(self.trip_type.currentIndex()==0):chosenProps=self.visitorProps
        elif(self.trip_type.currentIndex()==1):chosenProps=self.employeeProps
        elif(self.trip_type.currentIndex()==2): chosenProps=self.projectSite.commercial
        elif(self.trip_type.currentIndex()==3): chosenProps=[self.visitorProps, self.employeeProps, self.projectSite.commercial]

        graphData= calculateDataForGraph(hourlyData, chosenProps, self.trip_type.currentIndex(), self.means_type.currentIndex())
        print(graphData)
        self.graph_window = GraphWindow(graphData)
        self.graph_window.show()
        return
    
    
    def calculate(self):
        areaInp = float(self.area.text())
        employeeRateInp = float(self.employeeRate.text())
        visitorRateInp = float(self.visitorRate.text())
        freqEmployeeInp = float(self.freqEmployee.text())
        freqVisitorInp = float(self.freqVisitor.text())
        pedShareEmployeeInp = float(self.pedShareEmployee.text())
        pedShareVisitorInp = float(self.pedShareVisitor.text())
        bikeShareEmployeeInp = float(self.bikeShareEmployee.text())
        bikeShareVisitorInp = float(self.bikeShareVisitor.text())
        publicShareEmployeeInp = float(self.publicShareEmployee.text())
        publicShareVisitorInp = float(self.publicShareVisitor.text())
        motorEmployeeInp = float(self.motorEmployee.text())
        motorVisitorInp = float(self.motorVisitor.text())
        vehiclesEmployeeInp = float(self.vehiclesEmployee.text())
        vehiclesVisitorInp = float(self.vehiclesVisitor.text())
        commercialInp = float(self.commercial.text())
        effect1Inp=0
        effect2Inp=0
        effect3Inp=0
        try:
            effect1Inp = float(self.effect1.text())
        except ValueError:
            print('Value is not a float')
        try:
            effect2Inp = float(self.effect2.text())
        except ValueError:
            print('Value is not a float')
        try:
            effect3Inp = float(self.effect3.text())
        except ValueError:
            print('Value is not a float')

        categoryInp = self.category.currentIndex()

        bounds = propBounds()
        bounds.retrieveValuesFromExcel(categoryInp, datasetPath, datasetSheet)
        if(employeeRateInp<bounds.employee[0] or employeeRateInp>bounds.employee[1]):
            self.employeeRate.setStyleSheet("background-color: yellow;")
        else:
            self.employeeRate.setStyleSheet("")

        if isinstance(bounds.visitor[0], float):
            if(visitorRateInp<float(bounds.visitor[0]) or visitorRateInp>bounds.visitor[1]):
                self.visitorRate.setStyleSheet("background-color: yellow;")
            else:
                self.visitorRate.setStyleSheet("")
        
        if(freqEmployeeInp<bounds.freqEmployee[0] or freqEmployeeInp>bounds.freqEmployee[1]):
            self.freqEmployee.setStyleSheet("background-color: yellow;")
        else:
            self.freqEmployee.setStyleSheet("")

        if(freqVisitorInp<bounds.freqVisitor[0] or freqVisitorInp>bounds.freqVisitor[1]):
            self.freqVisitor.setStyleSheet("background-color: yellow;")
        else:
            self.freqVisitor.setStyleSheet("")

        if(motorEmployeeInp<bounds.motorShareEmployee[0] or motorEmployeeInp>bounds.motorShareEmployee[1]):
            self.motorEmployee.setStyleSheet("background-color: yellow;")
        else:
            self.motorEmployee.setStyleSheet("")
        if(motorVisitorInp<bounds.motorShareVisitor[0] or motorVisitorInp>bounds.motorShareVisitor[1]):
            self.motorVisitor.setStyleSheet("background-color: yellow;")
        else:
            self.motorVisitor.setStyleSheet("")

        if(vehiclesEmployeeInp<bounds.vehicleEmployee[0] or vehiclesEmployeeInp>bounds.vehicleEmployee[1]):
            self.vehiclesEmployee.setStyleSheet("background-color: yellow;")
        else:
            self.vehiclesEmployee.setStyleSheet("")
        if(vehiclesVisitorInp<bounds.vehicleVisitor[0] or vehiclesVisitorInp>bounds.vehicleVisitor[1]):
            self.vehiclesVisitor.setStyleSheet("background-color: yellow;")
        else:
            self.vehiclesVisitor.setStyleSheet("")
        if(commercialInp<bounds.commercial[0] or commercialInp>bounds.commercial[1]):
            self.commercial.setStyleSheet("background-color: yellow;")
        else:
            self.commercial.setStyleSheet("")

        if isinstance(bounds.effect1[0], float):
            if(effect1Inp<bounds.effect1[0] or effect1Inp>bounds.effect1[1]):
                self.effect1.setStyleSheet("background-color: yellow;")
            else:
                self.effect1.setStyleSheet("")
        if isinstance(bounds.effect2[0], float):
            if(effect2Inp<bounds.effect2[0] or effect2Inp>bounds.effect2[1]):
                self.effect2.setStyleSheet("background-color: yellow;")
            else:
                self.effect2.setStyleSheet("")
        if isinstance(bounds.effect3[0], float):
            if(effect3Inp<bounds.effect3[0] or effect3Inp>bounds.effect3[1]):
                self.effect3.setStyleSheet("background-color: yellow;")
            else:
                self.effect3.setStyleSheet("")
        ################ Main calculations
        self.projectSite = Site(areaInp, employeeRateInp, visitorRateInp, commercialInp)
        self.projectSite.calculateEmployee()
        self.projectSite.calculateVisitors()
        self.projectSite.calculateCommercialRoutes()

        self.employeeProps = tripProp(freqEmployeeInp, motorEmployeeInp, vehiclesEmployeeInp, pedShareEmployeeInp, bikeShareEmployeeInp, publicShareEmployeeInp)
        self.visitorProps = tripProp(freqVisitorInp, motorVisitorInp, vehiclesVisitorInp,pedShareVisitorInp, bikeShareVisitorInp, publicShareVisitorInp )
        self.employeeProps.calculateRoutes(self.projectSite.employees, False)
        self.visitorProps.calculateRoutes(self.projectSite.visitors, True)
    

        self.EmpPed.setText(f"Pedestrian Trips: {self.employeeProps.pedestrianTrips}")
        self.EmpBike.setText(f"Bike Trips: {self.employeeProps.bikeTrips}")
        self.EmpPublic.setText(f"Public Transport Trips: {self.employeeProps.publicTrips}")
        self.EmpMotor.setText(f"Car Trips: {self.employeeProps.motorTrips}")

        self.VisPed.setText(f"Pedestrian Trips: {self.visitorProps.pedestrianTrips}")
        self.VisBike.setText(f"Bike Trips: {self.visitorProps.bikeTrips}")
        self.VisPublic.setText(f"Public Transport Trips: {self.visitorProps.publicTrips}")
        self.VisMotor.setText(f"Car Trips: {self.visitorProps.motorTrips}")

        self.Comm.setText(f"Commercial Car Trips: {self.projectSite.commercial}")

        self.TotPed.setText(f"Pedestrian Trips: {self.employeeProps.pedestrianTrips+self.visitorProps.pedestrianTrips}")
        self.TotBike.setText(f"Bike Trips: {self.employeeProps.bikeTrips+self.visitorProps.bikeTrips}")
        self.TotPublic.setText(f"Public Transport Trips: {self.employeeProps.publicTrips+self.visitorProps.publicTrips}")
        self.TotMotor.setText(f"Car Trips: {self.employeeProps.motorTrips+self.visitorProps.motorTrips+self.projectSite.commercial}")

        

        return {

            'EmpPed': self.employeeProps.pedestrianTrips,
            'EmpBike': self.employeeProps.bikeTrips,
            'EmpPublic': self.employeeProps.publicTrips,
            'EmpMotor': self.employeeProps.motorTrips,

            'VisPed': self.visitorProps.pedestrianTrips,
            'VisBike': self.visitorProps.bikeTrips,
            'VisPublic': self.visitorProps.publicTrips,
            'VisMotor': self.visitorProps.motorTrips,

            'TotPed': self.employeeProps.pedestrianTrips+self.visitorProps.pedestrianTrips,
            'TotBike': self.employeeProps.bikeTrips+self.visitorProps.bikeTrips,
            'TotPublic': self.employeeProps.publicTrips+self.visitorProps.publicTrips,
            'TotMotor': self.employeeProps.motorTrips+self.visitorProps.motorTrips+self.projectSite.commercial,
            'CommMotor': self.projectSite.commercial,

        }
