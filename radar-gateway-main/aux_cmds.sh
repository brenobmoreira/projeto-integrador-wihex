#!/bin/bash

ssh rasp-29dc8b@192.168.0.11
scp -r ../radar-gateway rasp-29dc8b@192.168.0.11:/home/rasp-29dc8b
sudo systemctl status rc-local

mosquitto_sub -h 34.59.162.139 -p 1883 -u briskcom -P Bbr1skc0m_2024 -t "application/#" -d
mosquitto_pub -h 34.59.162.139 -p 1883 -u briskcom -P Bbr1skc0m_2024 -t "application/update" -m "Olá mundo" -d
mosquitto_pub -h 34.59.162.139 -p 1883 -u briskcom -P Bbr1skc0m_2024 -t "application/reboot" -m "reset_a84041ffff29dc8e" -d

# Application python scripts
python radar-gateway/app/alarms.py 34.59.162.139 1883 radar1/alarm briskcom Bbr1skc0m_2024 application/update a84041ffff29dc8e 10 0.2 3 /dev/ttyUSB0
python radar-gateway/app/keepalive.py 34.59.162.139 1883 radar1/keepalive briskcom Bbr1skc0m_2024 a84041ffff29dc8e 60
python radar-gateway/app/wakeup.py 34.59.162.139 1883 radar1/wakeup briskcom Bbr1skc0m_2024 a84041ffff29dc8e
python radar-gateway/app/reboot.py 34.59.162.139 1883 radar1/reboot briskcom Bbr1skc0m_2024 a84041ffff29dc8e

# Static IP set
sudo nmcli c mod "Wired connection 1" ipv4.addresses 172.16.50.29/16 ipv4.method manual
sudo nmcli con mod "Wired connection 1" ipv4.gateway 172.16.50.1
sudo nmcli con mod "Wired connection 1" ipv4.dns 8.8.8.8
sudo nmcli c down "Wired connection 1" && sudo nmcli c up "Wired connection 1"
sudo nmcli -p connection show

# DCHP IP set
sudo nmcli con modify "Wired connection 1" ipv4.method auto
sudo nmcli c down "Wired connection 1" && sudo nmcli c up "Wired connection 1"
sudo nmcli -p connection show
