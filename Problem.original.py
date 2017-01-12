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

        nLocations = 5
    maxTime = 720
    tl = [20,41,21,20]
    timeWindow = [ [266,293] , [579,597] , [198,244] , [211,242] ]
    dist=[[0,22,16,39,10],[22,0,16,12,28],[16,16,0,22,11],[39,12,22,0,23],[10,28,11,23,0]]

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

    xl = numpy.zeros((nLocations, nLocations))
    arrivalTime = [0,0,0,0]
    waitTime = [0,0,0,0]
    count =0
    for l1 in xrange(1,nLocations):
        #count=count +1
        #waitTime[l1-1]=dist[0][l1]
        for l2 in xrange(1,nLocations):
            #distance must be in the time window()  
            if(dist[l1][l2]>=timeWindow[l2][1] and dist[l1][l2]<=timeWindow[l2][2]):
                #each location should be visited only once
                if(xl[l1+1][l2+1]!=1):
                   xl[l1+1][l2+1] = 1 
            # if(timeWindow[l2][1] <= arrivalTime[l2] and arrivalTime[l2] <= timeWindow[l2][2]):
            #     arrivalTime[l2] = arrivalTime[l1]+tl[l1]+ waitTime[l1] +dist[l1,l2]              
            #     xl[l1][l2] = 1
                

        self.tasks = []                             # review this
        for tId in xrange(0, nTasks):               # tId = 0..(nTasks-1)
            task = Task(tId)
            for hId in xrange(0, nThreads):         # hId = 0..(nThreads-1)
                # if thread hId belongs to task tId
                if(TH[tId][hId]):
                    # add thread hId requiring res resources to task tId
                    resources = rh[hId]
                    task.addThreadAndResources(hId, resources)
            self.tasks.append(task)

        self.cpus = []                              # vector with cpus
        self.maxCapacityPerCPUId = [0] * nCPUs      # vector with max capacity of each CPU. initialized to nCPUs zeros [ 0 ... 0 ]
        self.maxCapacityPerCoreId = [0] * nCores    # vector with max capacity of each core. initialized to nCores zeros [ 0 ... 0 ]
        for cId in xrange(0, nCPUs):                # cId = 0..(nCPUs-1)
            cpu = CPU(cId)
            for kId in xrange(0, nCores):           # kId = 0..(nCores-1)
                # if core kId belongs to CPU cId
                if(CK[cId][kId]):
                    # add core kId with capacity to CPU cId
                    capacity = rc[cId]
                    cpu.addCoreAndCapacity(kId, capacity)
                    self.maxCapacityPerCPUId[cId] += capacity
                    self.maxCapacityPerCoreId[kId] = capacity
            self.cpus.append(cpu)

    def getTasks(self):
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
