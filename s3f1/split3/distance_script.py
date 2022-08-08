import bge
import numpy as np
import time
cont = bge.logic.getCurrentController()
own = cont.owner
coll = cont.sensors['Collision']


def dist():
	pos =  own.position
	dist = np.sqrt(np.square(pos[0])+np.square(pos[1])+np.square(pos[2]))
	#print("Distance=",dist)
	if dist>35.1:
		bge.logic.endGame()

def seafloor():
	pos = own.position
	depth = pos[2]
	if depth<-0.5:
		bge.logic.endGame()
def end():
	if coll.positive:
        	time.sleep(0.5)
        	bge.logic.endGame()

dist()
seafloor()
end()
