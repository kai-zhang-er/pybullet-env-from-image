import pybullet as p
import time
import math
import pybullet_data
import numpy as np

CLIENT=0
def get_yaw(point):
    dx, dy = point[:2]
    return np.math.atan2(dy, dx)

def get_pitch(point):
    dx, dy, dz = point
    return np.math.atan2(dz, np.sqrt(dx ** 2 + dy ** 2))

def set_camera_pose(camera_point, target_point=np.zeros(3)):
    delta_point = np.array(target_point) - np.array(camera_point)
    distance = np.linalg.norm(delta_point)
    yaw = get_yaw(delta_point) - np.pi/2 # TODO: hack
    pitch = get_pitch(delta_point)
    p.resetDebugVisualizerCamera(distance, math.degrees(yaw), math.degrees(pitch),
                                 target_point)

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
#don't create a ground plane, to allow for gaps etc
p.resetSimulation()
#p.createCollisionShape(p.GEOM_PLANE)
#p.createMultiBody(0,0)
#p.resetDebugVisualizerCamera(5,75,-26,[0,0,1]);


p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, 0)

rect_list=[]
with open("rect.txt") as f:
    lines=f.readlines()
    center_y, center_x=lines[0].strip().split(",")
    center_x=float(center_x)/20
    center_y=float(center_y)/20
    for line in lines[1:]:
        items=line.strip().split(",")
        rect_list.append([float(items[0])/20-center_y, float(items[1])/20-center_x, float(items[2])/40, float(items[3])/40])

print("view center {},{}".format(center_y, center_x))
# set_camera_pose((center_x,center_y,20),(center_x,center_y+3,0))
set_camera_pose((0,5,20),(0,0,0))
print("total rect {}".format(len(rect_list)))

mass = 1
visualShapeId = -1

segmentStart = 0

for rect in rect_list:
    colBoxId = p.createCollisionShape(p.GEOM_BOX,
                                  halfExtents=[rect[2], rect[3], 0.3])
    p.createMultiBody(baseMass=0,
                    baseCollisionShapeIndex=colBoxId,
                    basePosition=[rect[0], rect[1], 0.])

p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, 1)
while (1):
    camData = p.getDebugVisualizerCamera()
    viewMat = camData[2]
    projMat = camData[3]
    p.getCameraImage(256,
                    256,
                    viewMatrix=viewMat,
                    projectionMatrix=projMat,
                    renderer=p.ER_BULLET_HARDWARE_OPENGL)
    keys = p.getKeyboardEvents()
    p.stepSimulation()
    #print(keys)
    time.sleep(0.01)