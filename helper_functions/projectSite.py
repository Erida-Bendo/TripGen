
class Site:
    def __init__(self, area, employeeRate, visitorRate, commercialRate, employees=None, visitors=None, commercial=None):
        self.area = area
        self.employeeRate = employeeRate
        self.visitorRate = visitorRate
        self.employees = employees
        self.visitors = visitors
        self.commercialRate = commercialRate
        self.commercial = commercial

    def calculateEmployee(self):
        if self.employeeRate != 0:
            self.employees = self.area / self.employeeRate
        else:
            self.employees = None  
    
    def calculateVisitors(self):
        if self.visitorRate != 0:
            self.visitors = self.area * self.visitorRate
        else:
            self.visitors = None
    def calculateCommercialRoutes(self):
        self.commercial=self.area/100*self.commercialRate
