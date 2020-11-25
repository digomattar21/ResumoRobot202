#!/usr/bin/python
#-*- coding:utf-8 -*-

'''
This example illustrates how to use Hough Transform to find lines

Usage:
    houghlines.py [<image_name>]
    image argument defaults to ./box.png
'''

# Python 2/3 compatibility
from __future__ import print_function

import cv2
import numpy as np
import sys
import math

if __name__ == '__main__':
    print(__doc__)

    try:
        fn = sys.argv[1]
    except IndexError:
        fn = "./arduino_capa.png"

    src = cv2.imread(fn)
    dst = cv2.Canny(src, 50, 200) # aplica o detector de bordas de Canny à imagem src
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR) # Converte a imagem para BGR para permitir desenho colorido

    if True: # HoughLinesP
        lines = cv2.HoughLinesP(dst, 10, math.pi/180.0, 100, np.array([]), 5, 5)
        print("Used Probabilistic Rough Transform")
        print("The probabilistic hough transform returns the end points of the detected lines")
        a,b,c = lines.shape
        print("Valor de A",a, "valor de lines.shape", lines.shape)

        m = []
        right = []
        left = []
        maior_dir = []
        maior_esq = []
        maior = 0
        m1=0
        m2=0
        x_intercept=0
        h1=0
        h2=0

        for i in range(a):
            # Faz uma linha ligando o ponto inicial ao ponto final, com a cor vermelha (BGR)
            #cv2.line(cdst, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
            if (lines[i][0][2]-lines[i][0][0]) != 0:
                slope = ((float(lines[i][0][3])-float(lines[i][0][1]))/(float(lines[i][0][2])-float(lines[i][0][0])))
                tamanho =  math.sqrt((float(lines[i][0][3])+float(lines[i][0][1]))**2 + (float(lines[i][0][2])+float(lines[i][0][0]))**2)
            else:
                slope = 100000


            if (-1.5 < slope< -0.4) and 400<tamanho<1000:
                m1 = slope
                h1 = ((float(lines[i][0][1]))-m1*float(lines[i][0][0]))

                cv2.line(cdst, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 255, 0), 3, cv2.LINE_AA)
                left.append(m1)
                    
            elif (1.0 < slope< 2.71) and 700<tamanho<1300:
                m2=slope
                h2 = ((float(lines[i][0][1]))-m2*float(lines[i][0][0]))

                cv2.line(cdst, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (255, 0, 0), 3, cv2.LINE_AA)
                right.append(m2)
                

            if (m1-m2)!=0:
                x_intercept = int((h2-h1)/m1-m2)
            
            y_intercept = int(m1*x_intercept+h1)

            if x_intercept in range(300,400) and y_intercept in range(40,100):
                cv2.circle(cdst,(x_intercept,y_intercept),10,(0,0,255),-1)
            

            
    else:    # HoughLines
        # Esperemos nao cair neste caso
        lines = cv2.HoughLines(dst, 1, math.pi/180.0, 50, np.array([]), 0, 0)
        a,b,c = lines.shape
        for i in range(a):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0, y0 = a*rho, b*rho
            pt1 = ( int(x0+1000*(-b)), int(y0+1000*(a)) )
            pt2 = ( int(x0-1000*(-b)), int(y0-1000*(a)) )
            cv2.line(cdst, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)
        print("Used old vanilla Hough transform")
        print("Returned points will be radius and angles")

    cv2.imshow("source", src)
    cv2.imshow("detected lines", cdst)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        False
    cv2.waitKey(0)