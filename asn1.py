#!/usr/bin/env python
import roslib
import rospy
from fw_wrapper.srv import *

# -----------SERVICE DEFINITION-----------
# allcmd REQUEST DATA
# ---------
# string command_type
# int8 device_id
# int16 target_val
# int8 n_dev
# int8[] dev_ids
# int16[] target_vals

# allcmd RESPONSE DATA
# ---------
# int16 val
# --------END SERVICE DEFINITION----------

# ----------COMMAND TYPE LIST-------------
# GetMotorTargetPosition
# GetMotorCurrentPosition
# GetIsMotorMoving
# GetSensorValue
# GetMotorWheelSpeed
# SetMotorTargetPosition
# SetMotorTargetSpeed
# SetMotorTargetPositionsSync
# SetMotorMode
# SetMotorWheelSpeed

# check to see if blocked
def walkBlock(direction = "none"):
    if (getSensorValue(1) > 900):
        if (getSensorValue(2) > 10 and getSensorValue(5) > 10):
            setMotorTargetPositionCommand(1, 512)
            setMotorTargetPositionCommand(2, 512)
            setMotorTargetPositionCommand(3, 512)
            setMotorTargetPositionCommand(4, 512)
            turn180()
        elif (getSensorValue(2) > 10):
            setMotorTargetPositionCommand(1, 512)
            setMotorTargetPositionCommand(2, 512)
            setMotorTargetPositionCommand(3, 512)
            setMotorTargetPositionCommand(4, 512)
            turnRight()
        elif (getSensorValue(5) > 10):
            setMotorTargetPositionCommand(1, 512)
            setMotorTargetPositionCommand(2, 512)
            setMotorTargetPositionCommand(3, 512)
            setMotorTargetPositionCommand(4, 512)
            turnLeft()
        else:    
            turnRight()
            if (getSensorValue(1) > 1000):
                turnRight()
                
    if (direction == "left"):        
        wallWalk("left")
    elif (direction == "right"):
        wallWalk("right")
    else:
        walk()
    

# wall following function
def wallWalk(direction):
    walk()
    #walk()
    if (direction == "left"):
        port = 2
        if (getSensorValue(port) < 1):
            partialTurnLeft(482)
        elif (getSensorValue(port) > 25):
            partialTurnRight(542)
    else:
        port = 5
        if (getSensorValue(port) < 1):
            partialTurnRight(542)
        elif (getSensorValue(port) > 25):
            partialTurnLeft(482)
    setMotorTargetPositionCommand(1, 512)
    setMotorTargetPositionCommand(2, 512)
    setMotorTargetPositionCommand(3, 512)
    setMotorTargetPositionCommand(4, 512)
    pause()
    

def pause():
    a = 0
    while (a < 10000000):
        a += 1
        
def slowMotorTurn(motorID, finalPosition):
    currentPosition = getMotorPositionCommand(motorID)
    if (currentPosition < finalPosition):
        while (currentPosition < finalPosition):
            currentPosition += 2
            setMotorTargetPositionCommand(motorID, currentPosition)
    else:
        while (currentPosition > finalPosition):
            currentPosition -= 2
            setMotorTargetPositionCommand(motorID, currentPosition)
            

        
#one part of the left turn        
def partialTurnLeft(angle=427):
    #right leg planted
    setMotorTargetPositionCommand(4, 362)
    setMotorTargetPositionCommand(3, 462)
    pause()
    
    #turn left leg left
    setMotorTargetPositionCommand(2, angle)
    pause()
    
    #feet flat
    setMotorTargetPositionCommand(3, 512)
    setMotorTargetPositionCommand(4, 512)
    pause()
    
    #left leg planted
    setMotorTargetPositionCommand(3, 662)
    setMotorTargetPositionCommand(4, 592)
    #setMotorTargetPositionCommand(7, 1000)
    pause()
    
    #
    slowMotorTurn(2, 562)
    setMotorTargetPositionCommand(3, 512)
    pause()
    
    # feet flat
    setMotorTargetPositionCommand(4, 512)
    #setMotorTargetPositionCommand(7, 812)
    pause()
 
# actual left turn function    
def turnLeft():
    i = 0
    while (i < 2):
        partialTurnLeft()
        i += 1
        
        
