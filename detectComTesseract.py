from unittest import result
import cv2
import numpy as np
from keras.models import load_model
from pytesseract import pytesseract

# lista das cameras disponiveis no sistema
#all_camera_idx_avaiable = []

# endereço da camera do celular através do app 'IP Webcam'
urlCamCel = 'http://192.168.15.2:8080/video'
# caminho da camera usb
urlCamUsb = "/dev/video4"

# loading pre trained model
model = load_model('model/digits.h5')

# função para predizer os digitos
def prediction(frame):
    caminho_tesseract = r"/Tesseract-OCR/teressact.exe"
    pytesseract.tesseract_cmd = caminho_tesseract

    imgH ,imgW,_ = frame.shape
    x1,y1,w1,h1 = 0,0,imgH ,imgW
    imgchar = pytesseract.image_to_string(frame)
    imgboxes =  pytesseract.image_to_boxes(frame)
    for boxes in imgboxes.splitlines():
        boxes = boxes.split(' ')
        x,y,w,h = int(boxes[1]),int(boxes[2]),int(boxes[3]),int(boxes[4])
        cv2.rectangle(frame,(x,imgH-y),(w,imgH-h),(0,0,255),3)
        cv2.putText(frame,imgchar,(x1 +int(w1/50),y1+int(h1/50)),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2) 
        
        cv2.imshow('text',frame)    
    
    return resultado,probabilidade

# versão do OpenCV que estamos usando para saber
# quais formas de chamar as funções
print("VERSAO: ", cv2.__version__)

# pega o vídeo do celular
cap = cv2.VideoCapture(urlCamUsb)
WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# se o vídeo nao estiver aberto
if not (cap.isOpened):
    print("Nao pude abrir a cameraa!")

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

    # em cada um dos contornos verifica a area
    for contorno in contornos:
        area = cv2.contourArea(contorno)

        # se a area do contorno for mtt pequena,
        # mt provavelmente é ruído
        if area > 100:
            # desenha cada contorno
            cv2.drawContours(frame, contorno, -1, (0, 255, 0), 3)

    prediction(frame)

    # mostra o frame original e o modificado em uma janelinha
    cv2.imshow('frame', frame)
    cv2.imshow('modificado', mascara)

    # se user apertar q, finaliza a execução
    if cv2.waitKey(1) & 0XFF == ord('q'): 
        break

cap.release()
cv2.destroyAllWindows()

