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
        xl = numpy.zeros((nLocations, nLocations))
        arrivalTime = [0] * (nLocations-1)
        waitTime = [0] * (nLocations-1)
        vehicleId = 0
        vehi = Vehicle(vehicleId)

        #closestOne stores the index(min_index) and value (min_value) of the closest cities
        # arrivalTime = [] 
        # waitTime = []
        closestOne=[]
        min_index=0
        min_value=0
        positionX = 0
        aTime = 0  
        visitedLocations=[]  
        #this code is used to create the routes
        for indexX in xrange(0, nLocations):  
            visited = 0
            print "arrivalTime: ",arrivalTime
            print "closestOne", closestOne        
            print "position X: ", positionX
            #checks if arrival time is close to the time limit 
            if (maxTime - arrivalTime[indexX-1]<min(i for i in dist[positionX] if i > 0)):
                indexX -=1
                print "ENTER INDEX -1"
                #gets the minimun element and index of the visited matriz row, including the origin
                min_index, min_value = min(enumerate(i for i in dist[positionX] if i > 0), key=operator.itemgetter(1))
            else:
                #gets the minimun element and index of the visited matriz row, but the origin
                positions = [x for i,x in enumerate(dist[positionX]) if i!=0]
                print "positions: ",positions
                min_index, min_value = min(enumerate(i for i in positions if i > 0), key=operator.itemgetter(1))
            #when an index is added, we need to compensate for the cut of the 0 element, depending on its position 
            min_index+=1 

            #when an index is added, we need to compensate for the cut of the 0 element, depending on its position  
            if(min_index>positionX)and (indexX!=0):  
                min_index+=1  

            #checks if the location has already been visited
            if(min_index in visitedLocations):
                #visited = 1
                #indexX -=1
                setRepeated = range(0, nLocations)
                setNotRepeated =list(set(range(1, nLocations))-set(visitedLocations))
                print "setRepeated: ",setRepeated,"setNotRepeated: ",setNotRepeated
                randomElement = random.choice(setNotRepeated)
                print "randomElement: ",randomElement
                positions = [x for j,x in enumerate(dist[randomElement]) if j!=0]            
                min_index, min_value = min(enumerate(k for k in positions if k > 0), key=operator.itemgetter(1))
                print "positions: ",positions
                print "min_index before: ", min_index
                print "min_value before: ", min_value

            #if its already visited, go back index and continue with another
            if (visited==0):
                print "min_index: ", min_index
                print "min_value: ", min_value
                #first trip
                if(indexX==0):
                    if(timeWindow[min_index][positionX]>=min_value):
                        val = timeWindow[min_index][positionX]-min_value
                        waitTime[indexX]=val
                        aTime = min_value + tl[min_index] + waitTime[indexX]
                        print "enter 0" 
                        print "val: ",val
                        print "aTime: ",aTime
                        print "waitTime: ",waitTime[indexX]   
                        print "tw: ",timeWindow[min_index][positionX]
                else:
                    print "enter ",indexX
                    print "position X: ", positionX
                    print "tw: ",timeWindow[min_index][0]
                    #this part of the code will ensure the task is between the time windows  
                    if(timeWindow[min_index][0]>=arrivalTime[indexX-1]):
                        val = timeWindow[min_index][0]-min_value
                        waitTime[indexX]=val
                        aTime = min_value + tl[min_index] + waitTime[indexX]
                        print "val: ",val
                        print "aTime: ",aTime
                        print "waitTime: ",waitTime[indexX] 
                
                        
                closestOne.append([min_index, min_value])   
                visitedLocations.append(min_index)
                arrivalTime[indexX]=aTime
                positionX = min_index
                print "position X: ", positionX
                vehi.addLocationToVehicle(vehicleId,closestOne) 

    def getVehicles(self):
        return(self.vehicles)

    def getTimeWindow(self):
        return(self.timeWindow[0+1][0])

    print timeWindow[7][0]
    print "arrivalTime: ",arrivalTime
    print "waitTime: ",waitTime
    print "vehicleId: ",vehicleId
    print "minimun of all: ", closestOne
    print "min_index: ", min_index
    print "min_value: ", min_value