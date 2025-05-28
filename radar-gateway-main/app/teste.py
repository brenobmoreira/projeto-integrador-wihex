import serial

print(serial.__file__)  # mostra de onde está sendo importado
s = serial.Serial(port='COM3', baudrate=9600, timeout=1)
print("Conectado com sucesso!")
s.close()