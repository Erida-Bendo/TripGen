class transportStats:
    def __init__(self, employees, visitors, commercial, effect1, effect2, effect3):
        self.employees=employees
        self.visitors=visitors
        self.commercial=commercial
        self.effect1= effect1
        self.effect2 = effect2
        self.effect3 = effect3


    def updateEffects(self):
        if(self.effect1 != 0):
            self.visitors=self.visitors*(1-self.effect1)
        if(self.effect2 != 0):
            self.visitors=self.visitors*(1-self.effect2)
        if(self.effect3 != 0):
            self.visitors=self.visitors*(1-self.effect3)