#! /usr/bin/python

import mqtt_client as mqtt
import connect as parser
from time import sleep
import sys
from datetime import datetime, timezone
import time
import serial
import json
import os

usb = "COM9"

HYSTERESIS_SECONDS = 60
last_alarm = 0
algorithm = 1

def reset(T, com):
    # Sleep and send anything in TX to reset the device
    sleep(T)
    com.sendByte(0xff)


def alarm():
    now = int(time.time())
    if now <= last_alarm + HYSTERESIS_SECONDS:
        return
    
    last_alarm = now
    # Publish JSON for alarming plataform
    client = mqtt.connect_mqtt(broker, port, client_id, username, password)
    mqtt.publish(client, topic, mqtt.payload(deveui, "TRUE"))


if __name__ == '__main__':
    # Opening COM port and connecting to broker
    comPort = parser.UARTParser("DoubleCOMPort")
    comPort.connectDataComPort(usb)
    
    # Initialize JSON logging
    log_file = 'radar_readings.json'
    readings = []
    
    # Start loop for alarming
    i = 0
    while(True):
        # Reading COM port and parsing it with Parser
        reading = comPort.readAndParseUartDoubleCOMPort()
        y = 0
        
        if algorithm == 1:
            # Checking if is there any people detected
            x = 'numDetectedTracks' in reading
            y+=1
            
            # Log the reading with timestamp
            timestamp = datetime.now(timezone.utc).isoformat()
            reading_with_timestamp = {
                'timestamp': timestamp,
                'reading': reading
            }
            readings.append(reading_with_timestamp)
            
            # Write to JSON file
            try:
                with open(log_file, 'w') as f:
                    json.dump(readings, f, indent=4)
            except Exception as e:
                print(f"Error writing to JSON file: {e}")
            
            print(reading)

            # # Counting detections i and reset radar
            # if x == True:
            #     i = i+1
            #     reset(read_T, comPort)
            # else:
            #     i = 0
            
            # # If i surpasses N, alarm it
            # if i >= N:
            #     alarm()
            #     print("Alarm")
            #     reset(reset_T, comPort)
            #     i = 0
            # else:
            #     sleep(read_T)

        # if algorithm == 2:
        #     if 'enhancedPresenceDet' in reading:
        #         print('enhancedPresenceDet!')
        #         file = open("Enhanced.log", "a") 
        #         file.print(datetime.fromtimestamp(datetime.now(timezone.utc).timestamp()))
        #         file.print(str(reading['enhancedPresenceDet']))
                
        #         enhancedPresenceDet = reading['enhancedPresenceDet']
        #         for zone in enhancedPresenceDet:
        #             if zone > 0:
        #                 alarm()

        #     if 'classifierOutput' in reading:
        #         print('classifierOutput!')
        #         file = open("Classifier.log", "a") 
        #         file.print(datetime.fromtimestamp(datetime.now(timezone.utc).timestamp()))
        #         file.print(str(reading['classifierOutput']))
