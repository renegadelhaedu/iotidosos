from gpiozero import Buzzer
from time import sleep

buzzer = Buzzer(17)  # use o número do pino GPIO, não o físico

for i in range(3):
    buzzer.on()
    sleep(1)
    buzzer.off()
    sleep(1)
