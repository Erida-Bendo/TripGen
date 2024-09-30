from projectSite import Site
from tripProp import tripProp, calculateEmployeeRoutes, calculateVisitorsRoutes
from propCheck import propBounds
from transportStats import transportStats
import tkinter as tk
from tkinter import ttk

datasetPath="./resources/Trip Generation Old Tool.xlsm"
datasetSheet="NF-Sets"
    
def calculate():
    # Retrieve values from the input boxes
    areaInp = float(area.get())
    employeeRateInp = float(employeeRate.get())
    visitorRateInp = float(visitorRate.get())
    freqEmployeeInp = float(freqEmployee.get())
    freqVisitorInp = float(freqVisitor.get())
    motorEmployeeInp = float(motorEmployee.get())
    motorVisitorInp = float(motorVisitor.get())
    vehiclesEmployeeInp = float(vehiclesEmployee.get())
    vehiclesVisitorInp = float(vehiclesVisitor.get())
    commercialInp = float(commercial.get())
    effect1Inp = float(effect1.get())
    effect2Inp = float(effect2.get())
    effect3Inp = float(effect3.get())
    categoryInp = category.current()
    
    bounds=propBounds()
    bounds.retrieveValuesFromExcel(categoryInp,datasetPath, datasetSheet)
    #TODO check bounds
    boundCheck = "None"
    if(employeeRateInp<bounds.employee[0] or employeeRateInp>bounds.employee[1]):
        boundCheck="Employee Rate"

    if isinstance(bounds.visitor[0], float):
        if(visitorRateInp<float(bounds.visitor[0]) or visitorRateInp>bounds.visitor[1]):
            boundCheck+=", Visitor Rate"
    
    if(freqEmployeeInp<bounds.freqEmployee[0] or freqEmployeeInp>bounds.freqEmployee[1]):
            boundCheck+=", Emp Freq"

    if(freqVisitorInp<bounds.freqVisitor[0] or freqVisitorInp>bounds.freqVisitor[1]):
        boundCheck+=", Vis Freq"
    if(motorEmployeeInp<bounds.motorShareEmployee[0] or motorEmployeeInp>bounds.motorShareEmployee[1]):
        boundCheck+=", Motor Share Emp"
    if(motorVisitorInp<bounds.motorShareVisitor[0] or motorVisitorInp>bounds.motorShareVisitor[1]):
        boundCheck+=", Motor Share Vis"

    if(vehiclesEmployeeInp<bounds.vehicleEmployee[0] or vehiclesEmployeeInp>bounds.vehicleEmployee[1]):
        boundCheck+=", Vehicle Emp"
    if(vehiclesVisitorInp<bounds.vehicleVisitor[0] or vehiclesVisitorInp>bounds.vehicleVisitor[1]):
        boundCheck+=", Vehicle Vis"
    if(commercialInp<bounds.commercial[0] or commercialInp>bounds.commercial[1]):
        boundCheck+=", Commercial"

    if isinstance(bounds.effect1[0], float):
        if(effect1Inp<bounds.effect1[0] or effect1Inp>bounds.effect1[1]):
            boundCheck+=", Effect1"
    if isinstance(bounds.effect2[0], float):
        if(effect2Inp<bounds.effect2[0] or effect2Inp>bounds.effect2[1]):
            boundCheck+=", Effect2"
    if isinstance(bounds.effect3[0], float):
        if(effect3Inp<bounds.effect3[0] or effect3Inp>bounds.effect3[1]):
            boundCheck+=", Effect3"

    projectSite=Site(areaInp, employeeRateInp, visitorRateInp, commercialInp)
    projectSite.calculateEmployee()
    projectSite.calculateVisitors()
    projectSite.calculateCommercialRoutes()
    

    employeeProps = tripProp(freqEmployeeInp, motorEmployeeInp, vehiclesEmployeeInp)
    visitorProps = tripProp(freqVisitorInp, motorVisitorInp, vehiclesVisitorInp)

    #calculate trips
    employeesRoutes = calculateEmployeeRoutes(projectSite, employeeProps)
    visitorsRoutes = calculateVisitorsRoutes(projectSite, visitorProps)

    trips= transportStats(employeesRoutes, visitorsRoutes, projectSite.commercial, effect1Inp, effect2Inp, effect3Inp)

    trips.updateEffects()
    
    # Perform some calculations (example: sum of the values)
    resultEmpInp = trips.employees
    resultVisInp = trips.visitors
    resultCommInp = trips.commercial
    resultSummInp = trips.employees + trips.visitors + trips.commercial

    #Show values that are out of bounds
    resultCheck2.config(text=f"{boundCheck}")
    
    # Display the result
    resultEmp.config(text=f"Employee Trips: {resultEmpInp}")
    resultVis.config(text=f"Visitor Trips: {resultVisInp}")
    resultComm.config(text=f"Commercial Trips: {resultCommInp}")
    resultSumm.config(text=f"Total: {resultSummInp}")

# region tkinter UI
root = tk.Tk()
root.title("TripGen")

