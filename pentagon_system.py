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

def getRegularNGon(ngon):
    delta = 360. / ngon
    points = []
    for i in range(ngon):
        degree = i * delta
        radian = deg2rad(degree)
        x = np.cos(radian) 
        y = np.sin(radian) 
        points.append((x,y))
    points = np.array(points)
    return points

def drawLinePQ(canvas, p, q, color):
    drawLine(canvas, p[0], p[1], q[0], q[1], color)
    
def drawPolygon(canvas, pts, color, axis=False) :
    for k in range(pts.shape[0]-1) : #the number of ngon
         drawLine(canvas, pts[k,0], pts[k,1], pts[k+1,0], pts[k+1,1], color)
    drawLinePQ(canvas, pts[-1], pts[0], color)
    
    if axis == True: # center - pts[0]
        center = np.array([0.,0])
        for p in pts:
            center += p
        center = center / pts.shape[0]
        center = center.astype('int')
        drawLinePQ(canvas, center, pts[0], color)


def makeRmat(num) :
    r = deg2rad(num)
    c = np.cos(r)
    s = np.sin(r)
    Rmat = np.zeros((2,2))
    Rmat[0,0] = c
    Rmat[0,1] = -s
    Rmat[1,0] = s
    Rmat[1,1] = c
    return Rmat
      
def rotatePoints(degree, points):
    R = makeRmat(degree)
    qT = R @ points.T
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

def main():
    width, height = 1400, 800
    canvas = np.zeros((height,width,3), dtype='uint8')
    degree_p, degree_t = 0, 0
    
    while True :
        canvas.fill(0) # canvas를 초기화하기
        
        #pentagon의 theta
        if degree_p == 360 :
            degree_p = 0
        else :
            degree_p += 1
            
        #triangle의 theta
        if degree_t == 360.:
            degree_t = 0.
        else :
            degree_t += 0.05
        
        #draw pentagon
        points_p = getRegularNGon(5)  
        points_p = rotatePoints(degree_p, points_p)
        points_p = points_p * 100 # magnify the shape
        points_p = translatePoints(width/2,height/2,points_p)
        points_p = points_p.astype('int') # convert point float to integer
        drawPolygon(canvas, points_p, (0,255,255), 1)
        
        #draw triangle
        points_t = getRegularNGon(3)
        points_t = rotatePoints(degree_p, points_t)
        points_t = points_t * 30
        points_t = translatePoints(width/2+300*np.cos(degree_t),height/2+300*np.sin(degree_t),points_t)
        points_t = points_t.astype('int')
        drawPolygon(canvas, points_t, (0,255,255), 1)
        
        cv2.imshow("my window", canvas)
        if cv2.waitKey(20) == 27 : break
    
if __name__ == "__main__":
    main()