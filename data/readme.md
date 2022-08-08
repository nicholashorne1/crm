# Data repository for "Providing a detailed estimate of mortality using a simulation-based collision risk model"

## Scenarios
There are 6 different scenarios run within this paper. 3 different animal speeds and 2 different flow speeds.
This therefore correpsonds to the folder names S1F1 being speed 1 and flow 1 - the lower animal and flow speeds. (S2F2 would be the medium animal and higher flow speed).

## Split files
Within each of the scenario folders are 5 split folders - these are the sets of simulations run across 5 splits of the model to reduce computational time. Therefore there is an input file and output file for each split. 
Also, there is the main input file for each scenarios (this was the file that was split to create the split input files).

## Input files
The input files contain the information to run an individual simulation. This contains a starting position, animal speed, flow speed and heading. 
It also contains a 'run number' this is used to identify the individual simulation for matching with results files.

## Output files
The output files contain the results produced when a collision occurs. This includes the speed of collision and where on the animal the collision occurs. 
The results from this are matched to the input file using 'run number'. 
This then allows analysis of number of collisions vs the the number of simulations and further detailed analysis on collision parameters, where on the device or animal collisions occur etc.