def partialTurnRight(angle=602):
    #change shoulder position
    setMotorTargetPositionCommand(5, 412)
    setMotorTargetPositionCommand(6, 612)

    #left leg planted
    setMotorTargetPositionCommand(4, 562)
    setMotorTargetPositionCommand(3, 662)
    pause()
    
    #turn right leg right
    setMotorTargetPositionCommand(1, angle)
    pause()
    
    #feet flat
    setMotorTargetPositionCommand(3, 512)
    setMotorTargetPositionCommand(4, 512)
    pause()
    
    #right leg planted
    setMotorTargetPositionCommand(3, 442)
    setMotorTargetPositionCommand(4, 362)
    #setMotorTargetPositionCommand(8, 24)
    pause()
    
    #
    slowMotorTurn(1, 472)
    setMotorTargetPositionCommand(4, 512)
    pause()
    
    # feet flat
    setMotorTargetPositionCommand(3, 512)
    #setMotorTargetPositionCommand(8, 212)
    pause()

def turnRight():
    i = 0
    while (i < 2):
        partialTurnRight()
        i += 1
        
def turn180():
    i = 0
    while (i < 4):
        partialTurnRight(607)
        i += 1

# set walking speed
def walkMotorTurn(motorID, finalPosition):
    speed = 10
    currentPosition = getMotorPositionCommand(motorID)
    if (currentPosition < finalPosition):
        while (currentPosition < finalPosition):
            currentPosition += speed
            setMotorTargetPositionCommand(motorID, currentPosition)
    else:
        while (currentPosition > finalPosition):
            currentPosition -= speed
            setMotorTargetPositionCommand(motorID, currentPosition)

# walking function
def walk():
    #put arms down
    setMotorTargetPositionCommand(7, 1012)
    setMotorTargetPositionCommand(8, 12)
    
    #right leg planted
    setMotorTargetPositionCommand(4, 372)
    setMotorTargetPositionCommand(3, 422)
    pause()
    #left leg move
    #setMotorTargetPositionCommand(1, 412)
    walkMotorTurn(1, 412)
    setMotorTargetPositionCommand(2, 512)
    setMotorTargetPositionCommand(4, 512)
    pause()
    #feet flat
    setMotorTargetPositionCommand(4, 512)
    setMotorTargetPositionCommand(3, 512)
    setMotorTargetPositionCommand(1, 512)
    pause()
    #left leg planted
    setMotorTargetPositionCommand(3, 652)
    setMotorTargetPositionCommand(4, 602)
    pause()
    #right leg move
    #setMotorTargetPositionCommand(2, 612)
    walkMotorTurn(2, 612)
    setMotorTargetPositionCommand(1, 512)
    setMotorTargetPositionCommand(3, 512)
    pause()
    #feet flat
    setMotorTargetPositionCommand(3, 512)
    setMotorTargetPositionCommand(4, 512)
    setMotorTargetPositionCommand(2, 512)
    pause()
    

# wrapper function to call service to get sensor value
def getSensorValue(port):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('GetSensorValue', port, 0, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to set a motor target position
def setMotorTargetPositionCommand(motor_id, target_val):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
	resp1 = send_command('SetMotorTargetPosition', motor_id, target_val, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to get a motor's current position
def getMotorPositionCommand(motor_id):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
	resp1 = send_command('GetMotorCurrentPosition', motor_id, 0, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to check if a motor is currently moving
def getIsMotorMovingCommand(motor_id):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
	resp1 = send_command('GetIsMotorMoving', motor_id, 0, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# Main function
if __name__ == "__main__":
    rospy.init_node('example_node', anonymous=True)
    rospy.loginfo("Starting Group X Control Node...")
    
    # control loop running at 10hz
    r = rospy.Rate(10) # 10hz
    
    # initialize leg motors to normal position
    setMotorTargetPositionCommand(1, 512)
    setMotorTargetPositionCommand(2, 512)
    setMotorTargetPositionCommand(3, 512)
    setMotorTargetPositionCommand(4, 512)
    
    # initialize arm motors to walking position
    setMotorTargetPositionCommand(7, 812)
    setMotorTargetPositionCommand(8, 212)
    pause()
    
    
    while not rospy.is_shutdown():
        
        wallWalk("right")
        
        # sleep to enforce loop rate
        r.sleep()

