###Collision Risk model script
#Looped collision of Minesto Kite with seal object.

##Import modules
import os
import bpy
import math
from math import radians
import csv
import mathutils 
from mathutils import Vector
import numpy as np
#Delete cube
bpy.ops.object.delete(use_global=False)
#Change to game engine
bpy.context.scene.render.engine = 'BLENDER_GAME'

#Basepath = "/home/pal/tmp/CollisionRiskModellblender/NickModel/Modelrunfolder"
#Basepath = os.getcwd()
Basepath = "C:\\Users\\Portaferry\\Desktop\\May_CRM3\\s3f1\\split3"
#Basepath = "/home/nicholas/Desktop/CRM2/CRM_April_runs/Test"
#Basepath = "/media/nicholas/OS/Users/Nicholas/Desktop/PhD/CRM/Model_run_folder/"
Device_base = "/base.stl"
Device_rotor = "/rotor.stl"
Filenameanimal = "/seal2.ply"
#Filenamedata = "test dataset.csv" #File of data to run.
#Input_file = "/2pos_run_input.csv"
#Input_file = "/2_pos_test.csv"
Input_file = "/input.csv"

#Input_file = "/collision1.csv"
collisionfilename = "/crm3_1.8ms.csv"
#runsfilename = "/runs_angles_testing_90.csv"
#Set the scene 
#Set the units
sc = bpy.data.scenes['Scene']
#Set to metric
sc.unit_settings.system = 'METRIC'
bpy.context.scene.game_settings.physics_gravity = 0
#Radius of sphere
Sp_rad = 25
#Number of subdivisions in sphere
sub_d = 6

