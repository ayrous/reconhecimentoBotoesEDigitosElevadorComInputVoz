import cv2
import numpy as np
import time

# lista das cameras disponiveis no sistema
#all_camera_idx_avaiable = []

# endereço da camera do celular através do app 'IP Webcam'
urlCamUsb = 'http://100.69.101.91:8080/video'
# pega a deep neural network do yolo
net = cv2.dnn.readNet('yolov3_training_last.weights', 'yolov3_testing.cfg')

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


# enquanto user nao digitar q (de quit)    
while(True):
    # lê os frames do vídeo
    ret, frame = cap.read()
    # mostra o frame em uma janelinha
    cv2.imshow('frame', frame)
    # se user apertar q, finaliza a execução
    if cv2.waitKey(1) & 0XFF == ord('q'): 
        break
