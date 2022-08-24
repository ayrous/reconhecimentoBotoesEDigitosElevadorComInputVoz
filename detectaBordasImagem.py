from unittest import result
import cv2
import numpy as np
from keras.models import load_model

# lista das cameras disponiveis no sistema
# all_camera_idx_avaiable = []

# endereço da camera do celular através do app 'IP Webcam'
urlCamCel = 'http://192.168.0.26:8080/video'
# caminho da camera usb
urlCamUsb = "/dev/video4"

# imagem
srcImg = ""

# loading pre trained model
model = load_model('model/digits.h5')

# função para predizer os digitos
def prediction(frame):

    # box cortado
    bbox_size = (80,80)
    bbox = [(int(WIDTH//2 - bbox_size[0]//2),int(HEIGHT//2 - bbox_size[1]//2)),
            (int(WIDTH//2 + bbox_size[0]//2), int(HEIGHT//2 + bbox_size[1]//2))]

    # corta a partir do frame
    img_cortada = frame[bbox[0][1]:bbox[1][1], bbox[0][0]:bbox[1][0]]
    img_cinza = cv2.cvtColor(img_cortada, cv2.COLOR_BGR2GRAY)
    img_cinza = cv2.resize(img_cinza, (400,300))
    # 200 200

    # Sobel Edge Detection
    sobelx = cv2.Sobel(src=img_cinza, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
    sobely = cv2.Sobel(src=img_cinza, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
    sobelxy = cv2.Sobel(src=img_cinza, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection

    # Canny Edge
    edges = cv2.Canny(image=img_cinza, threshold1=100, threshold2=200) # Canny Edge Detection

    cv2.imshow("Sobel x edge", sobelx)
    cv2.imshow("canny edge", edges)

    return sobelx,sobely, sobelxy

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

    frame = cv2.rotate(frame, cv2.ROTATE_180)
    frame_backup = frame.copy        
    sobelx, sobely, sobelxy = prediction(frame)
    cv2.putText(frame, f"Sobel x: {sobelx}", (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,255), 2,cv2.LINE_AA)
    cv2.putText(frame, f"Sobel y: {sobely}", (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,255),2, cv2.LINE_AA)


    # mostra o frame original e o modificado em uma janelinha
    cv2.imshow('frame', frame)
#    cv2.imshow('modificado', mascara)

    # se user apertar q, finaliza a execução
    if cv2.waitKey(1) & 0XFF == ord('q'): 
        break

cap.release()
cv2.destroyAllWindows()

