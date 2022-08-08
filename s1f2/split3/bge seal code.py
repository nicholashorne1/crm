import bge
import math
import mathutils
import csv
cont = bge.logic.getCurrentController()
own = cont.owner



def callback_three(object, point, normal):
    print('Hit by %r at %s with normal %s' % (object.name, point, normal))
    hp = mathutils.Vector(point)
    hit_ob = object.name
    print("CONTACTTTTTTTT",hit_ob)
    sv = (bge.logic.getCurrentScene().objects['seal2'].getVelocity(hp))
    seal_pos = (bge.logic.getCurrentScene().objects['seal2'].localPosition)
    kv = (bge.logic.getCurrentScene().objects[hit_ob].getVelocity(hp))
    dev = (bge.logic.getCurrentScene().objects[hit_ob])
    lt = dev.localTransform
    wt = dev.worldTransform
    rot = dev.localOrientation
    loc = dev.worldPosition
    x = mathutils.Vector((0,0,16))
    print("ROT",rot)
    print("LOC",loc)
    print("New loc",(hp-loc))
    b=hp-loc
    b.rotate(rot)
    print("B",b)
    #loc,rot,sca = lt.decompose()
    nv=dev.getVelocity(b)
    print("NV",nv)
    Basepath = own['basepath']
    Run = own['run_counter']
    #Start_pos = own['Start_pos']
    #Head = own['Start_head']
    #Inc = own['Start_inc']
    Collision = own['collision_counter']
    #lag = own['lag']
    print("Seal Velocity", sv)
    print("Kite Velocity", nv)
    cv = (sv-nv).magnitude
    print(cv)
    with open(Basepath + '/output.csv', 'a') as csvfile:
        collisiondata = csv.writer(csvfile, delimiter=',')
        collisiondata.writerow((Run,sv[0],sv[1],sv[2],nv[0],nv[1],nv[2],hp[0],hp[1],hp[2],seal_pos[0],seal_pos[1],seal_pos[2],cv))
    #print("Collision.Game.End")
    #bge.logic.endGame()

def main():
    
    cont = bge.logic.getCurrentController()
    own = cont.owner

    if 'init' not in own:
        cont.owner.collisionCallbacks.append(callback_three)
		
   
   
main()
