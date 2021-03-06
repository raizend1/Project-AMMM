#!/bin/bash

#AMMM Lab Heuristics v1.1
#Run the heuristic algorithm.
#Store the output log in a file and view it on the terminal.
#Copyright 2016 Luis Velasco and Lluis Gifre.
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

python Main.py config/example.dat | tee logs/example.txt
