from cmath import pi
from fnmatch import translate
import numpy as np
import cv2

def getline(x0, y0, x1, y1):
    points = []

    if x0 > x1 :
        x0, x1 = x1, x0
        y0, y1 = y1, y0
        
    for x in range(x0, x1+1) :
        if x1==x0:
            y=y0
        else:
            y=int((x-x0)*(y1-y0)/(x1-x0)+y0)
        points.append((x,y))
      
    if y0 > y1 :
        x0, x1 = x1, x0
        y0, y1 = y1, y0
      
    for y in range(y0, y1+1) :
        if y1==y0:
            x=x0
        else :
            x=int((y-y0)*(x1-x0)/(y1-y0)+x0)
        points.append((x,y))
        
    return points

def drawLine(canvas, x0, y0, x1, y1, color=(255,255,255)) :
    if 1: 
        xys = getline(x0, y0, x1, y1) # contain the array of points along the line
        for xy in xys:
            x, y = xy
            canvas[y, x, :] = color
    else:
        cv2.line(canvas, (x0, y0), (x1, y1), color=tuple([int(c) for c in color]))
        #color=(int(color[0]),int(color[1]),int(color[2]))
    return 


def deg2rad(degree):
    rad = degree * np.pi / 180.
    return rad

def getRectangle(w,h):
    points = []
    points.append((0,0))
    points.append((0,h))
    points.append((w,h))
    points.append((w,0))
    points = np.array(points)
    return points

def drawLinePQ(canvas, p, q, color):
    drawLine(canvas, p[0], p[1], q[0], q[1], color)
    
def drawRectangle(canvas, pts, color) :
    for k in range(3) : 
         drawLine(canvas, pts[k,0], pts[k,1], pts[k+1,0], pts[k+1,1], color)
    drawLinePQ(canvas, pts[-1], pts[0], color)


def makeRmat(num, points, bottom_line) :  
    r = deg2rad(num)
    c = np.cos(r)
    s = np.sin(r)
    Rmat = np.zeros((2, 3))
    Rmat[0,0] = c
    Rmat[0,1] = -s
    Rmat[1,0] = s
    Rmat[1,1] = c
    Rmat[0,2] = bottom_line[0]*(1-c)+bottom_line[1]*s
    Rmat[1,2] = bottom_line[1]*(1-c)-bottom_line[0]*s
    return Rmat
      
def rotatePoints(degree, points, bottom_line):
    new_points = np.zeros((points.shape[0],3))
    for i in range(points.shape[0]):
        new_points[i] += np.concatenate((points[i],[1]))
        
    R = makeRmat(degree, points, bottom_line)
    qT = R @ new_points.T
    points = qT.T
    return points   

def makeTmat(tx, ty) :
    Tmat = np.zeros((2,3))
    Tmat[0,0] = 1
    Tmat[0,1] = 0
    Tmat[0,2] = tx
    Tmat[1,0] = 0
    Tmat[1,1] = 1
    Tmat[1,2] = ty
    return Tmat

def translatePoints(tx, ty, points):
    new_points = np.zeros((points.shape[0],3))
    for i in range(points.shape[0]):
        new_points[i] += np.concatenate((points[i],[1]))
    T = makeTmat(tx, ty)
    qT = T @ new_points.T
    new_points = qT.T
    return new_points

def getBottomLine(a, b, points) :
    #사각형의 a번째 꼭짓점과 b번째 꼭짓점의 중심을 반환한다.
    return [(points[a][0]+points[b][0])/2,(points[a][1]+points[b][1])/2]

