#!/usr/bin/env python
 
import platform
import socket
import time
import subprocess
import re
 
CARBON_SERVER = '192.168.1.19'
CARBON_PORT = 2003
 
def get_humidity():
    proc = subprocess.Popen(["/usr/local/bin/tempered --scale Fahrenheit"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    #print "program output: ", out
    (TEMP1, HUM1, DEW1) = re.findall(r'\d+\.\d+', out)
    #print "TEMP1: ", TEMP1
    #print "HUM1: ", HUM1
    #print "DEW1: ", DEW1
    return (TEMP1, HUM1, DEW1)
 
def get_temps():
    proc = subprocess.Popen("/usr/local/bin/temper-poll", stdout=subprocess.PIPE
, shell=True)
    (out, err) = proc.communicate()
    #print "program output: ", out
    (TEMP3, TEMP4) = re.findall(r'C (\d+\.\d+)', out)
    return (TEMP3, TEMP4)
 
def send_msg(message):
    #print 'sending message:\n%s' % message
    sock = socket.socket()
    sock.connect((CARBON_SERVER, CARBON_PORT))
    sock.sendall(message)
    sock.close()

if __name__ == '__main__':
    node = platform.node().replace('.', '-')
    while True:
    timestamp = int(time.time())
    temps = get_temps()
    humidity = get_humidity()
    lines = [
        'system.%s.reptile_centertemperature %s %d' % (node, humidity[0], timestamp),
        'system.%s.reptile_relativehumidity %s %d' % (node, humidity[1], timestamp),
        'system.%s.reptile_dewpoint %s %d' % (node, humidity[2], timestamp),
        'system.%s.reptile_hottemperature %s %d' % (node, temps[0], timestamp),
        'system.%s.reptile_coldtemperature %s %d' % (node, temps[1], timestamp)
    ]
    message = '\n'.join(lines) + '\n'
    send_msg(message)
    time.sleep(60)
