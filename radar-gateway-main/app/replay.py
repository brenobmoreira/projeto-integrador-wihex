#! /usr/bin/python
import json
from datetime import datetime
import time
import sys
import os
import pprint

# Convert the unix timestamp from packet to date
def toDate(unixtimestamp):
    return datetime.fromtimestamp(unixtimestamp/1000).strftime('%Y-%m-%d-%H:%M:%S')


# Main parse and process packet
def GetParsedFile(confidence, fileName):
    global current_detected_points
    # Open and read the JSON file
    with open(fileName, 'r') as file:
        packet = json.load(file)

    # print("Config:", packet['cfg'])
    # print("Demo:", packet['demo'])
    # print("Device:", packet['device'])

    # Process data in packet
    for data in packet['data']:

        # Get frame data and timestamp of packet
        frameData = data['frameData']
        timestamp = toDate(int(data['timestamp']))
        # print(timestamp, frameData)
        
        # Check if packet is not null
        if 'pointCloud' not in frameData:
            # print("Continuando... frame sem pointCloud: ", frameData)
            # print(timestamp, ":", frameData)
            # time.sleep(5)   # só pra debugar
            # continue
            return -1

        # # Check if packet is not null
        # if 'error' not in frameData:
            # print("Continuando... frame vazio: ", frameData)
            # print(timestamp, ":", frameData)
            # time.sleep(5)   # só pra debugar
            # continue
            # return -1        
        
        # # Check if packet is not null
        # if 'numDetectedPoints' not in frameData:
            # print("Continuando... frame vazio: ", frameData)
            # print(timestamp, ":", frameData)
            # time.sleep(5)   # só pra debugar
            # continue
            # return -1     

        # Check if a track was detected 
        if 'numDetectedTracks' not in frameData:
            # se necesario, resetar logica aqui, pois pode ter recebido uma sequencia de pacotes sem presença
            # continue
            return 0

        # Get track data from packet soon after checked
        numDetectedTracks = frameData['numDetectedTracks']
        # Check if a number of track is 0
        if numDetectedTracks == 0:
            # se necesario, resetar logica aqui, pois pode ter recebido uma sequencia de pacotes sem presença
            # continue
            return 0

        # # Get point from data
        # error = frameData['error']
        frameNum = int(frameData["frameNum"])
        # pointCloud = frameData['pointCloud']
        # numDetectedPoints = frameData['numDetectedPoints']
        # # if error > 0:
        # #     print("Apareceu erros aqui:", fileName, "erros", error )

        # Get tracked target data
        trackData = frameData['trackData']
        # print(timestamp, ":", trackData)

        # Process a target tracked in packet
        for track in trackData:

            # Get target ID
            targetId = int(track[0])

            # Get target position
            x = track[1]
            y = track[2]
            z = track[3]

            # Get target velocity
            vel_x = track[4]
            vel_y = track[5]
            vel_z = track[6]

            # Get target accel
            accel_x = track[7]
            accel_y = track[8]
            accel_z = track[9]

            # Get target Gatting Function Gain
            g = track[10]

            # Get target confidence level
            confidenceLevel = track[11]

            # Get target tracking error covariance matrix
            # ec = [[0 for _ in range(2)] for _ in range(2)]
            # ec[0][0] = track[12]
            # ec[0][1] = track[13]
            # ec[1][0] = track[14]
            # ec[1][1] = track[15]
            # ec = [0 for _ in range(4)]
            # ec[0] = track[12]
            # ec[1] = track[13]
            # ec[2] = track[14]
            # ec[3] = track[15]

            if confidenceLevel < 0 or confidenceLevel > 1 or targetId < 0 or targetId > 249:
                continue #ignore
            

            # Log
            # print(timestamp, "| FID:", frameData['frameNum'],  "| TID:", targetId, "| CL:", "{:.7lf}".format(confidenceLevel), \
            #     "| Px:", "{:+.3f}".format(x), "| Py:", "{:+.3f}".format(y), "| Pz:", "{:+.3f}".format(z), \
            #     )
            # print(timestamp, frameData['frameNum'], targetId, confidenceLevel)
            # print(timestamp, frameData['frameNum'], targetId, x, y, z, vel_x, vel_y, vel_z, accel_x, accel_y, accel_z, confidenceLevel)

            # Logic is here 
            if (confidenceLevel > confidence):
                print(timestamp, " FrameID:", frameData['frameNum'],  " TargetID:", targetId, "    alarm ", " ConfLevel:", confidenceLevel)
                if targetId not in target_map:
                    target_map[targetId] = dict()
                    target_map[targetId]['first_time'] = timestamp
                    target_map[targetId]['first_packet'] = frameNum
                    target_map[targetId]['last_packet'] = frameNum
                    target_map[targetId]['first_pos'] = {x,y,z}
                    target_map[targetId]['current_in_sequence'] = 0
                    target_map[targetId]['max_current_in_sequence'] = 0
                    current_detected_points += 1
                
                if target_map[targetId]['last_packet'] == frameNum - 1:
                    target_map[targetId]['current_in_sequence'] += 1
                    if target_map[targetId]['current_in_sequence'] > target_map[targetId]['max_current_in_sequence']:
                        target_map[targetId]['max_current_in_sequence'] = target_map[targetId]['current_in_sequence']
                else:
                    target_map[targetId]['current_in_sequence'] = 0

                target_map[targetId]['last_time'] = timestamp
                target_map[targetId]['last_packet'] = frameNum
                target_map[targetId]['last_pos'] = {x,y,z}

                # print("Alarmando - Timestamp:", timestamp, "Target ID:", targetId)
                # print("Posi XYZ:", "%.2f" % x, "%.2f" % y, "%.2f" % z)
                # print("Veloc XYZ:", "%.2f" % vel_x, "%.2f" % vel_y, "%.2f" % vel_z)
                # print("Accel XYZ:", "%.2f" % accel_x, "%.2f" % accel_y, "%.2f" % accel_z)
                # print("Gating function Gain:", g)
                # print("ConfidenceLevel:", confidenceLevel)
                # print("Tracking error covariance matrix:", ec)
                # return 1
            # else:
            #     print(timestamp, " FrameID:", frameData['frameNum'],  " TargetID:", targetId, " no alarm ", " ConfLevel:", confidenceLevel)
                # print("Não alarmando - Timestamp:", timestamp, "Target ID:", targetId)
                # print("Posi XYZ:", "%.2f" % x, "%.2f" % y, "%.2f" % z)
                # print("Veloc XYZ:", "%.2f" % vel_x, "%.2f" % vel_y, "%.2f" % vel_z)
                # print("Accel XYZ:", "%.2f" % accel_x, "%.2f" % accel_y, "%.2f" % accel_z)
                # print("Gating function Gain:", g)
                # print("ConfidenceLevel:", confidenceLevel)
                # print("Tracking error covariance matrix:", ec)
                # return 0

    return 1
        
        #     if confidenceLevel < 0.99:
        #         #nao confiavel
        #         print("Ignorando esse trackData")
        #         continue

            #colocar a logica aqui: 


