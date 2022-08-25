from unittest import result
import cv2
import numpy as np
from keras.models import load_model
import getVoice

# lista das cameras disponiveis no sistema
#all_camera_idx_avaiable = []

# endereço da camera do celular através do app 'IP Webcam'
urlCamCel = 'http://192.168.0.26:8080/video'
# caminho da camera usb
urlCamUsb = "/dev/video4"

# loading pre trained model
model = load_model('model/digits.h5')

# função para predizer os digitos
def prediction(frame, model, numProcura):

    # box cortado
    bbox_size = (200,200)
    bbox = [(int(WIDTH//2 - bbox_size[0]//2),int(HEIGHT//2 - bbox_size[1]//2)),
            (int(WIDTH//2 + bbox_size[0]//2), int(HEIGHT//2 + bbox_size[1]//2))]

    # corta a partir do frame
    img_cortada = frame[bbox[0][1]:bbox[1][1], bbox[0][0]:bbox[1][0]]
    img_cinza = cv2.cvtColor(img_cortada, cv2.COLOR_BGR2GRAY)
    img_cinza = cv2.resize(img_cinza, (400,300))

    # mostra o box com o frame cortado e ampliado
    cv2.imshow("cortado", img_cinza)
    
    img = cv2.resize(img_cinza, (28,28))
    img = img/255
    img = img.reshape(1,28,28,1)
    predict = model.predict(img)

    probabilidade = np.amax(predict)
#    class_index = (model.predict(img) > 0.5).astype("int32")
    class_index = np.argmax(model.predict(img),axis=1)
    resultado = class_index[0]

    if probabilidade < 0.75:
        resultado = 0
        probabilidade = 0
    elif probabilidade >= 0.99 and resultado == numProcura:
        print("ENCONTREI!")      
        # desenhar um circulo ao redor do botao encontrado  
#        circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 1.2, 100, param1=100, param2=30, minRadius=75, maxRadius=400)
 #       img = cv2.circle(frame, )
        
    return resultado,probabilidade


# função para predizer os digitos
def desenhaCirculo(frame):

    # box cortado
    bbox_size = (120,120)
    bbox = [(int(WIDTH//2 - bbox_size[0]//2),int(HEIGHT//2 - bbox_size[1]//2)),
            (int(WIDTH//2 + bbox_size[0]//2), int(HEIGHT//2 + bbox_size[1]//2))]

    # corta a partir do frame
    img_cortada = frame[bbox[0][1]:bbox[1][1], bbox[0][0]:bbox[1][0]]
    img_cinza = cv2.cvtColor(img_cortada, cv2.COLOR_BGR2GRAY)
    img_cinza = cv2.resize(img_cinza, (200,200))
    # mostra o box com o frame cortado e ampliado
    cv2.imshow("cortado", img_cinza)



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

# pega o andar
num = getVoice.main()
# enquanto user nao digitar q (de quit)    
while(True):

    # lê os frames do vídeo
    ret, frame = cap.read()
    # para evitar ruidos e muitos pontos na img final
    frame_com_blur = cv2.GaussianBlur(frame, (5,5), 0)

    if not ret: break
    hsv = cv2.cvtColor(frame_com_blur, cv2.COLOR_BGR2HSV)
    testeThreshold = cv2.threshold(frame_com_blur, 128, 255, cv2.THRESH_TOZERO)

    # define as escalas de azul baixo e cima
    # para serem detectadas/amplificadas na mascara
    lower_blue = np.array([38,86,0])
    upper_blue = np.array([121,255,255])

    # amarelo
    lower_yellow = np.array([22, 93, 0], dtype='uint8')
    upper_yellow = np.array([45, 255, 255], dtype="uint8")
    
    # define a mascara
    mascara = cv2.Laplacian(frame, cv2.CV_64F)

    frame = cv2.rotate(frame, cv2.ROTATE_180)
    frame_backup = frame.copy        
    resultado, probabilidade = prediction(frame, model, num)
    cv2.putText(frame, f"Predicao: {resultado}", (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,255), 2,cv2.LINE_AA)
    cv2.putText(frame, f"Probabilidade: {probabilidade}", (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,255),2, cv2.LINE_AA)
    print("RESULTADO: " + str(resultado))
    print("PROB: "+ str(probabilidade))

    # mostra o frame original e o modificado em uma janelinha
    cv2.imshow('frame', frame)
    cv2.imshow('modificado', mascara)

    if resultado == num and probabilidade >= 1.0:
        getVoice.speak("Bora lá?")
        print("ENCONTREI CARA!")
        #desenha o circulo
        break

    # se user apertar q, finaliza a execução
    if cv2.waitKey(1) & 0XFF == ord('q'): 
        getVoice.speak("Até mais!")
        break

cap.release()
cv2.destroyAllWindows()