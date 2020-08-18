##################################################
#      
#      Wave share Relay Hat for Raspbery PI
#           P26 ----> Relay_Ch1
##################################################

#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import subprocess


#  Relay channel to raspberry pi GPIO pins

Relay_Ch1 = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Relay_Ch1,GPIO.OUT)
GPIO.output(Relay_Ch1,GPIO.HIGH)

# MQTT functions: on_connect and on_message 

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")

# The callback for when a PUBLISH message is received from the server.
# This call back will activate the relay for the lights and then determine which song to play


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    GPIO.output(Relay_Ch1,GPIO.LOW)
    if msg.payload == b'Disco':
        print("saturday night")
        player = subprocess.Popen(["mplayer", "stayingalive.mp3", "-ss", "60"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if msg.payload == b'Dog':
        print ("dogs in the house")
        player = subprocess.Popen(["mplayer", "dogs.mp3", "-ss", "60"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep (30)
    # Turn of lights and music
    GPIO.output(Relay_Ch1,GPIO.HIGH)
    player.kill()


# MQTT instance setup

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)

client.loop_forever()
