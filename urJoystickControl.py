#Import libraries
##################
import time
import pygame
from pyModbusTCP.client import ModbusClient
import keyboard  # using module keyboard

#Initialize variables
##################
executionTime=0
MODBUS_SERVER_IP="10.20.1.108"

#Process initialization
##################

#Joystick
pygame.joystick.init()
joy=pygame.joystick.Joystick(0)
joy.init()
pygame.display.init()

#communication
# TCP auto connect on first modbus request
c = ModbusClient(host=MODBUS_SERVER_IP, port=502, auto_open=True)
c.host(MODBUS_SERVER_IP)
c.port(502)
# managing TCP sessions with call to c.open()/c.close()
c.open()

#Functions definition
def rescaleAxis(axisPosition,axisIniPosition):
  #Rescale axis position according to its initial resting position.
  #
  #Parameters:
  # axisposition: axis position of the joystick. It should be a value between -1 and 1.
  # axisIniPosition: axis position when the joystick is at rest. It should be a value between -1 and 1.
  #
  #Return:
  # rescaledPosition: axis position between -1 and 1 with a value equal to 0 when the joystick is at rest.
  rescaledPosition=0
  
  lowSegmentLen=1+axisIniPosition
  upperSegmentLen=1-axisIniPosition
  
  if axisPosition<axisIniPosition:
    rescaledPosition=((axisPosition-axisIniPosition)/lowSegmentLen)
  else:
    rescaledPosition=((axisPosition-axisIniPosition)/upperSegmentLen)
  return rescaledPosition

##################
##################
#Main program
##################
##################
#This program get the joystick position and send it to UR robot MODBUS server.
##################

#initialize Joystick position
pygame.event.pump()
axis0Ini=joy.get_axis(0)
axis1Ini=joy.get_axis(1)
axis2Ini=joy.get_axis(2)
axis3Ini=joy.get_axis(3)

while True:
  try:
    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
      print('You Pressed q Key! The program stopped.')
      break
    else:
      #get joystick position
      pygame.event.pump()
      
      #right joystick
      
      #-1 for left, 1 for right
      axis0=joy.get_axis(0)
      axis0=rescaleAxis(axis0,axis0Ini)

      #-1 up 1 down
      axis1=joy.get_axis(1)
      axis1=rescaleAxis(axis1,axis1Ini)
      
      #left joystick
      
      #-1 for left, 1 for right
      axis2=joy.get_axis(2)
      axis2=rescaleAxis(axis2,axis2Ini)
      
      #-1 up 1 down
      axis3=joy.get_axis(3)
      axis3=rescaleAxis(axis3,axis3Ini)
      
      print([round(axis0,2),round(axis1,2),round(axis2,2),round(axis3,2)])
      #Send axis position to Modbus server registers 128, 129, 130 and 131
      if c.write_multiple_registers(128, [int((axis0+1)*100),int((axis1+1)*100),int((axis2+1)*100),int((axis3+1)*100)]):
        pass
      else:
        print("Error")
  except:
      break