# Create a frame for the table-like layout
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
bold_font = ("TkDefaultFont", 10, "bold")
# region labels
# Create input boxes and labels
ttk.Label(frame, text="Category:", font=bold_font).grid(row=0, column=0, padx=5, pady=5)
category = ttk.Combobox(frame, values=["BüroNutzung", "Discounter", "kleinfl. Einzelhandel", "Einkaufszentrum", "großfl. Einzelhandel", "Getränkemarkt", "Möbelmarkt", "Logistikzentrum",
                                       "Baumarkt", "Handwerksbetrieb", "Autohaus", "Produktionsbetrieb", "Lagerhaus", "Dienstleistungsbetrieb","Fitnesscenter", "Sport und Freizeit",
                                       "Fastfood", "Restaurant", "Hotel", "Tankstelle", "Wohnen", "Wohnen (in ha)"])
category.grid(row=0, column=1, padx=5, pady=5)
category.current(0)  # Set default selection

ttk.Label(frame, text="Area").grid(row=1, column=0, padx=5, pady=5)
area = ttk.Entry(frame)
area.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame, text="Employee per unit").grid(row=2, column=0, padx=5, pady=5)
employeeRate = ttk.Entry(frame)
employeeRate.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame, text="Visitor per unit").grid(row=3, column=0, padx=5, pady=5)
visitorRate = ttk.Entry(frame)
visitorRate.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(frame, text="Frequency Employee").grid(row=4, column=0, padx=5, pady=5)
freqEmployee = ttk.Entry(frame)
freqEmployee.grid(row=4, column=1, padx=5, pady=5)

ttk.Label(frame, text="Frequency Visitor").grid(row=5, column=0, padx=5, pady=5)
freqVisitor = ttk.Entry(frame)
freqVisitor.grid(row=5, column=1, padx=5, pady=5)

ttk.Label(frame, text="Motorized Share Employees").grid(row=6, column=0, padx=5, pady=5)
motorEmployee = ttk.Entry(frame)
motorEmployee.grid(row=6, column=1, padx=5, pady=5)

ttk.Label(frame, text="Motorized Share Visitors").grid(row=7, column=0, padx=5, pady=5)
motorVisitor = ttk.Entry(frame)
motorVisitor.grid(row=7, column=1, padx=5, pady=5)

ttk.Label(frame, text="Vehicle Occupancy Employees").grid(row=8, column=0, padx=5, pady=5)
vehiclesEmployee = ttk.Entry(frame)
vehiclesEmployee.grid(row=8, column=1, padx=5, pady=5)

ttk.Label(frame, text="Vehicle Occupancy Visitors").grid(row=9, column=0, padx=5, pady=5)
vehiclesVisitor = ttk.Entry(frame)
vehiclesVisitor.grid(row=9, column=1, padx=5, pady=5)

ttk.Label(frame, text="Commercial Trips").grid(row=10, column=0, padx=5, pady=5)
commercial = ttk.Entry(frame)
commercial.grid(row=10, column=1, padx=5, pady=5)

ttk.Label(frame, text="Effects", font=bold_font).grid(row=11, column=0, padx=0, pady=5)

ttk.Label(frame, text="Effect 1").grid(row=12, column=0, padx=5, pady=5)
effect1 = ttk.Entry(frame)
effect1.grid(row=12, column=1, padx=5, pady=5)

ttk.Label(frame, text="Effect 2").grid(row=13, column=0, padx=5, pady=5)
effect2 = ttk.Entry(frame)
effect2.grid(row=13, column=1, padx=5, pady=5)

ttk.Label(frame, text="Effect 3").grid(row=14, column=0, padx=5, pady=5)
effect3 = ttk.Entry(frame)
effect3.grid(row=14, column=1, padx=5, pady=5)
# endregion


# Create a button to trigger the calculation
calculate_button = ttk.Button(frame, text="Calculate", command=calculate)
calculate_button.grid(row=15, column=0, columnspan=2, pady=10)

# Create a label to display the values check
resultCheck= ttk.Label(frame, text="Values out of bounds:", font=bold_font)
resultCheck.grid(row=16, column=0, columnspan=2, pady=5)

resultCheck2= ttk.Label(frame, text="", font=bold_font)
resultCheck2.grid(row=17, column=0, columnspan=2, pady=5)

# Create a label to display the result
resultEmp= ttk.Label(frame, text="Employee Trips:", font=bold_font)
resultEmp.grid(row=18, column=0, columnspan=2, pady=5)
resultVis = ttk.Label(frame, text="Visitor Trips:", font=bold_font)
resultVis.grid(row=19, column=0, columnspan=2, pady=5)
resultComm = ttk.Label(frame, text="Commercial Trips:", font=bold_font)
resultComm.grid(row=20, column=0, columnspan=2, pady=5)
resultSumm = ttk.Label(frame, text="Total:", font=bold_font)
resultSumm.grid(row=21, column=0, columnspan=2, pady=5)
###################################################################################################################
# Run the application
root.mainloop()

#endregion
