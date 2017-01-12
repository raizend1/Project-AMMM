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
from Task import Task
from CPU import CPU

class Problem(object):
    def __init__(self, inputData):
        self.inputData = inputData        
        nLocations = self.inputData.nLocations
        maxTime = self.inputData.maxTime
        tl = self.inputData.tl
        timeWindow = self.inputData.timeWindow
        dist = self.inputData.dist

        self.vehicles = []     
        xl = numpy.zeros((nLocations, nLocations))
        arrivalTime = [0] * nLocations-1
        waitTime = [0] * nLocations-1
        count =0
        

    def getVehicles(self):
        return(self.tasks)

    def getCPUs(self):
        return(self.cpus)

    def checkInstance(self):
        totalCapacityCPUs = 0.0
        maxCoreCapacity = 0.0
        for cpu in self.cpus:
            capacity = cpu.getTotalCapacity()
            totalCapacityCPUs += capacity
            for coreId in cpu.getCoreIds():
                capacity = cpu.getTotalCapacityByCore(coreId)
                maxCoreCapacity = max(maxCoreCapacity, capacity)
                
        totalResourcesTasks = 0.0
        for task in self.tasks:
            resources = task.getTotalResources()
            totalResourcesTasks += resources
            
            threadIds = task.getThreadIds()
            for threadId in threadIds:
                threadRes = task.getResourcesByThread(threadId)
                if(threadRes > maxCoreCapacity): return(False)
            
            feasible = False
            for cpu in self.cpus:
                capacity = cpu.getTotalCapacity()
                feasible = (resources < capacity)
                if(feasible): break
            
            if(not feasible): return(False)
        
        if(totalCapacityCPUs < totalResourcesTasks): return(False)
        
        return(True)
