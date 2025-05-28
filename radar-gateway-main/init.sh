#!/bin/sh


RASP_USER=rasp-29dc8b


BROKER_IP=34.59.162.139
BROKER_PORT=1883
CLIENT_ID=radar1
USER=briskcom
PASS=Bbr1skc0m_2024
TOPIC=application/update


GW_EUI=a84041ffff29dc8b
GW_KEEPALIVE_T=60


EP_EUI=a84041ffff29dc8c
EP_KEEPALIVE_T=600
EP_RESET_T=10
EP_READ_T=0.2
EP_READ_N=3


echo "Testando conexão com a internet inicialmente..."
MAX_RETRIES=300 # Número máximo de tentativas
SLEEP_TIME=2 # Tempo entre tentativas (em segundos)
attempt=0 # Contador de tentativas
while (( attempt < MAX_RETRIES )); do
    if ping -c 1 -W $SLEEP_TIME $BROKER_IP > /dev/null 2>&1; then
        echo "Conexão estabelecida! Continuando..."
        break
    else
        echo "Falha na conexão. Tentativa $((attempt + 1)) de $MAX_RETRIES..."
        ((attempt++))
        sleep $SLEEP_TIME
    fi
done
if (( attempt == MAX_RETRIES )); then
    echo "Não foi possível estabelecer conexão após $MAX_RETRIES tentativas."
    reboot
    exit 1
fi


# Radar sensor application in python scripts
APP_DIR=/home/$RASP_USER/radar-gateway/app
python $APP_DIR/wakeup.py $BROKER_IP $BROKER_PORT $CLIENT_ID/wakeup $USER $PASS $EP_EUI &
sleep 1
python $APP_DIR/keepalive.py $BROKER_IP $BROKER_PORT $CLIENT_ID/keepalivegw $USER $PASS $GW_EUI $GW_KEEPALIVE_T &
sleep 1
python $APP_DIR/keepalive.py $BROKER_IP $BROKER_PORT $CLIENT_ID/keepaliveep $USER $PASS $EP_EUI $EP_KEEPALIVE_T &
sleep 1
python $APP_DIR/alarms.py $BROKER_IP $BROKER_PORT $CLIENT_ID/alarm0 $USER $PASS $TOPIC/alarm0 $EP_EUI $EP_RESET_T $EP_READ_T $EP_READ_N /dev/ttyUSB0 &
sleep 1
python $APP_DIR/alarms.py $BROKER_IP $BROKER_PORT $CLIENT_ID/alarm1 $USER $PASS $TOPIC/alarm1 $EP_EUI $EP_RESET_T $EP_READ_T $EP_READ_N /dev/ttyUSB1 &
sleep 1
python $APP_DIR/alarms.py $BROKER_IP $BROKER_PORT $CLIENT_ID/alarm2 $USER $PASS $TOPIC/alarm2 $EP_EUI $EP_RESET_T $EP_READ_T $EP_READ_N /dev/ttyUSB2 &
sleep 1
python $APP_DIR/reboot.py $BROKER_IP $BROKER_PORT $CLIENT_ID/reboot $USER $PASS $EP_EUI &
sleep 1


echo "Testando conexão com a internet constantemente..."
CHECK_NET=30 # Tempo entre tentativas (em segundos)
while (( 1 )); do
    if ping -c 1 -W $CHECK_NET $BROKER_IP > /dev/null 2>&1; then
        echo "Conexão estabelecida! Continuando..."
        break
    else
        echo "Falha na conexão. Reboot..."
        reboot
    fi
done
