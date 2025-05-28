#! /usr/bin/python

import mqtt_client as mqtt
import sys
import os


broker = sys.argv[1]
port = int(sys.argv[2])
client_id = sys.argv[3]
username = sys.argv[4]
password = sys.argv[5]
deveui = sys.argv[6]


def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if(msg.payload.decode() == "reset_" + deveui):
            mqtt.publish(client, "application/reset", str(deveui) + " is reseting")
            os.system('reboot')
            exit()


if __name__ == '__main__':
    client = mqtt.connect_mqtt(broker, port, client_id, username, password)
    mqtt.sub(client, "application/reboot", on_message)