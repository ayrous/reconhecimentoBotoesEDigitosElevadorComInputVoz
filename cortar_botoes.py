#!/usr/bin/env python3
import numpy as np
import cv2

def image_reader():
    src_img = cv2.imread('/home/marcos/reconhecimentoBordas/Testes_1/images/painel_elevador5_1.jpg')
    gray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    blur_img = cv2.GaussianBlur(gray,(5,5),0)

    return src_img, blur_img

def circles_detect(src_img, blur_img):
    circles_img = cv2.HoughCircles(blur_img,cv2.HOUGH_GRADIENT,1,150,
                                param1=50,param2=30,minRadius=150,maxRadius=170)                      
    circles_img = np.uint16(np.around(circles_img))
    #sorted(circles_img , key=lambda k: [k[1], k[0]])
    #n = 9
    for (x, y, raio) in circles_img[0,:]:
        cv2.circle(src_img,(x, y), raio,(0,255,0),2)
        #n -= 1
        #number = str(n)
        #cv2.putText(src_img, number, (x, y), cv2.FONT_HERSHEY_COMPLEX, 6, (0, 255, 0), 4)
        

    return src_img, circles_img

def crop_button(circles_list, n):
    x = circles_list[0][n][0]
    y = circles_list[0][n][1]
    raio = circles_list[0][n][2]
    distancia = raio/12   #Relação em pixel/mm do tamanho do botão
    box_size = (100,150)
    maiorx = x - distancia*30 + box_size[0]
    menorx = x - distancia*30 - box_size[0]
    maiory = y + box_size[1] - 40
    menory = y - box_size[1] - 40
    edges = cv2.Laplacian(blur_img,cv2.CV_64F)
    cv2.rectangle(src_img, (int(menorx), int(menory)), (int(maiorx), int(maiory)), (0, 128, 255), 4)
    img_cortada = edges[int(menory):int(maiory), int(menorx):int(maiorx)]
    #cv2.imshow("cortado", img_cortada)
    return img_cortada

def show_image(image):
    image = cv2.resize(image, (540, 990))
    cv2.imshow('Detected Circles',image)


if __name__ == '__main__':
    src_img, blur_img = image_reader()
    marqued_img, circles_list= circles_detect(src_img, blur_img)
    cv2.imshow("cortado 0", crop_button(circles_list, 0))
    cv2.imshow("cortado 1", crop_button(circles_list, 1))
    cv2.imshow("cortado 2", crop_button(circles_list, 2))
    cv2.imshow("cortado 3", crop_button(circles_list, 3))
    cv2.imshow("cortado 4", crop_button(circles_list, 4))
    cv2.imshow("cortado 5", crop_button(circles_list, 5))
    cv2.imshow("cortado 6", crop_button(circles_list, 6))
    cv2.imshow("cortado 7", crop_button(circles_list, 7))
    cv2.imshow("cortado 8", crop_button(circles_list, 8))
    cv2.imshow("cortado 9", crop_button(circles_list, 9))
    show_image(marqued_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