# Initial folder, number of packets and confidence in tracked IDs
# folder='/home/ykupas/Documents/radar-gateway/records/replays-29dc8d/03_21_2025_09_58_41'
folder = sys.argv[1]

# CONFIDENCE = 0.999999
CONFIDENCE = float(sys.argv[2])

# array[target_id] = dict() (target_data)
target_map = dict()
current_detected_points = 0

count = 0
for f in os.listdir(folder):
    if os.path.isfile(os.path.join(folder, f)):
        count += 1

last_replay_count = count

# Main program
if __name__ == '__main__':

    # Main loop
    detected = 0
    not_detected = 0
    error = 0

    # Count detected, not detected and errors
    for i in range(1, last_replay_count):
        # print("")
        var = GetParsedFile(CONFIDENCE, folder + '/replay_' + str(i) + '.json')
        if var == 1:
            detected = detected+1
        elif var == -1:
            error = error+1
        else:
            not_detected = not_detected+1

    # Final print
    print("")
    print("Vezes que detectou numDetectedTracks:", detected, "de", last_replay_count)
    print("Vezes que não detectou numDetectedTracks", not_detected, "de", last_replay_count)
    print("Vezes que perdeu pacote:", error, "de", last_replay_count)
    pprint.PrettyPrinter(indent=4).pprint(target_map)


# - scatter plot para posições, com funcao de ver posição mudando com o tempo (provavelmente igual ao Industrial Toolbox"
# - plot para confidence level, numDetectedTracks