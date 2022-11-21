import numpy as np
import cv2
import time

def getRandomPosition(width, height, star_num=50):
    pos = []
    for i in range(star_num) :
        xinit = np.random.randint(0,width)
        yinit = np.random.randint(0,height)
        pos.append((xinit,yinit))
    return pos

def main():
    width, height = 1400, 800
    canvas = np.zeros((height,width,3), dtype='uint8')
    
    pos = getRandomPosition(width,height,30)
    delta = 0

    while True:
        if delta == 2 :
            canvas.fill(0)
            delta = 0
        else :
            delta += 1
            
        for p in pos :
            cv2.circle(canvas, (p[0], p[1]), delta, (255, 255, 255), -1)
        
        cv2.imshow("my window", canvas)
        if cv2.waitKey(20) == 27 : break
    
if __name__ == "__main__":
    main()