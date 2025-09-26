import pygame
import os  # Importar 'os' para definir a variável de ambiente


def tocar_som(caminho_arquivo):
    # --- NOVO: Forçar o uso do driver ALSA ---
    # Isso pode resolver o erro "Couldn't open audio device"
    os.environ['SDL_AUDIODRIVER'] = 'alsa'

    # É uma boa prática iniciar o mixer com uma frequência e tamanho de buffer específicos
    # Padrões comuns: frequência 44100 ou 48000
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
    except pygame.error as e:
        print(f"Erro ao inicializar o mixer: {e}")
        print("Tente garantir que você não está usando o usuário root e que tem permissão para o áudio.")
        return  # Sai da função se a inicialização falhar

    # O resto do seu código permanece o mesmo
    pygame.mixer.music.load(caminho_arquivo)
    pygame.mixer.music.play(0)

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Desinicializa o mixer após o uso para liberar o dispositivo
    pygame.mixer.quit()


tocar_som('lulu.mp3')