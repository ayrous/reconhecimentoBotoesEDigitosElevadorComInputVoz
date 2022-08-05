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
    # para evitar ruidos e muitos pontos na imsg final
    frame_com_blur = cv2.GaussianBlur(frame, (5,5), 0)

    if not ret: break
    hsv = cv2.cvtColor(frame_com_blur, cv2.COLOR_BGR2HSV)

    # define as escalas de azul baixo e cima
    # para serem detectadas/amplificadas na mascara
    lower_blue = np.array([38,86,0])
    upper_blue = np.array([121,255,255])

    # define a mascara
    mascara = cv2.inRange(hsv, lower_blue, upper_blue)

    # função que vai nos retornar 2 valores, sendo o primeiro o contorno
    # o 3 nao precisamos e ent chamaremos de _
    # pegar o contorno das areas brancas mostradas na mascara
    contornos, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #print(contornos)
    # desenhar os contornos
    cv2.drawContours(frame, contornos, -1, (0, 255, 0), 3)


    # mostra o frame original em uma janelinha
    cv2.imshow('frame', frame)
    cv2.imshow('modificado', mascara)
    # se user apertar q, finaliza a execução
    if cv2.waitKey(1) & 0XFF == ord('q'): 
        break

cap.release()
cv2.destroyAllWindows()