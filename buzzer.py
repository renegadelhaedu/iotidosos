import time

def apitar():

    try:
        from gpiozero import Buzzer

        buzzer = Buzzer(17)

        for i in range(5):
            buzzer.on()
            time.sleep(1)
            buzzer.off()
            time.sleep(1)

    except ImportError:
        try:
            import RPi.GPIO as GPIO

            BUZZER_PIN = 17

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(BUZZER_PIN, GPIO.OUT)


            for i in range(5):
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(BUZZER_PIN, GPIO.LOW)


            GPIO.cleanup()

        except ImportError:
            print("ERRO: Nenhuma biblioteca GPIO (gpiozero ou RPi.GPIO) encontrada. Executando em modo 'dummy'.")


if __name__ == '__main__':
    apitar()