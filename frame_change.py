#!/usr/bin/env python3
import cv2
import numpy as np

def noise_reduction(video):
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    return ret, frame, blur

def crop_button(x1, x2, y1, y2):
    edges = cv2.Laplacian(blur,cv2.CV_64F)
    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 128, 255), 4)
    img_cortada = edges[int(y1):int(y2), int(x1):int(x2)]
    #cv2.imshow("cortado", img_cortada)
    return img_cortada

def show_image(image):
    image = cv2.resize(image, (540, 990))
    cv2.imshow('Detected Circles',image)

if __name__ == '__main__':
    # caminho da camera usb
    urlCamUsb = "/dev/video2"
    # caminho do vídeo
    #urlCamUsb = "/home/marcos/reconhecimentoBordas/Testes_1/videos/painel_serviço_1.mp4"
    cap = cv2.VideoCapture(urlCamUsb)
    WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frames_pose = {
            1:(100, WIDTH//2, 0, HEIGHT//4),
            2:(100, WIDTH//2, HEIGHT//4, HEIGHT//2),
            3:(100, WIDTH//2, HEIGHT//2, 3*HEIGHT//4),
            4:(100, WIDTH//2, 3*HEIGHT//4, HEIGHT),
            5:(WIDTH//2, WIDTH-100, 0, HEIGHT//4),
            6:(WIDTH//2, WIDTH-100, HEIGHT//4, HEIGHT//2),
            7:(WIDTH//2, WIDTH-100, HEIGHT//2, 3*HEIGHT//4),
            8:(WIDTH//2, WIDTH-100, 3*HEIGHT//4, HEIGHT)
        }
    key = 1
    while(True):
        ret, frame, blur = noise_reduction(cap)
        if not ret: break
        #frame = cv2.resize(frame, (540, 990))
        if cv2.waitKey(1) & 0XFF == ord('p'):
            key += 1
            if key >= 9 or key <=0:
                key = 1
        frame_cortado =  crop_button(frames_pose[key][0], frames_pose[key][1], frames_pose[key][2], frames_pose[key][3])
        cv2.imshow('Frame cortado', frame_cortado)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0XFF == ord('q'): 
            break
    cap.release()
    cv2.destroyAllWindows()
