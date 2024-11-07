import pandas as pd

class propBounds:
    def __init__(self, employee=[0,0], visitor=[0,0], freqEmployee=[0,0], freqVisitor=[0,0], motorShareEmployee=[0,0], 
                 motorShareVisitor=[0,0], vehicleEmployee=[0,0], vehicleVisitor=[0,0], commercial=[0,0], effect1= [0,0], effect2=[0,0], effect3=[0,0]):
        self.employee=employee
        self.visitor = visitor
        self.freqEmployee = freqEmployee
        self.freqVisitor = freqVisitor
        self.motorShareEmployee = motorShareEmployee
        self.motorShareVisitor = motorShareVisitor
        self.vehicleEmployee = vehicleEmployee
        self.vehicleVisitor = vehicleVisitor
        self.commercial = commercial
        self.effect1 = effect1
        self.effect2 = effect2
        self.effect3 = effect3

    def retrieveValuesFromExcel(self, chosenCategory, excelPath, spreadsheet):
        df = pd.read_excel(excelPath, spreadsheet)
        self.employee[0]=df.iloc[4,3+5*chosenCategory]
        self.employee[1]=df.iloc[4,4+5*chosenCategory]
        self.visitor[0]=df.iloc[5,3+5*chosenCategory]
        self.visitor[1]=df.iloc[5,4+5*chosenCategory]
        self.freqEmployee[0]=df.iloc[6,3+5*chosenCategory]
        self.freqEmployee[1]=df.iloc[6,4+5*chosenCategory]
        self.freqVisitor[0]=df.iloc[7,3+5*chosenCategory]
        self.freqVisitor[1]=df.iloc[7,4+5*chosenCategory]
        self.motorShareEmployee[0]=df.iloc[8,3+5*chosenCategory]
        self.motorShareEmployee[1]=df.iloc[8,4+5*chosenCategory]
        self.motorShareVisitor[0]=df.iloc[9,3+5*chosenCategory]
        self.motorShareVisitor[1]=df.iloc[9,4+5*chosenCategory]
        self.vehicleEmployee[0]=df.iloc[10,3+5*chosenCategory]
        self.vehicleEmployee[1]=df.iloc[10,4+5*chosenCategory]
        self.vehicleVisitor[0]=df.iloc[11,3+5*chosenCategory]
        self.vehicleVisitor[1]=df.iloc[11,4+5*chosenCategory]
        self.commercial[0]=df.iloc[12,3+5*chosenCategory]
        self.commercial[1]=df.iloc[12,4+5*chosenCategory]

        self.effect1[0]=df.iloc[16,3+5*chosenCategory]
        self.effect1[1]=df.iloc[16,4+5*chosenCategory]
        self.effect2[0]=df.iloc[17,3+5*chosenCategory]
        self.effect2[1]=df.iloc[17,4+5*chosenCategory]
        self.effect3[0]=df.iloc[18,3+5*chosenCategory]
        self.effect3[1]=df.iloc[18,4+5*chosenCategory]
