#! /usr/bin/python

from paho.mqtt import client as mqtt_client
import json


def connect_mqtt(broker, port, client_id, username, password):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def sub(client, topic, on_message):
    client.subscribe(topic)
    client.on_message = on_message
    client.loop_forever()


def publish(client, topic, msg):
    client.loop_start()
    result = client.publish(topic, json.dumps(msg))
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send msg to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    client.loop_stop()


def payload(deveui, alarm):
    return {
        "deduplicationId": "df74f750-18df-4142-9f1f-7fcc95eb9202",
        "time": "2025-01-22T00:12:31.450251+00:00",
        "deviceInfo": {
            "tenantId": "52f14cd4-c6f1-4fbd-8f87-4025e1d49242",
            "tenantName": "ChirpStack",
            "applicationId": "69e050c8-2db6-4f0b-89e9-69324b5406ec",
            "applicationName": "application",
            "deviceProfileId": "cfac0e09-7135-4109-97f6-192e111c7938",
            "deviceProfileName": "SN50v3",
            "deviceName": "Door Sensor DS03A-LB",
            "devEui": deveui,
            "deviceClassEnabled": "CLASS_A",
            "tags": {
            }
        },
        "devAddr": "00aefc64",
        "adr": True,
        "dr": 5,
        "fCnt": 1,
        "fPort": 2,
        "confirmed": True,
        "data": "CiB//wAAmQAA//8=",
        "object": {
            "EXTI1_Status": "CLOSE",
            "EXTI1_Trigger": "FALSE",
            "EXTI2_Status": "OPEN",
            "EXTI2_Trigger": alarm,
            "EXTI3_Status": "OPEN",
            "EXTI3_Trigger": "FALSE",
            "Work_mode": "3Interrupt",
            "Digital_IStatus": "L",
            "TempC1": "NULL",
            "BatV": 3.192,
            "ADC_CH0V": 0, 
        },
        "rxInfo": [
            {
            "gatewayId": "a84041fdfe2764e4",
            "uplinkId": 40676,
            "time": "2025-01-22T00:12:31.450251+00:00",
            "rssi": -36,
            "snr": 14,
            "channel": 6,
            "rfChain": 1,
            "location": {
                
            },
            "context": "D67rXw==",
            "metadata": {
                "region_config_id": "au915_0",
                "region_common_name": "AU915"
            },
            "crcStatus": "CRC_OK"
            },
            {
            "gatewayId": "a84041fdfe2764e4",
            "uplinkId": 61666,
            "time": "2025-01-22T00:12:31.450232+00:00",
            "rssi": -36,
            "snr": 14,
            "channel": 6,
            "rfChain": 1,
            "location": {
                
            },
            "context": "D67rXw==",
            "metadata": {
                "region_config_id": "au915_0",
                "region_common_name": "AU915"
            },
            "crcStatus": "CRC_OK"
            }
        ],
        "txInfo": {
            "frequency": 916400000,
            "modulation": {
            "lora": {
                "bandwidth": 125000,
                "spreadingFactor": 7,
                "codeRate": "CR_4_5"
            }
            }
        }
}