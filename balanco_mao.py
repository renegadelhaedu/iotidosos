import cv2
import numpy as np
from collections import deque
import requests
import time
ultimo_alerta = 0
COOLDOWN = 5

from exceptiongroup import catch

# Parâmetros ajustáveis
MAX_HISTORY = 30            # quantos frames manter no histórico
MIN_CONTOUR_AREA = 2500     # descartar blobs menores (ajustar)
DX_CHANGE_THRESHOLD = 30    # deslocamento mínimo para considerar uma mudança significativa (pixels)
SWINGS_REQUIRED = 5         # quantas mudanças de direção (vai/volta) para considerar um "balanço"
WINDOW_FPS = 30             # usado só para referência (não crítico)

HOST_PORTA = 'http://localhost:5000'

# Inicializa captura
cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(history=300, varThreshold=25, detectShadows=False)

centers = deque(maxlen=MAX_HISTORY)

def get_centroid_from_mask(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, None
    # pega maior contorno
    c = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(c)
    if area < MIN_CONTOUR_AREA:
        return None, None
    M = cv2.moments(c)
    if M["m00"] == 0:
        return None, None
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    return (cx, cy), c

def detect_waving(centers):
    # centers: deque de (x,y)
    if len(centers) < 4:
        return False
    xs = [c[0] for c in centers]
    # calc dx's entre frames consecutivos
    dxs = np.diff(xs)
    # filtra pequenos ruídos
    dxs_filtered = [d if abs(d) >= DX_CHANGE_THRESHOLD else 0 for d in dxs]
    # transform to signs: -1, 0, 1
    signs = [0 if d == 0 else (1 if d > 0 else -1) for d in dxs_filtered]
    # conta quantas vezes o sinal muda (ignora zeros)
    last = None
    changes = 0
    for s in signs:
        if s == 0:
            continue
        if last is None:
            last = s
        else:
            if s != last:
                changes += 1
                last = s
    # cada mudança representa metade de um ciclo (vai ou volta). arredondamos:
    return changes >= SWINGS_REQUIRED

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_small = cv2.resize(frame, (640, 480))  # processa em resolução reduzida para economia
    gray = cv2.cvtColor(frame_small, cv2.COLOR_BGR2GRAY)
    # aplique o background subtractor
    fgmask = fgbg.apply(gray)
    # limpeza morfológica
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel, iterations=1)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_DILATE, kernel, iterations=2)

    centroid, contour = get_centroid_from_mask(fgmask)
    if centroid is not None:
        centers.append(centroid)
        # desenha contorno + centro
        cv2.drawContours(frame_small, [contour], -1, (0,255,0), 2)
        cv2.circle(frame_small, centroid, 5, (0,0,255), -1)
    else:
        # mesmo sem detecção, mantemos histórico (pode preferir limpar)
        # centers.append(None)
        pass

    waving = detect_waving(centers)
    key2 = cv2.waitKey(1) & 0xFF
    if waving and (time.time() - ultimo_alerta > COOLDOWN) and key2 == 32:
        cv2.putText(frame_small, "AJUDAAA!", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        try:
            resp = requests.get(HOST_PORTA + '/alerta?id=1&tipo=gesto')
            print(resp)
            ultimo_alerta = time.time()
        except Exception as e:
            print(e)


    # mostrar histórico de posições
    #for i in range(1, len(centers)):
    #    cv2.line(frame_small, centers[i-1], centers[i], (255,0,0), 2)

    cv2.imshow("frame", frame_small)
    #cv2.imshow("fgmask", fgmask)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
