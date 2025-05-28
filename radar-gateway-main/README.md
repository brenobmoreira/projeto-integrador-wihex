# radar-gateway

O projeto consiste em uma Raspberry Pi 3 B+ funcionando como um gateway e endpoint LoRa para detectar pessoas utilizando os sensores de radar e mandar alarmes para o servidor da plataforma. A Raspberry imita um gateway e um endpoint LoRa ao enviar seus pacotes para o MQTT Broker. É necessário um cartão SD de 16GB com a imagem da Raspberry Pi OS Lite (32-bit). Utilizando o software [Raspberry Pi Imager](https://www.raspberrypi.com/news/raspberry-pi-imager-imaging-utility/), é possível já configurar a imagem com as seguintes características:

* **HOSTNAME**: rasp-XXXXXX (final do DevEUI do gateway LoRa que a Rasp representa)  
* **SSH**: Habilitado com autenticação por *password*   
* **USERNAME**: rasp-XXXXXX (mesmo do hostname)  
* **PASSWORD**: Br1sKc0N!  

## Criando a imagem da Raspberry Pi 3B+

Após criar a imagem em um cartão SD, iniciar a Rasp conectada a um roteador. É necessário acessar o roteador para descobrir qual IPv4 o DHCP atrelou a Rasp, para assim poder acessá-la via SSH, podendo assim conectar o dispositivo em algum Wi-Fi através do comando `sudo raspi-config`. 

## Parâmetros e pré-requisitos

Baixado os arquivos do repositório em uma máquina local conectada a mesma rede que a Rasp, deve-se editar as configurações nos arquivos `rc.local` e `init.sh` (seguir os comentários dos arquivos como referência). Os parâmetros necessários são apresentados a seguir:

**Gateway Dev-EUI**: Endereço EUI que imita um gateway.
**Endpoint Dev-EUI**: Endereço EUI que imita um endpoint.
**MQTT Broker IP**: Endereço IP do MQTT Broker da aplicação.
**MQTT Broker User**: Usuário necessário para interagir com o MQTT Broker.
**MQTT Broker Pass**: Senha necessária para interagir com o MQTT Broker.
**T**: Tempo entre leituras dos sensores. 
**N**: Vezes necessárias de detecções para alertar a plataforma.

Após editar os arquivos locais, é necessaria enviar os arquivos para Rasp via SSH. Para enviar os arquivos para Rasp, deve-se executar o comando:

```
sshpass -p "PASSWORD" scp -r ../radar-gateway HOSTNAME@IPv4:/home/USERNAME
```

Com o acesso realizado a Rasp via SSH e os arquivos copiados, é necessário realizar os seguintes comandos para instalar todos os requisitos:

```
sudo apt-get update
sudo apt-get install libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev rng-tools python3-pip
pip3 install --force-reinstall -v "numpy==1.22.1" --break-system-packages
sudo pip3 install --force-reinstall -v "numpy==1.22.1" --break-system-packages
pip3 install --force-reinstall -v "pyserial==3.5" --break-system-packages
sudo pip3 install --force-reinstall -v "pyserial==3.5" --break-system-packages
pip3 install --force-reinstall -v "json-fix==1.0.0" --break-system-packages
sudo pip3 install --force-reinstall -v "json-fix==1.0.0" --break-system-packages
pip3 install --force-reinstall -v "paho-mqtt==1.6.1" --break-system-packages
sudo pip3 install --force-reinstall -v "paho-mqtt==1.6.1" --break-system-packages
pip3 install --force-reinstall --break-system-packages ntplib
sudo pip3 install --force-reinstall --break-system-packages ntplib
sudo cp radar-gateway/rc.local /etc/rc.local
sudo chmod 777 /etc/rc.local
sudo chmod 777 radar-gateway/init.sh
sudo systemctl start rc-local.service
sudo reboot
```