with open(Basepath + '/output.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['run','sv_x','sv_y','sv_z','nv_x','nv_y','nv_z','hp_x','hp_y','hp_z','sp_x','sp_y','sp_z','Collision_speed'])

# with open(Basepath + '/output2.csv', 'w') as csvfile:
    # filewriter = csv.writer(csvfile, delimiter=',',
                            # quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # filewriter.writerow(['Run number','Start_pos','Start_head','Start_inc','Lag'])


###############################

Xpos = []
Ypos = []
Zpos = []
head = []
inc = []
speed = []
flow=[]
lag = []
seal_length = []
seal_width = []
runs = []

############################
#Read in input file - 'Input_file'
with open(Basepath + Input_file) as  csvfile:
	db = csv.reader(csvfile, delimiter = ',')
	next(db,None) #Skips the header row
	for row in db:
		Xpos.append(float(row[0]))
		Ypos.append(float(row[1]))
		Zpos.append(float(row[2]))
		head.append(float(row[3]))
		inc.append(float(row[4]))
		speed.append(float(row[5]))
		flow.append(float(row[6]))
		lag.append(float(row[7]))
		seal_length.append(float(row[8]))
		seal_width.append(float(row[9]))
		runs.append(float(row[10]))
		
# #########################################
#Seal properties
#Will require vector to create angular movement
#seal_speed = 1.8 #Need to check speed will be in m/s

#########################################Set up device
#
#Device - Horizontal Axis Turbine
#Import device
#Turbine Base

#Dont need base
# ~ bpy.ops.import_mesh.stl(filepath= Basepath + Device_base)
# ~ device_base = bpy.data.objects['Base']

# ~ ######################################################Physics of objects
# ~ device_base.game.physics_type = 'RIGID_BODY'
# ~ device_base.game.use_collision_bounds = True
# ~ device_base.game.collision_bounds_type = 'TRIANGLE_MESH'
# ~ device_base.game.use_actor = True
# ~ device_base.game.use_ghost = True
# ~ device_base.game.collision_margin = 0.0

#########
#Device rotor
bpy.ops.import_mesh.stl(filepath= Basepath + Device_rotor)
device_rotor = bpy.data.objects['Rotor']
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
bpy.ops.logic.sensor_add(type='ALWAYS', object = "Rotor")
bpy.ops.logic.controller_add(type='LOGIC_AND', object = "Rotor")
bpy.ops.logic.actuator_add(type='MOTION', object = "Rotor")

rotor_always = device_rotor.game.sensors['Always']
rotor_motion = device_rotor.game.actuators['Motion']

device_rotor.game.controllers['And'].link(sensor = rotor_always, actuator = rotor_motion)
### 1.466075333 radians per second 14rpm @ 3m/s tidal speed

######################################################Physics of objects
device_rotor.game.physics_type = 'RIGID_BODY'
device_rotor.game.use_collision_bounds = True
device_rotor.game.collision_bounds_type = 'TRIANGLE_MESH'
device_rotor.game.use_actor = True
device_rotor.game.use_ghost = True
device_rotor.game.collision_margin = 0.0
#################################################################################

#################################################################################
#
################################Set up animal (seal)
#
#
#
#Import seal object
bpy.ops.import_mesh.ply(filepath= Basepath + "/seal2.ply")
seal = bpy.data.objects['seal2']

#Set properties
#Actuators, controllers, sensors properties.
bpy.ops.object.game_property_new(type = 'TIMER', name = "time")
bpy.ops.object.game_property_new(type = 'INT', name = "collision_counter")
bpy.ops.object.game_property_new(type = 'STRING', name = "run_counter")
bpy.ops.object.game_property_new(type = 'STRING', name = "basepath")
bpy.ops.object.game_property_new(type = 'STRING', name = "Start_pos")
bpy.ops.object.game_property_new(type = 'STRING', name = "Start_head")
bpy.ops.object.game_property_new(type = 'STRING', name = "Start_inc")
bpy.ops.object.game_property_new(type = 'STRING', name = "lag")
seal.game.properties['basepath'].value = Basepath


bpy.ops.logic.sensor_add(type='ALWAYS', object = "seal2")
bpy.ops.logic.sensor_add(type='COLLISION', object = "seal2")
bpy.ops.logic.sensor_add(type='PROPERTY', object = "seal2")
bpy.ops.logic.sensor_add(type='ALWAYS', object = "seal2", name = "dist_always")

bpy.ops.logic.controller_add(type='LOGIC_AND', object = "seal2")
bpy.ops.logic.controller_add(type='LOGIC_OR', object = "seal2")
bpy.ops.logic.controller_add(type='PYTHON', object = "seal2" ,name = "SealPython")
bpy.ops.logic.controller_add(type='LOGIC_OR', object = "seal2", name = "Or2")
bpy.ops.logic.controller_add(type='PYTHON', object = "seal2", name = "dist_py")

bpy.ops.logic.actuator_add(type = 'MOTION', object = "seal2")
bpy.ops.logic.actuator_add(type = 'GAME', object = "seal2")
bpy.ops.logic.actuator_add(type = 'PROPERTY', object = "seal2")

#Connect sens,cont, actu
seal_always = seal.game.sensors['Always']
seal_motion = seal.game.actuators['Motion']
seal_prop = seal.game.sensors['Property']
seal_collision = seal.game.sensors['Collision']
seal_game = seal.game.actuators['Game']
seal_actu_prop = seal.game.actuators['Property']
seal_dist_always = seal.game.sensors['dist_always']
seal_dist_always.use_pulse_true_level = True

seal.game.controllers['Or2'].link(sensor = seal_collision, actuator = seal_actu_prop)
seal.game.controllers['And'].link(sensor = seal_always, actuator = seal_motion)
#seal.game.controllers['Or'].link(sensor = seal_collision, actuator = seal_game)
seal.game.controllers['Or'].link(sensor = seal_prop, actuator = seal_game)
seal.game.controllers['SealPython'].link(sensor = seal_collision, actuator = seal_motion)
seal.game.controllers['dist_py'].link(sensor = seal_dist_always)
seal.game.controllers['dist_py'].link(sensor = seal_collision)
###
#Settings for sens cont actu
#Python code
bpy.ops.text.open(filepath = Basepath + "/bge seal code.py")
sealtext = bpy.data.texts["bge seal code.py"]
seal.game.controllers['SealPython'].text = sealtext

bpy.ops.text.open(filepath = Basepath + "/distance_script.py")
dist_text = bpy.data.texts["distance_script.py"]
seal.game.controllers['dist_py'].text = dist_text


#Actuators
#seal.game.actuators['Motion'].linear_velocity[0] = seal_speed #Can be changed in the loop if needed. Also check at which angle.
seal.game.actuators['Motion'].use_local_linear_velocity = True

seal.game.sensors['Property'].property = 'time'
seal.game.sensors['Property'].value = "10"
seal.game.sensors['Property'].evaluation_type = 'PROPGREATERTHAN'

seal.game.actuators['Game'].mode = 'QUIT'
seal.game.actuators['Property'].mode = 'ADD'
seal.game.actuators['Property'].value = "1"
seal.game.actuators['Property'].property = "collision_counter"
#Seal physics

seal.game.physics_type = 'RIGID_BODY'
seal.game.use_collision_bounds = True
seal.game.collision_bounds_type = 'TRIANGLE_MESH'
seal.game.use_actor = True
seal.game.use_ghost = True
seal.game.collision_margin = 0
###########################################################################################
#Make shorterned list of start positions for testing
#
#
#
#
#
# p1 = pos_list[54]
# p2 = pos_list[276]
# p3 = pos_list[1137]
# p4 = pos_list[356]
# p5 = pos_list[467]
# pos_list = [p1,p2,p3,p4,p5]



#Code for single position
#p1 = Vector((0,-25,0))
#pos_list = [p1]



for v in range(0,len(Xpos)):
	sealdir=Vector(((np.cos(radians(inc[v]))*np.cos(radians(head[v]))),(np.cos(radians(inc[v]))*np.sin(radians(head[v]))),(np.sin(radians(inc[v])))))
	start_pos = Vector((Xpos[v],Ypos[v],Zpos[v]))
	angle=sealdir.angle(start_pos)
	if angle>radians(90):
		seal.location = start_pos
		seal.rotation_euler = ((radians(0),radians(inc[v]),radians(head[v])))
		seal.dimensions = ((seal_length[v],seal_width[v],seal_width[v]))
		seal.game.properties['Start_pos'].value = str(start_pos)
		seal.game.properties['Start_inc'].value = str(inc[v])
		seal.game.properties['Start_head'].value = str(head[v])
		seal.game.actuators['Motion'].linear_velocity[0] = speed[v]		
		seal.game.properties['run_counter'].value = str(runs[v])
		rot_speed = flow[v]
		rotor_motion.angular_velocity[0] = rot_speed
		l = lag[v]
		device_rotor.rotation_euler[0]=device_rotor.rotation_euler[0]-(rot_speed*l)
		seal.game.properties['lag'].value = str(l)
		bpy.ops.view3d.game_start()
	else:
		print("Outside")


#Rename output file
os.rename(Basepath + "/output.csv", Basepath + collisionfilename)
#os.rename(Basepath + "/output2.csv", Basepath + runsfilename)
