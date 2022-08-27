#!/usr/bin/env python3
import cv2
import numpy as np

def noise_reduction(video):
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(3,3),0)
    return ret, frame
    
def sobel(frame):
    # Sobel Edge Detection
    edges = cv2.Sobel(src=frame, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection
    return edges

def canny(frame):
    # Canny Edge Detection
    edges = cv2.Canny(image=frame, threshold1=100, threshold2=200)
    return edges

def laplacian(frame):
    # Laplacian Edge Detection
    edges = cv2.Laplacian(frame,cv2.CV_64F)
    return edges

def circles_transform(frame):
    circles = cv2.HoughCircles(frame,cv2.HOUGH_GRADIENT,1,150,
                            param1=50,param2=30,minRadius=50,maxRadius=70)
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            #cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    return frame

if __name__ == '__main__':
    # caminho da camera usb
    urlCamUsb = "/dev/video0"
    # caminho do vídeo
    #urlCamUsb = "/home/marcos/reconhecimentoBordas/Testes_1/videos/painel_serviço_5.mp4"
    cap = cv2.VideoCapture(urlCamUsb)
    while(True):
        ret, frame = noise_reduction(cap)
        if not ret: break
        #frame = cv2.resize(frame, (540, 990))
        cv2.imshow('Sobel Edge Detection', frame)
        cv2.imshow('Sobel Edge Detection', sobel(frame))
        cv2.imshow('Canny Edge Detection', canny(frame))
        cv2.imshow('Laplacian Edge Detection', laplacian(frame))
        if cv2.waitKey(1) & 0XFF == ord('q'): 
            break
    cap.release()
    cv2.destroyAllWindows()
