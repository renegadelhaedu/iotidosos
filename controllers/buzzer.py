import time

try:
    from gpiozero import Buzzer

    BUZZER_PIN = 17 #coloque na gpio 17 da rasp o positivo
    buzzer_device = Buzzer(BUZZER_PIN)


    def tocar_buzzer():
        buzzer_device.on()
        time.sleep(1)
        buzzer_device.off()


except ImportError:
    try:
        import RPi.GPIO as GPIO

        BUZZER_PIN = 17

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUZZER_PIN, GPIO.OUT)


        def tocar_buzzer():
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)


        def cleanup_gpio():
            GPIO.cleanup()

    except ImportError:
        print("ERRO: Nenhuma biblioteca GPIO (gpiozero ou RPi.GPIO) encontrada. Executando em modo 'dummy'.")


def main():
    print("Iniciando o sistema...")

    try:
        # Chama a função que foi definida dinamicamente
        tocar_buzzer()
        time.sleep(2)
        tocar_buzzer()

    except Exception as e:
        print(f"Ocorreu um erro durante a execução: {e}")

    finally:
        # Garante que o cleanup seja chamado no final
        cleanup_gpio()
        print("Sistema finalizado.")


if __name__ == "__main__":
    main()