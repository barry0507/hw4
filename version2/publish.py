
import matplotlib.pyplot as plt

import numpy as np

import serial

import time

import paho.mqtt.client as paho

def get_float(f_str,n):
    a,b,c = f_str.partition(".")
    c=c[:n]
    return ".".join([a,c])

serdev = '/dev/ttyUSB0'

s = serial.Serial(serdev, 9600)

print("start sending RPC")# send RPC to remote

t=[]
time_stamp = np.arange(0,5,1.)
number_of_data = np.arange(0,5,1)
x=[]
y=[]
z=[]
tilt=[]

number_of_all=0
for i in range(0,5):
    s.write("magicline\r".encode()) #???
    time.sleep(0.2) #???
    s.write("/getAcc_logger/run\r".encode())
    number=s.readline()
    print(number.decode())
    number_of_data[i]=int(number.decode())

    j=0
    
    while(j<int(number.decode())):

        line=s.readline() # Read an echo string from K66F terminated with '\n' (pc.putc())
        print(line.decode())
        t_temp=get_float(line.decode().split()[3],1) # Get one digit
        
        if(t_temp in t):
            j=j+1
            continue

        t.append(t_temp)
        x.append(line.decode().split()[0])
        y.append(line.decode().split()[1])
        z.append(line.decode().split()[2])
        if(float(line.decode().split()[2]) < 0.7071):
            tilt.append(1)
        else:
            tilt.append(0)
        number_of_all=number_of_all+1
        if(time_stamp[i]==i): # haven't change
            time_stamp[i] = float(t_temp)
            print(time_stamp[i])
        

        j=j+1
    print(t)
    time.sleep(1)

fig,ax = plt.subplots(1, 1)
ax.plot(time_stamp,number_of_data)
for i in range(5):
    ax.scatter([time_stamp[i],], [number_of_data[i],],50 , color="purple")
ax.set_xlabel('time stamp')
ax.set_ylabel('number of data')
plt.yticks([0, 2*max(number_of_data)])
plt.show()



mqttc = paho.Client()

# Settings for connection

host = "localhost"

topic= "Mbed"

port = 1883


# Callbacks

def on_connect(self, mosq, obj, rc):

    print("Connected rc: " + str(rc))


def on_subscribe(mosq, obj, mid, granted_qos):

    print("Subscribed OK")


def on_unsubscribe(mosq, obj, mid, granted_qos):

    print("Unsubscribed OK")


# Set callbacks


mqttc.on_connect = on_connect

mqttc.on_subscribe = on_subscribe

mqttc.on_unsubscribe = on_unsubscribe


# Connect and subscribe

print("Connecting to " + host + "/" + topic)

mqttc.connect(host, port=1883, keepalive=60)

mqttc.subscribe(topic, 0)

outstr_x=""
outstr_y=""
outstr_z=""
outstr_t=""
outstr_tilt=""
for i in range(number_of_all):
    outstr_x=outstr_x+f"{x[i]}"+' '
    outstr_y=outstr_y+f"{y[i]}"+' '
    outstr_z=outstr_z+f"{z[i]}"+' '
    outstr_t=outstr_t+f"{t[i]}"+' '
    outstr_tilt=outstr_tilt+f"{tilt[i]}"+' '        


mesg = f"{outstr_x}~{outstr_y}~{outstr_z}~{outstr_t}~{outstr_tilt}~{number_of_all}"

mqttc.publish(topic, mesg)

print(mesg)

time.sleep(1)