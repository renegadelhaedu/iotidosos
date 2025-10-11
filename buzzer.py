from gpiozero import Buzzer
from time import sleep

# Define o buzzer na porta GPIO 17
buzzer = Buzzer(17)

print("Buzzer LIGADO por 1 segundo...")

buzzer.on()

# Espera 1 segundo
sleep(1)

print("Buzzer DESLIGADO.")

buzzer.off()