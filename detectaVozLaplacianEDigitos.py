from unittest import result
import cv2
import numpy as np
from keras.models import load_model
import time
import getVoice

# lista das cameras disponiveis no sistema
#all_camera_idx_avaiable = []

# endereço da camera do celular através do app 'IP Webcam'
urlCamCel = 'http://192.168.0.26:8080/video'
# caminho da camera usb
urlCamUsb = "/dev/video4"

# loading pre trained model
model = load_model('model/digits.h5')

def predizFrame(frame, model):
    img_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_cinza = cv2.resize(img_cinza, (400,300))

    # mostra o box com o frame cortado e ampliado
    cv2.imshow("cortado2", img_cinza)
        
    img = cv2.resize(img_cinza, (28,28))
    img = img/255
    img = img.reshape(1,28,28,1)
    predict = model.predict(img)

    probabilidade = np.amax(predict)
    #    class_index = (model.predict(img) > 0.5).astype("int32")
    class_index = np.argmax(model.predict(img),axis=1)
    resultado = class_index[0]

    return resultado, probabilidade


# função para predizer os digitos
def prediction(frame, frame2, model, numProcura):

#    f = list()
 #   f.append(frame)
  #  f.append(frame2)
   # agora = 0

    probabilidade, resultado = predizFrame(frame, model)
    if probabilidade >= 0.99 and resultado == numProcura:
        print("ENCONTREI!")      

    if cv2.waitKey(1) & 0XFF == ord('p'): 
        getVoice.speak("TROCOU!")
    #    time.sleep(10)
        while probabilidade < 0.90 and resultado != numProcura:
            resultado = 0
            probabilidade = 0
#            print("proximo")
            probabilidade, resultado = predizFrame(frame2, model)
            mascara = cv2.Laplacian(frame2, cv2.CV_64F)
            cv2.imshow('boa', mascara)

        if probabilidade >= 0.99 and resultado == numProcura:
            print("ENCONTREI!")      
    
    # desenhar um circulo ao redor do botao encontrado  
#        marqued_img, circles_list = cortar_botoes.circles_detect(img_cortada, img_cinza)
 #       ciruclo_cortado = cortar_botoes.crop_button(circles_list, 1)
  #      cv2.imshow("detecta circulo", ciruclo_cortado)
   #     cortar_botoes.show_image(marqued_img)

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

# pega o andar
#num = getVoice.main()
num = 5
output = cv2.VideoWriter(
        "output.avi", cv2.VideoWriter_fourcc(*'MPEG'), 
      30, (1080, 1920))

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
#    mascara = cv2.Laplacian(frame, cv2.CV_64F)

    frame = cv2.rotate(frame, cv2.ROTATE_180)
    frame_backup = frame.copy        

    # mostra o frame original e o modificado em uma janelinha
    print('tamanho: ' + str(WIDTH))
    #cv2.rectangle(frame, (0, 0), (int(WIDTH), int(HEIGHT)), (0, 255, 0), 4)

#    cv2.rectangle(frame, (0, 0), (int(WIDTH//2), int(HEIGHT//2)), (0, 255, 0), 4)
 #   cv2.rectangle(frame, (int(WIDTH//2), 0), (int(WIDTH), int(HEIGHT//2)), (0, 255, 0), 4)

    bbox = [(0,0),
            (int(WIDTH//2), int(HEIGHT//2))]
    bbox2 = [(int(WIDTH//2), 0),
            (int(WIDTH), int(HEIGHT//2))]

    # corta a partir do frame quadrante 01
    img_cortada = frame[bbox[0][1]:bbox[1][1], bbox[0][0]:bbox[1][0]]
    img_cortada2 = frame[bbox2[0][1]:bbox2[1][1], bbox2[0][0]:bbox2[1][0]]
    resultado, probabilidade = prediction(img_cortada, img_cortada2, model, num)
    cv2.putText(img_cortada, f"Predicao: {resultado}", (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,255), 2,cv2.LINE_AA)
    cv2.putText(img_cortada, f"Probabilidade: {probabilidade}", (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,255),2, cv2.LINE_AA)
    print("RESULTADO: " + str(resultado))
    print("PROB: "+ str(probabilidade))
    # define a mascara
 #   mascara = cv2.Laplacian(img_cortada, cv2.CV_64F)

    cv2.rectangle(frame, (0, int(HEIGHT//2)), (int(WIDTH//2), int(HEIGHT)), (0, 255, 0), 4)
    cv2.rectangle(frame, (int(WIDTH//2), int(HEIGHT//2)), (int(WIDTH), int(HEIGHT)), (0, 255, 0), 4)

    output.write(frame)
#    cv2.imshow('frame', frame)
#    cv2.imshow('modificado', mascara)
    cv2.imshow('crop1', img_cortada)
    cv2.imshow('crop2', img_cortada2)


    if resultado == num and probabilidade >= 0.9999:
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