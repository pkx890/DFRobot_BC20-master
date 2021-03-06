'''file Publish_Topic.py
   Messages from the device to the cloud are sent by filling in the relevant information of the ALIYUN platform

   If the Message is sent successfully, you can see "Message is sent." in the serial port, and you can see the 
   Message you sent on the ALIYUN platform

   copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
   licence     The MIT License (MIT)
   author      [PengKaixing](kaixing.peng@dfrobot.com)
   version  V1.0
   date  2020-3-19
   get from https://www.dfrobot.com
   get from https://www.dfrobot.com.cn'''


# -*- coding: utf-8 -*
import time
import sys
sys.path.append("../../..")
import DFRobot_BC20

RED = 'R'
BLUE = 'B'
GREEN = 'G'
YELLOW = 'Y'
PURPLE = 'P'
CYAN = 'C'
WHITE = 'W'

'''For general controllers. Communicate by IIC
   Connect Instructions
      Raspberry Pi   |    Module(BC20)
      SDA(GPIO3)     |       D/T
      SCL(GPIO5)     |       C/R
      GND(GPIO6)     |       GND
      VCC(GPIO2)     |       VCC

   IIC address(A0,A1)
     0x30:(A0=0,A1=0)
     0x31:(A0=0,A1=1)
     0x32:(A0=1,A1=0)
     0x33:(A0=1,A1=1) default'''

'''For general controllers. Communicate by Serial
   Connect Instructions
      Raspberry Pi   |    Module(BC20)
      RXD(GPIO10)    |       D/T
      TXD(GPIO8)     |       C/R
      GND(GPIO6)     |       GND
      VCC(GPIO2)     |       VCC'''
          
BC20=DFRobot_BC20.DFRobot_BC20_IIC(0x33)

#BC20=DFRobot_BC20.DFRobot_BC20_Serial()

#Configure device certificate information
ProductKey = "your_ProductKey"
ClientId = "your_ClientId"
DeviceName = "your_DeviceName"
DeviceSecret = "your_DeviceSecret"

#Configure the domain name and port number
ALIYUN_SERVER =".iot-as-mqtt.cn-shanghai.aliyuncs.com"
PORT = "1883"

#Product identifier that needs to be operated

Identifier = "your_Identifier"

#TOPIC that need to be published
pubTopic = "your_pubTopic"

def ConnectCloud():
  print("Attempting MQTT connection...")
  BC20.changeColor(YELLOW)
  while BC20.connected() == False:
    print(".")
    BC20.ledON()
    time.sleep(0.5)
    BC20.ledOFF()
    time.sleep(0.5)    
    if BC20.connect_Aliyun(ProductKey,DeviceName,DeviceSecret):  
      print("Connect Server OK")
    else:
      #Used to detect the connection between the device and the server
      if BC20.getQMTCONN():
        break 
#Initialize BC20        
print("Starting the BC20.Please wait...")
BC20.changeColor(RED)
while BC20.powerOn()==False:
  print(".")
  BC20.ledON()
  time.sleep(0.5)
  BC20.ledOFF()
  time.sleep(0.5)
print("BC20 started successfully!\r\n")  

#Check whether SIM card is inserted
print("Checking SIM card...")
BC20.changeColor(GREEN)
while BC20.checkNBCard() == False:
  print("Please insert the NB SIM card...")
  BC20.ledON()
  time.sleep(0.5)
  BC20.ledOFF()
  time.sleep(0.5)  
print("SIM card check OK!\r\n") 

#Print IMEI, ICCID and IMSI 
BC20.getGSN(1)
print("BC20 IMEI:")
print(BC20.imei)
print("SIM card ICCID:")
print(BC20.getQCCID())
print("SIM card IMSI: ")
print(BC20.getIMI())

'''The module will automatically attempt to connect to the network (mobile station).
   Check whether it is connected to the network.'''
BC20.changeColor(BLUE)
while BC20.getGATT()==0 :
  print(".");
  BC20.ledON()
  time.sleep(0.5)
  BC20.ledOFF()
  time.sleep(0.5)   
print("Network is connected!\r\n")

print("Connecting to DFRobot Aliyun-IoT")

#Configure IoT Server
while BC20.setAliyunserver(ProductKey,ALIYUN_SERVER,PORT) == False:
  print("Connection to server failed!")
  time.sleep(1)

print("Server is available!")
ConnectCloud()

while True:
  time.sleep(5)
  print("send message to cloud...")  
  BC20.publish(pubTopic,"Hello")
  print("Message is sent.")        