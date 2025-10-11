from gpiozero import Buzzer
from time import sleep

buzzer = Buzzer(17)

for i in range(5):
    buzzer.on()
    sleep(1)
    buzzer.off()