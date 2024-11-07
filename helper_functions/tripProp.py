from helper_functions.projectSite import Site

class tripProp:
    def __init__(self, frequency, motorizedShare, vehicleOccupancy,pedShare, bikeShare, publicShare, 
                 motorTrips=0, bikeTrips=0, publicTrips=0, pedestrianTrips=0,
                 effect1=0, effect2=0, effect3=0):
        self.frequency=frequency
        self.motorizedShare = motorizedShare
        self.vehicleOccupancy = vehicleOccupancy
        self.pedShare=pedShare
        self.bikeShare=bikeShare
        self.publicShare=publicShare

        self.effect1=effect1
        self.effect2=effect2
        self.effect3=effect3
        self.motorTrips=motorTrips
        self.bikeTrips=bikeTrips
        self.publicTrips=publicTrips
        self.pedestrianTrips=pedestrianTrips
        
    def calculateRoutes(self, persons:float, applyEffects):
        self.motorTrips = persons*self.frequency*self.motorizedShare/self.vehicleOccupancy
        if applyEffects:
            if(self.effect1 != 0):
                self.motortrips=self.motortrips*(1-self.effect1)
            if(self.effect2 != 0):
                self.motortrips=self.motortrips*(1-self.effect2)
            if(self.effect3 != 0):
                self.motortrips=self.motortrips*(1-self.effect3)
        self.bikeTrips = persons*self.frequency*self.bikeShare
        self.publicTrips = persons*self.frequency*self.publicShare
        self.pedestrianTrips = persons*self.frequency*self.pedShare

     