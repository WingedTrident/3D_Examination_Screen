from numpy import array, dot, cross, sqrt, sum, matmul
from math import cos, sin, radians
from cube import hitboxes

def line_plane_intersection(hitbox, cursorX, cursorY, color, zoom):
    A, B, C = array(hitbox[0]), array(hitbox[1]), array(hitbox[2])
    prod = cross((B-A),(C-A))
        
    o = [cursorX, 0, cursorY]
    d = [0, 1, 0] #cursor is along Y
    
    temp = 0 - (prod[0] * (o[0]-A[0])) - (prod[1] * (o[1]-A[1])) - (prod[2] * (o[2]-A[2]))
    temp2 = ((prod[0]*d[0])+(prod[1]*d[1])+(prod[2]*d[2]))
    
    if temp == 0 or temp2 == 0:
        return False
    t = temp / temp2
   
    point = [o[0]+d[0]*t, o[1]+d[1]*t, o[2]+d[2]*t]
      
    if point[1] != 1:
        point[0] *= (7/10)
        point[1] *= (7.5/10)
        point[2] *= (9/10)
        
    if zoom >= 0:
        if point[0] <= (1.0 + (0.1 * zoom)) and point[0] >= (-1.0 - (0.1 * zoom)) and point[2] <= (1.0 + (0.1 * zoom)) and point[2] >= (-1.0 - (0.1 * zoom)) and (point[1] <= 1.0 and point[1] >= 0.0):
            print('hit', color, point, t)
            return point[1]
    elif zoom < 0:
        if point[0] <= (1.0 + ((1/30) * zoom)) and point[0] >= (-1.0 - ((1/30) * zoom)) and point[2] <= (1.0 + ((1/30) * zoom)) and point[2] >= (-1.0 - ((1/30) * zoom)) and (point[1] <= 1.0 and point[1] >= 0.0):
            print('hit', color, point, t, zoom)
            return point[1]
        
       
def matrix_multiplication(matrix,axis,angle):
    angle = radians(angle)
    if axis == 'x':
        rotMat = [[1,0,0],[0,cos(angle),-sin(angle)],[0,sin(angle),cos(angle)]]
        return matmul(rotMat,matrix)
    if axis == 'y':
        rotMat = [[cos(angle),0,sin(angle)],[0,1,0],[-sin(angle),0,cos(angle)]]
        return matmul(rotMat,matrix)
    if axis == 'z':
        rotMat = [[cos(angle),-sin(angle),0],[sin(angle),cos(angle),0],[0,0,1]]
        return matmul(rotMat,matrix)
    
def rotate_all_hitboxes(axis,angle):
    for coords in hitboxes.values():
        for i in range(len(coords)):
            coords[i] = matrix_multiplication(coords[i],axis,angle)
            
def check_if_hit(cursorX,cursorY,zoom):
    l = []
    for color, coords in hitboxes.items():
        hit = line_plane_intersection(coords,cursorX,cursorY,color,zoom)
        if hit:
            l.append((color, hit))
    if len(l)>0:
        print(l)
        return True
