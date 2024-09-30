from projectSite import Site

class tripProp:
    def __init__(self, frequency, motorizedShare, vehicleOccupancy):
        self.frequency=frequency
        self.motorizedShare = motorizedShare
        self.vehicleOccupancy = vehicleOccupancy
    
def calculateTrips(area, people, frequency, motorizedShare, vehicleOccupancy):
    trips = area/people*frequency*motorizedShare/vehicleOccupancy
    return trips

def calculateEmployeeRoutes(projectSite:Site, tripProperties:tripProp):
     trips= calculateTrips(projectSite.area, projectSite.employees, 
                           tripProperties.frequency, tripProperties.motorizedShare, tripProperties.vehicleOccupancy)
     return trips

def calculateVisitorsRoutes(projectSite:Site, tripProperties:tripProp):
     trips= calculateTrips(projectSite.area, projectSite.visitors, 
                           tripProperties.frequency, tripProperties.motorizedShare, tripProperties.vehicleOccupancy)
     return trips



     