'''
AMMM Lab Heuristics v1.0
Representation of a problem instance.
Copyright 2016 Luis Velasco and Lluis Gifre.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import numpy
from Vehicle import Vehicle

class Problem(object):
    def __init__(self, inputData):
        self.inputData = inputData        
        nLocations = self.inputData.nLocations
        maxTime = self.inputData.maxTime
        tl = self.inputData.tl
        timeWindow = self.inputData.timeWindow
        dist = self.inputData.dist
        vehicleId = 0

        vehicles = []      
        #the constraints are the first one to insert into the algorithm
    #first I need to create the matrix that represents if a locations has been visited or not
    #as in cplex with constraint 1 and 2
    #forall(l1 in L1)
    #   sum(l2 in L)xl[l1,l2]==1;
    #forall(l1 in L)
    #   sum(l2 in L)xl[l1,l2]-sum(l2 in L)xl[l2,l1]==0;
    #we have to create the conditions to create the arrival time as in cplex
    #distance must be in the time window()
    #each location should be visited only once

    vehicles = []      
    xl = numpy.zeros((nLocations, nLocations))
    arrivalTime = [0] * (nLocations-1)
    vehicleId = 0
    vehi = Vehicle(vehicleId)

    #closestOne stores the index(min_index) and value (min_value) of the closest cities
    closestOne=[]
    min_index=0
    min_value=0
    positionX = 0
    aTime = 0  
    visitedLocations=[0] 
    locationsDestination=[] 
    visitedLocationsDestination=[] 

    #array with all the destinations
    for indexDestiny in xrange(0, nLocations): 
        dest_value = dist[indexDestiny][0]
        locationsDestination.append(dest_value)

    #this code is used to create the routes
    for indexX in xrange(0, nLocations):  
        min_index, min_value = min(enumerate(i for i in dist[positionX] if i > 0), key=operator.itemgetter(1))
        print "arrivalTime: ",arrivalTime
        print "closestOne", closestOne        
        print "position X: ", positionX

        #when an index is added, we need to compensate for the cut of the 0 element, depending on its position  
        if(min_index>positionX)and (indexX!=0):  
            min_index+=1  

        #checks if the location has already been visited
        if(len(visitedLocations)!=nLocations):
            if(min_index in visitedLocations):
                setRepeated = range(0, nLocations)
                setNotRepeated =list(set(range(1, nLocations))-set(visitedLocations))
                print "setRepeated: ",setRepeated,"setNotRepeated: ",setNotRepeated
                randomElement = random.choice(setNotRepeated)
                print "randomElement: ",randomElement
                positions = [x for j,x in enumerate(dist[randomElement]) if j!=0]     
                min_index = randomElement 
                min_value = min(k for k in positions if k > 0)    
                #min_index, min_value = min(enumerate(k for k in positions if k > 0), key=operator.itemgetter(1))
                print "positions: ",positions
                print "min_index repeated: ", min_index
                print "min_value repeated: ", min_value

        #if its already visited, go back index and continue with another
        print "min_index: ", min_index
        print "min_value: ", min_value

        #first trip
        #atime=0 represents that a new vehicle has been send to a route
        #so we can sum the previous value of arrivalTime to aTime
        if(aTime==0):
            print "timeWindow 1: ",timeWindow[min_index-1][0]
            #if the lower[0] timeWidow is bigger that the distance, the arrivalTime is the 
            # sum of the lower timeWidow and the tl
            if(timeWindow[min_index-1][0]>=min_value):
                aTime = timeWindow[min_index-1][0] + tl[min_index-1] 
                print "tl 1: ", tl[min_index-1]
                print "enter ",indexX 
                print "aTime 1: ",aTime   
                print "tw: ",timeWindow[min_index-1][0]
            else:
                aTime = min_value + tl[min_index-1] 
                print "tl 2: ", tl[min_index-1]
                print "enter ",indexX 
                print "aTime 2: ",aTime  
                print "tw: ",timeWindow[min_index-1][0]
        else:
            #if the time is upper the maxTime, create a new car and reassing the route until it fits
            if(aTime<=maxTime):
                print "timeWindow 2: ",timeWindow[min_index-1][0]
                #if the lower[0] timeWidow is bigger that the distance, the arrivalTime is the 
                # sum of the lower timeWidow and the tl
                if(timeWindow[min_index-1][0]>=min_value):
                    aTime = arrivalTime[indexX-1] + timeWindow[min_index-1][0] + tl[min_index-1]
                    print "tl 3: ", tl[min_index-1] 
                    print "enter ",indexX 
                    print "aTime 3: ",aTime  
                    print "tw: ",timeWindow[min_index-1][0]
                else:
                    aTime = arrivalTime[indexX-1] + min_value + tl[min_index-1] 
                    print "tl 4: ", tl[min_index-1]
                    print "enter ",indexX 
                    print "aTime 4: ",aTime  
                    print "tw: ",timeWindow[min_index-1][0]
            else:
                print "locationsDestination ", "[", min_index,"]",locationsDestination[min_index]  
                aTime = arrivalTime[indexX-1] + locationsDestination[min_index]   
                print "aTime: ",aTime
                vehicles.append(vehi)
                vehicleId += 1
                vehi = Vehicle(vehicleId)
                aTime =0       
                
        closestOne.append([min_index, min_value])   
        visitedLocations.append(min_index)       
        positionX = min_index
        print "position X: ", positionX
        if (aTime!=0):
            print indexX
            arrivalTime[indexX-1]=aTime
        vehi.addLocationToVehicle(vehicleId,min_index)

    def getVehicles(self):
        return(self.vehicles)

    def getTimeWindow(self,posX,posY):
        return(self.timeWindow[posX][posY])