#!/usr/bin/env python3
import cv2
import numpy as np
import getVoice
from keras.models import load_model

# loading pre trained model
model = load_model('model/digits.h5')

def noise_reduction(video):
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    return ret, frame, blur

def crop_button(x1, x2, y1, y2):
    #edges = cv2.Laplacian(blur,cv2.CV_64F)
    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 128, 255), 4)
    img_cortada = blur[int(y1):int(y2), int(x1):int(x2)]
    #cv2.imshow("cortado", img_cortada)
    return img_cortada


def prediction(frame_cortado, model, numProcura):

#    img_cinza = cv2.cvtColor(frame_cortado, cv2.COLOR_BGR2GRAY)
    img_corte = cv2.resize(frame_cortado, (400,300))

    # mostra o box com o frame cortado e ampliado
    cv2.imshow("cortado", img_corte)
    
    img = cv2.resize(img_corte, (28,28))
    img = img/255
    img = img.reshape(1,28,28,1)
    predict = model.predict(img)
 #   cv2.imshow("cortado2", img)

    probabilidade = np.amax(predict)
    class_index = np.argmax(model.predict(img),axis=1)
    resultado = class_index[0]

    if probabilidade < 0.75:
        resultado = 0
        probabilidade = 0
    elif probabilidade >= 0.95 and int(resultado) == int(numProcura):
        print("ENCONTREI!")      
        # desenhar um circulo ao redor do botao encontrado  
#        circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 1.2, 100, param1=100, param2=30, minRadius=75, maxRadius=400)
 #       img = cv2.circle(frame, )
        
    return resultado,probabilidade

def show_image(image):
    image = cv2.resize(image, (540, 990))
    cv2.imshow('Detected Circles',image)

if __name__ == '__main__':

    num = getVoice.main()
    getVoice.speak('Vamos até o '+ str(num))

    # caminho da camera usb
    urlCamUsb = "/dev/video4"
    # caminho do vídeo
    urlVideoTeste = "videos/painel_elevador5_1.mp4"
    urlCelUsb = 'http://192.168.15.2:8080/video'

    cap = cv2.VideoCapture(urlVideoTeste)
    WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    frames_pose = {
            1:(100, WIDTH//2 -50, 0, HEIGHT//4),
            2:(100, WIDTH//2 -50, HEIGHT//4, HEIGHT//2),
            3:(100, WIDTH//2 -50, HEIGHT//2, 3*HEIGHT//4),
            4:(100, WIDTH//2 -50, 3*HEIGHT//4, HEIGHT),
            5:(WIDTH//2, WIDTH-150, 0, HEIGHT//4),
            6:(WIDTH//2, WIDTH-150, HEIGHT//4, HEIGHT//2),
            7:(WIDTH//2, WIDTH-150, HEIGHT//2, 3*HEIGHT//4),
            8:(WIDTH//2, WIDTH-150, 3*HEIGHT//4, HEIGHT)
        }
    key = 1


    while(True):
        ret, frame, blur = noise_reduction(cap)
        if not ret: break
       # frame = cv2.resize(frame, (500, 700))
        frame = cv2.rotate(frame, cv2.ROTATE_180)

        if cv2.waitKey(1) & 0XFF == ord('p'):
            key += 1
            if key >= 9 or key <=0:
                key = 1

        frame_cortado =  crop_button(frames_pose[key][0], frames_pose[key][1], frames_pose[key][2], frames_pose[key][3])
        frame_cortado = cv2.rotate(frame_cortado, cv2.ROTATE_180)
        #img_cinza = cv2.cvtColor(frame_cortado, cv2.COLOR_BGR2GRAY)

        resultado, probabilidade = prediction(frame_cortado, model, int(num))
        cv2.putText(frame_cortado, f"Predicao: {resultado}", (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,255), 2,cv2.LINE_AA)
        cv2.putText(frame_cortado, f"Probabilidade: {probabilidade}", (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,255),2, cv2.LINE_AA)
        print("RESULTADO: " + str(resultado))
        print("PROB: "+ str(probabilidade))

        cv2.imshow('Frame cortado', frame_cortado)
        cv2.imshow('Frame', frame)

        if resultado == num and probabilidade >= 0.999:
            getVoice.speak("Bora lá?")
            print("ENCONTREI CARA!")
            #desenha o circulo
            break


        if cv2.waitKey(1) & 0XFF == ord('p'):
                key += 1
                
                if key >= 9 or key <=0:
                    getVoice.speak("Até mais!")
                    break
                else: 
                    getVoice.speak("Trocou de quadrante")
          

    cap.release()
    cv2.destroyAllWindows()