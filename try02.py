import cv2
from cv2 import circle
import numpy as np
import time

# lista das cameras disponiveis no sistema
#all_camera_idx_avaiable = []

# endereço da camera do celular através do app 'IP Webcam'
urlCamUsb = 'http://100.69.101.91:8080/video'
# pega a deep neural network do yolo
#net = cv2.dnn.readNet('yolov3_training_last.weights', 'yolov3_testing.cfg')

# versão do OpenCV que estamos usando para saber
# quais formas de chamar as funções
print("VERSAO: ", cv2.__version__)
'''for cameraId in range(10):
    cap = cv2.VideoCapture(cameraId)
    cap.set(3,1280)
    cap.set(4,1024)
    time.sleep(2)
    cap.set(15,-8.0)
    if cap.isOpened():
        print('Index da camera disponivel: ', cameraId)
        all_camera_idx_avaiable.append(cameraId)
        cap.release()
'''

# pega o vídeo do celular
cap = cv2.VideoCapture(urlCamUsb)
# se o vídeo nao estiver aberto
if not (cap.isOpened):
    print("Nao pude abrir a cameraa!")

#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# define circuloAnterior como none
circuloAnterior = None

# define a lambda que usaremos mais pra frente
dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2

# enquanto user nao digitar q (de quit)    
while(True):
    # lê os frames do vídeo
    ret, frame = cap.read()
    # converte o frame em escalas de cinza
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # ler os frames do video direto em escala de cinza
    #possible = cap.set(cv2.CAP_PROP_MODE, cv2.CAP_PROP_GIGA_FRAME_OFFSET_Y)
    #print(possible)
    # aplica um limite de nível fixo a cada elemento da matriz
#    ret2, thresh = cv2.threshold(possible,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # mostra o frame em uma janelinha
    cv2.imshow('frame', frame)
    # se user apertar q, finaliza a execução
    if cv2.waitKey(1) & 0XFF == ord('q'): 
        break
