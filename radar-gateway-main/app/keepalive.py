#! /usr/bin/python

import mqtt_client as mqtt
from time import sleep
import sys


broker = sys.argv[1]
port = int(sys.argv[2])
client_id = sys.argv[3]
username = sys.argv[4]
password = sys.argv[5]
deveui = sys.argv[6]
keepalive_T = int(sys.argv[7])


if __name__ == '__main__':
    while(True):
        client = mqtt.connect_mqtt(broker, port, client_id, username, password)
        mqtt.publish(client, "application/keepalive", mqtt.payload(deveui, "FALSE"))
        sleep(keepalive_T)