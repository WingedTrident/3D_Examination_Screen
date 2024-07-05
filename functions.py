from numpy import array, cross, matmul, multiply
from math import cos, sin, radians
from cube import hitboxes

#check if the given line (the cursor) intersects with the given plane (hitbox)
def line_plane_intersection(hitbox, cursorX, cursorY, color, zoom):
    A, B, C = array(hitbox[0]), array(hitbox[1]), array(hitbox[2])
    prod = cross((B-A),(C-A))
        
    o = [cursorX, 0, cursorY]
    d = [0, 1, 0] #cursor is along Y
        
    #matrix[0] /= (1-(0.005 * zoomVal))
    
    
    
     
    temp = 0 - (prod[0] * (o[0]-A[0])) - (prod[1] * (o[1]-A[1])) - (prod[2] * (o[2]-A[2]))
    temp2 = ((prod[0]*d[0])+(prod[1]*d[1])+(prod[2]*d[2]))
    
    if temp == 0 or temp2 == 0:
        return False
    t = temp / temp2
   
    point = [o[0]+d[0]*t, o[1]+d[1]*t, o[2]+d[2]*t]
    
    if zoom >= 0:
        lm = 1
        for i in range(int(zoom)):
            lm += 0.06
    elif zoom < 0:
        lm = 1
        for i in range(int(abs(zoom))):
            lm -= 0.04
    
    
    if min(hitbox[0][0],hitbox[1][0],hitbox[2][0],hitbox[3][0])*lm <= point[0] <= max(hitbox[0][0],hitbox[1][0],hitbox[2][0],hitbox[3][0])*lm:
        if min(hitbox[0][2],hitbox[1][2],hitbox[2][2],hitbox[3][2])*lm <= point[2] <= max(hitbox[0][2],hitbox[1][2],hitbox[2][2],hitbox[3][2])*lm:
            if min(hitbox[0][1],hitbox[1][1],hitbox[2][1],hitbox[3][1]) <= point[1] <= max(hitbox[0][1],hitbox[1][1],hitbox[2][1],hitbox[3][1]):
                print(point, color)
                return point[1]
            else:
                print(min(hitbox[0][1],hitbox[1][1],hitbox[2][1],hitbox[3][1]))
        
#plane rotation     
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
    
#all hitboxes are rotated since the entire object rotates    
def rotate_all_hitboxes(axis,angle):
    for coords in hitboxes.values():
        for i in range(len(coords)):
            coords[i] = matrix_multiplication(coords[i],axis,angle)
    
#checks for a hit between the cursor and the hitbox           
def check_if_hit(cursorX,cursorY,zoom):
    l = []
    for color, coords in hitboxes.items():
        hit = line_plane_intersection(coords,cursorX,cursorY,color,zoom)
        if hit and hit > 0:
            l.append((color, hit))
    if len(l)>0:
        if len(l) > 2:
            return sorted(l, key=lambda x: x[1])[1][0]
        else:
            return min(l, key=lambda x: x[1])[0]
    return None

