import time

try:
    import RPi.GPIO as GPIO
    HARDWARE_DISPONIVEL = True
except ImportError:
    HARDWARE_DISPONIVEL = False

BUZZER_PIN = 18

def setup():
    if HARDWARE_DISPONIVEL:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUZZER_PIN, GPIO.OUT)
        GPIO.output(BUZZER_PIN, GPIO.LOW)

def tocar_buzzer(duracao=3.0):
    if HARDWARE_DISPONIVEL:
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(duracao)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
    else:
        print("[SIMULADO] Buzzer acionado por", duracao, "segundos")

def cleanup():
    if HARDWARE_DISPONIVEL:
        GPIO.cleanup()