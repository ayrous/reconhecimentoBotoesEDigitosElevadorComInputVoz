import cv2
from cv2 import circle
import numpy as np
import time

# lista das cameras disponiveis no sistema
#all_camera_idx_avaiable = []

# endereço da camera do celular através do app 'IP Webcam'
urlCamCel = 'http://192.168.15.2:8080/video'
# caminho da camera usb
urlCamUsb = "/dev/video5"

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

    gray = cv2.cvtColor(frame_com_blur,cv2.COLOR_BGR2GRAY)
    ret2, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)
    
    # define marcadores
    # Marker labelling
    ret, marcadores = cv2.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    marcadores = marcadores+1
    # Now, mark the region of unknown with zero
    marcadores[unknown==255] = 0

    marcadores = cv2.watershed(frame_com_blur,marcadores)
    frame_com_blur[marcadores == -1] = [255,0,0]
 

    # mostra o frame original em uma janelinha
    cv2.imshow('frame', frame)
    cv2.imshow('modificado', frame_com_blur)
    # se user apertar q, finaliza a execução
    if cv2.waitKey(1) & 0XFF == ord('q'): 
        break

cap.release()
cv2.destroyAllWindows()