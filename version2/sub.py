import matplotlib.pyplot as plt

import numpy as np

import serial

import time

import paho.mqtt.client as paho

load_list=[]

mqttc = paho.Client()


# Settings for connection

host = "localhost"

topic= "Mbed"

port = 1883


# Callbacks

def on_connect(self, mosq, obj, rc):

    print("Connected rc: " + str(rc))


def on_message(mosq, obj, msg):

    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")
    load_list.append(msg.payload.decode())


def on_subscribe(mosq, obj, mid, granted_qos):

    print("Subscribed OK")


def on_unsubscribe(mosq, obj, mid, granted_qos):

    print("Unsubscribed OK")


# Set callbacks

mqttc.on_message = on_message

mqttc.on_connect = on_connect

mqttc.on_subscribe = on_subscribe

mqttc.on_unsubscribe = on_unsubscribe


# Connect and subscribe

print("Connecting to " + host + "/" + topic)

mqttc.connect(host, port=1883, keepalive=60)

mqttc.subscribe(topic, 0)

nf=0
while(nf <= 3):
    load_list_temp=load_list
    mqttc.loop()
    time.sleep(1)
    if load_list==load_list_temp:
        nf = nf + 1

print(load_list)
x=load_list[0].split("~")[0]
y=load_list[0].split("~")[1]
z=load_list[0].split("~")[2]
t=load_list[0].split("~")[3]
tilt=load_list[0].split("~")[4]

x_plot=[]
y_plot=[]
z_plot=[]
t_plot=[]

for i in range(int(load_list[0].split("~")[5])):
    x_plot.append(float(x.split()[i]))
    y_plot.append(float(y.split()[i]))
    z_plot.append(float(z.split()[i]))
    t_plot.append(float(t.split()[i]))


print(x_plot)
print(t_plot)

fig,ax = plt.subplots(2, 1)
for i in range(int(load_list[0].split("~")[5])):
    ax[1].plot([t_plot[i],t_plot[i]],[0,tilt.split()[i]],color="orange", linewidth=2.5, linestyle="-")
    ax[1].scatter([t_plot[i],], [tilt.split()[i],],50 , color="purple")
#ax[1].plot(t, tilt, color="black", linewidth=2.5, linestyle="dotted", label="tilt")
plt.yticks([0, +1])
ax[0].plot(t_plot, x_plot, color="red", linewidth=2.5, linestyle="-", label="x")
ax[0].plot(t_plot, y_plot, color="green", linewidth=2.5, linestyle="-", label="y")
ax[0].plot(t_plot, z_plot, color="blue", linewidth=2.5, linestyle="-", label="z")
ax[0].legend(loc='best')

plt.show()