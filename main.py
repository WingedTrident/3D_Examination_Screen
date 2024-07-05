import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from visuals import Cube, drawQuad, Grid
from functions import *
from texturing import *

#main loop    
def main():
    #window vars
    FPS = 30
    win_width = 800
    win_height = 600
    
    #sprite vars
    mouse_down = False
    
    displayWindow = pygame.Rect(250, 150, 300, 300)
    cursorX = 0 #openGL coords
    cursorY = 0 #openGL coords
    
    zoomVal = -5 #current camera distance to center
    zoom_window_interval = .2
    
    zoom_up_hitbox = pygame.Rect(70, 30, 60, 60) 
    zoom_down_hitbox = pygame.Rect(70, 510, 60, 60)
    zoom_up_pressed = False
    zoom_down_pressed = False
    
    zoom_bar_x = -5
    zoom_bar_y = 0
    zoom_bar_interval = 0.35
    zoom_bar_limits = (zoom_bar_interval*9, zoom_bar_interval*-9) #9 levels up, 9 levels down
    
    hwheelAnimationFrame = 0
    hwheelHitbox = pygame.Rect(220, 500, 360, 50)
    vwheelAnimationFrame = 0
    vwheelHitbox = pygame.Rect(650, 85, 50, 360) 
    mouseDirection = None
    rotDeg = 5
    
    selected = None
    selectedText = ""
    charNum = 0
      
    #setup pygame
    pygame.init()
    display = (win_width, win_height)
    clock = pygame.time.Clock()
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    #setup openGL
    glMatrixMode(GL_PROJECTION)
    aspect = (display[0]/display[1])
    gluPerspective(45, aspect, 0.1, 50.0)
    glTranslatef(0.0,0.0, zoomVal)
    glMatrixMode(GL_MODELVIEW)  
    modelMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    orthoL = -aspect*5
    orthoR = aspect*5
    orthoB = -5
    orthoT = 5 
    print(win_width/win_height, orthoL, orthoR, orthoB, orthoT)
    
    #load all textures
    zoomInID = loadTexture("zoomIn.png")
    zoomInPressedID = loadTexture("zoomInPressed.png")
    zoomOutID = loadTexture("zoomOut.png")
    zoomOutPressedID = loadTexture("zoomOutPressed.png")
    zoomBarID = loadTexture("zoomBar.png")
    zoomLevelID = loadTexture("zoomLevel.png")
    cursorID = loadTexture("cursor.png")
    background1ID = loadTexture("background1.png")
    textboxID = loadTexture("textbox.png")
    hwheelAnimation = [loadTexture("wheelFrame1.png"), loadTexture("wheelFrame2.png"), loadTexture("wheelFrame3.png")]
    vwheelAnimation = [loadTexture("wheelFrame1V.png"), loadTexture("wheelFrame2V.png"), loadTexture("wheelFrame3V.png")]
    
    while True:
        mouseX, mouseY = pygame.mouse.get_pos()
        
        #resetup viewport
        glViewport(0,0,win_width,win_height)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        #draw grid lines
        glPushMatrix()   
        Grid()
        glPopMatrix()
    
        #push identity matrix to manipulate 3D part
        glPushMatrix()
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(110, aspect, 1, 10) #3D camera
        glMatrixMode(GL_MODELVIEW)
        #event manipulation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
                    zoom_up_pressed, zoom_down_pressed = False, False 
                    if displayWindow.collidepoint((mouseX, mouseY)):
                        selected = check_if_hit(cursorX,cursorY,((zoomVal+5)//zoom_window_interval)) #get which part of the display was hit
                        charNum = 0 #reset textbox
                        if selected == None:
                            selected = True
                            selectedText = "There appears to be nothing at this location."
                        else:
                            selectedText = f"This side of the cube appears to be {selected}."             
            if event.type == pygame.MOUSEMOTION:
                mouseDirection = event.rel
                if displayWindow.collidepoint((mouseX, mouseY)):
                    cursorX = ((mouseX / win_width) * (orthoR - (orthoL))) + orthoL
                    cursorY = ((mouseY / win_height) * (orthoB - (orthoT))) + orthoT
        #if mouse is held down           
        if mouse_down:
            #zoom buttons
            if zoom_up_hitbox.collidepoint((mouseX, mouseY)):
                if zoom_bar_y < zoom_bar_limits[0]:
                    zoom_bar_y += zoom_bar_interval
                    zoomVal += zoom_window_interval
                    zoom_up_pressed = True
            elif zoom_down_hitbox.collidepoint((mouseX, mouseY)):
                if zoom_bar_y > zoom_bar_limits[1]:
                    zoom_bar_y -= zoom_bar_interval
                    zoomVal -= zoom_window_interval
                    zoom_down_pressed = True
            #left-right scroll        
            if hwheelHitbox.collidepoint((mouseX, mouseY)):
                if mouseDirection and mouseDirection[0] != 0:
                    if mouseDirection[0] > 2:
                        glRotatef(rotDeg, 0, 1, 0)
                        hwheelAnimationFrame += 1
                        if hwheelAnimationFrame >= len(hwheelAnimation):
                            hwheelAnimationFrame = 0
                        rotate_all_hitboxes('z',-rotDeg)
                    elif mouseDirection[0] < -2:
                        glRotatef(-rotDeg, 0, 1, 0)
                        hwheelAnimationFrame -= 1
                        if hwheelAnimationFrame < 0:
                            hwheelAnimationFrame = len(hwheelAnimation) - 1
                        rotate_all_hitboxes('z',rotDeg)
            #up-down scroll                
            if vwheelHitbox.collidepoint((mouseX, mouseY)):
                if mouseDirection and mouseDirection[1] != 0:
                    if mouseDirection[1] > 2:
                        glRotatef(rotDeg, 1, 0, 0)
                        vwheelAnimationFrame += 1
                        if vwheelAnimationFrame >= len(vwheelAnimation):
                            vwheelAnimationFrame = 0
                        rotate_all_hitboxes('x',-rotDeg)
                    elif mouseDirection[1] < -2:
                        glRotatef(-rotDeg, 1, 0, 0)
                        vwheelAnimationFrame -= 1
                        if vwheelAnimationFrame < 0:
                            vwheelAnimationFrame = len(vwheelAnimation) - 1
                        rotate_all_hitboxes('x',rotDeg)

        #apply transformations and save new matrix
        glMultMatrixf(modelMatrix)
        modelMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        
        #reset FOV
        glLoadIdentity()
        glTranslatef(0, 0, zoomVal)
        glMultMatrixf(modelMatrix)
        
        #draw 3D elements   
        glEnable(GL_DEPTH_TEST) 
        Cube()
        glDisable(GL_DEPTH_TEST)

        #reset stack for next part
        glPopMatrix()
        
        #now switch to drawing 2D sprites
        glClear(GL_DEPTH_BUFFER_BIT)
      
        glMatrixMode (GL_PROJECTION) 
        glLoadIdentity() 
        glOrtho(orthoL, orthoR, orthoB, orthoT, -1, 50) #2D viewport
        
        #draw all 2D sprites
        glMatrixMode(GL_MODELVIEW) 
        glLoadIdentity()
        
        #cursor lines
        glBegin(GL_LINES)
        glColor3f(1,0,0)
        glVertex3f(cursorX,-5,0)
        glVertex3f(cursorX,5,0)
        
        glVertex3f(-5,cursorY,0)
        glVertex3f(5,cursorY,0)
        glColor3f(1,1,1)
        glEnd()
        
        #sprite drawing
        drawQuad(-5, 0, background1ID, (2,5))
        drawQuad(5, 0, background1ID, (2,5))
        drawQuad(0, 4, background1ID, (3,1.5))
        drawQuad(0, -4, background1ID, (3,1.5))
        drawQuad(-5, 4, zoomInPressedID, ((1/2),(1/2))) if zoom_up_pressed else drawQuad(-5, 4, zoomInID, ((1/2),(1/2))) 
        drawQuad(-5, -4, zoomOutPressedID, ((1/2),(1/2))) if zoom_down_pressed else drawQuad(-5, -4, zoomOutID, ((1/2),(1/2)))
        drawQuad(-5, 0, zoomLevelID, (.8,3.5))
        drawQuad(cursorX, cursorY, cursorID, (1/10,1/10))
        drawQuad(zoom_bar_x, zoom_bar_y, zoomBarID, (1.3,(1/5)))
        drawQuad(0, 3.75, textboxID, (3.5,1))
        drawQuad(0, -4.5, hwheelAnimation[hwheelAnimationFrame], (3,1))
        drawQuad(5.5, .5, vwheelAnimation[vwheelAnimationFrame], (1,3))
        if selected:
            charNum = drawText(210, 530, selectedText, charNum)

        #render frame (matching FPS limits)
        pygame.display.flip()
        clock.tick(FPS)    
           
if __name__ == '__main__':
    main()