def main():
    width, height = 1400, 800
    rec_width, rec_height = 50, 100
    canvas = np.zeros((height,width,3), dtype='uint8')

    theta_2, theta_3, theta_4, theta_5 = 0,0,0,0
    
    while True :
        canvas.fill(0) # canvas를 초기화하기
        cv2.putText(canvas, 'Press q,w,e,r - you can move arm to the right', (50,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(canvas, 'Press Q,W,E,R - you can move arm to the left', (50,120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
        if cv2.waitKeyEx() == 27 : #esc
            break
        elif cv2.waitKeyEx() == 113 : #q
            theta_2 += 2
        elif cv2.waitKeyEx() == 81 : #Q
            theta_2 -= 2
        elif cv2.waitKeyEx() == 119 : #w
            theta_3 += 4
        elif cv2.waitKeyEx() == 87 : #W
            theta_3 -= 4
        elif cv2.waitKeyEx() == 101 : #e
            theta_4 += 6
        elif cv2.waitKeyEx() == 69 : #E
            theta_4 -= 6
        elif cv2.waitKeyEx() == 114 : #r
            theta_5 += 8
        elif cv2.waitKeyEx() == 82 : #R
            theta_5 -= 8

        
        #draw rectangle_1
        points_r1 = getRectangle(rec_width,rec_height)
        points_r1 = translatePoints(width/2,height-rec_height-20,points_r1)
        points_r1 = points_r1.astype('int') # convert point float to integer
        drawRectangle(canvas, points_r1, (0,255,255))
        
        #draw rectangle_2       
        points_r2 = points_r1
        points_r2 = translatePoints(0,-rec_height,points_r2)
        bottom_line_r2 = getBottomLine(0,3,points_r1)
        points_r2 = rotatePoints(theta_2, points_r2,bottom_line_r2)
        points_r2 = points_r2.astype('int')
        drawRectangle(canvas, points_r2, (0,255,255))
        
        #draw rectangle_3
        points_r3 = points_r2
        points_r3 = translatePoints(0,-rec_height,points_r3)
        bottom_line_r3_1 = getBottomLine(0,3,points_r1)
        points_r3 = rotatePoints(theta_2, points_r3, bottom_line_r3_1)
        bottom_line_r3_2 = getBottomLine(0,3,points_r2)
        points_r3 = rotatePoints(theta_3, points_r3, bottom_line_r3_2)
        points_r3 = points_r3.astype('int')
        drawRectangle(canvas, points_r3, (0,255,255))
        
        #draw rectangle_4
        points_r4 = points_r3
        points_r4 = translatePoints(0,-rec_height,points_r4)
        bottom_line_r4_1 = getBottomLine(0,3,points_r1)
        points_r4 = rotatePoints(theta_2, points_r4, bottom_line_r4_1)
        bottom_line_r4_2 = getBottomLine(0,3,points_r2)
        points_r4 = rotatePoints(theta_3, points_r4, bottom_line_r4_2)
        bottom_line_r4_3 = getBottomLine(0,3,points_r3)
        points_r4 = rotatePoints(theta_4, points_r4, bottom_line_r4_3)
        points_r4 = points_r4.astype('int')
        drawRectangle(canvas, points_r4, (0,255,255))
        
        #draw rectangle_5
        points_r5 = points_r4
        points_r5 = translatePoints(0,-rec_height,points_r5)
        bottom_line_r5_1 = getBottomLine(0,3,points_r1)
        points_r5 = rotatePoints(theta_2, points_r5, bottom_line_r5_1)
        bottom_line_r5_2 = getBottomLine(0,3,points_r2)
        points_r5 = rotatePoints(theta_3, points_r5, bottom_line_r5_2)
        bottom_line_r5_3 = getBottomLine(0,3,points_r3)
        points_r5 = rotatePoints(theta_4, points_r5, bottom_line_r5_3)
        bottom_line_r5_4 = getBottomLine(0,3,points_r4)
        points_r5 = rotatePoints(theta_5, points_r5, bottom_line_r5_4)
        points_r5 = points_r5.astype('int')
        drawRectangle(canvas, points_r5, (0,255,255))
        
        cv2.imshow("my window", canvas)
        
    
if __name__ == "__main__":
    main()