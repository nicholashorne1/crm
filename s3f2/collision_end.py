import bge
import time
def end():

    cont = bge.logic.getCurrentController()
    own = cont.owner

    sens = cont.sensors['Collision']
    actu = cont.actuators['Game']

    if sens.positive:
        time.sleep(0.5)
        cont.activate(actu)
    else:
        cont.deactivate(actu)

end()
