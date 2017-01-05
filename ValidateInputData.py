'''
AMMM Lab Heuristics v1.0
Instance file validator.
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

# Validate instance attributes read from a DAT file.
# It validates the structure of the parameters read from the DAT file.
# It does not validate that the instance is feasible or not.
# Use Problem.checkInstance() function to validate the feasibility of the instance.
class ValidateInputData(object):
    @staticmethod
    def validate(data):
        # Validate that all input parameters were found
        for paramName in ['nLocations', 'maxTime', 'tl', 'timeWindow', 'dist']:
            if(not data.__dict__.has_key(paramName)):
                raise Exception('Parameter/Set(%s) not contained in Input Data' % str(paramName))

        # Validate nLocations
        nLocations = data.nLocations
        if(not isinstance(nLocations, (int, long)) or (nLocations <= 0)):
            raise Exception('nLocations(%s) has to be a positive integer value.' % str(nLocations))
        
        # Validate maxTime
        maxTime = data.maxTime
        if(not isinstance(maxTime, (int, long)) or (maxTime <= 0)):
            raise Exception('maxTime(%s) has to be a positive integer value.' % str(maxTime))
         
        # Validate tl
        tl = data.tl
        if(len(tl) != nLocations-1):
            raise Exception('Size of tl(%d) does not match with value of nLocations-1(%d).' % (len(tl), nLocations))
        
        for value in tl:
            if(not isinstance(value, (int, long, float)) or (value < 0)):
                raise Exception('Invalid parameter value(%s) in tl. Should be a float greater or equal than zero.' % str(value))
        
        # Validate timeWindow
        timeWindow = data.timeWindow
        if(len(timeWindow) != nLocations):
            raise Exception('Size of timeWindow(%d) does not match with value of nLocations-1(%d).' % (len(timeWindow), nLocations))
        
        for value in timeWindow:
            if(not isinstance(value, (int, long, float)) or (value < 0)):
                raise Exception('Invalid parameter value(%s) in timeWindow. Should be a float greater or equal than zero.' % str(value))

        # Validate dist
        dist = data.dist
        if(len(dist) != nLocations):
            raise Exception('Size of first dimension of dist(%d) does not match with value of nLocations(%d).' % (len(dist), nLocations))
        
        for thEntry in dist:
            if(len(thEntry) != nLocations):
                raise Exception('Size of second dimension of dist(%d) does not match with value of nLocations(%d).' % (len(thEntry), nLocations))

