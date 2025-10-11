from time import sleep

def apitar():

    try:
        from gpiozero import Buzzer
        from gpiozero.devices import Device, BadPinFactory

        try:
            Device.pin_factory.close()
        except Exception:
            # Ignora o erro se a fábrica de pinos não estiver aberta
            pass

            # Garante que o GPIO Zero inicie o acesso no NOVO processo
        Device.ensure_pin_factory()

        buzzer = Buzzer(17)

        for i in range(3):
            buzzer.on()
            sleep(1)
            buzzer.off()
            sleep(1)

    except ImportError:
        try:
            import RPi.GPIO as GPIO

            BUZZER_PIN = 17

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(BUZZER_PIN, GPIO.OUT)


            for i in range(5):
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                sleep(1)
                GPIO.output(BUZZER_PIN, GPIO.LOW)


            GPIO.cleanup()

        except ImportError:
            print("ERRO: Nenhuma biblioteca GPIO (gpiozero ou RPi.GPIO) encontrada. Executando em modo 'dummy'.")

