import cv2
from cv2 import circle
import numpy as np
import time

# lista das cameras disponiveis no sistema
#all_camera_idx_avaiable = []

# endereço da camera do celular através do app 'IP Webcam'
urlCamCel = 'http://192.168.15.2:8080/video'
# caminho da camera usb
urlCamUsb = "/dev/video4"

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
    if not ret: break
    # converte o frame em escalas de cinza
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # dá um blir no frame
    blur_frame = cv2.GaussianBlur(gray_frame, (17,17),0)

    # define circulos
    circles = cv2.HoughCircles(blur_frame, cv2.HOUGH_GRADIENT, 1.2, 100, param1=100, param2=30, minRadius=75, maxRadius=400)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        escolhido = None

        for i in circles[0,:]:
            if escolhido is None: escolhido=i
            if circuloAnterior is not None:
                if dist(escolhido[0], escolhido[1], circuloAnterior[0], circuloAnterior[1]) <= dist(i[0], i[1], circuloAnterior[0], circuloAnterior[1]):
                    escolhido = i
        
        cv2.circle(frame, (escolhido[0], escolhido[1]), 1, (0,100,100), 3)
        cv2.circle(frame, (escolhido[0], escolhido[1]), escolhido[2], (255,0,255), 3)
        circuloAnterior = escolhido
    # mostra o frame em uma janelinha
    cv2.imshow('frame', frame)
    # se user apertar q, finaliza a execução
    if cv2.waitKey(1) & 0XFF == ord('q'): 
        break

cap.release()
cv2.destroyAllWindows()