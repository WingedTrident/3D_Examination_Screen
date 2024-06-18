import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image
from numpy import array

#cubes vertices
vertices= (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

#cubes edges
edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

#cubes colors values
colors = (
    (1,1,1),
    (0,0,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (1,1,1),
    )

#cubes surfaces
surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

#render for cube
def Cube():
    #line render
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    
    #surface area render
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x+=1
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])
    glEnd()

#function to load texture from image file    
def loadTexture(texture):
    path = "sprites/"
    try:
        text = Image.open(path + texture)
    except IOError as ex:
        print("Failed to open texture file: ", texture)
        

    textData = array(list(text.getdata()))
    textID = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glBindTexture(GL_TEXTURE_2D, textID)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text.size[0], text.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, textData)
    text.close()
    return textID

#render for quad (to impose texture on)
    """_params_: 
    centerX - Quad's X Position
    centerY - Quad's Y Position
    textureID - texture data from loadTexture
    scale - amount to scale the quad by (1 by 1 square by default)
    """
def drawQuad(centerX, centerY, textureID, scale=(1,1)):
    verts = ((1*scale[0],1*scale[1]), (1*scale[0],-1*scale[1]), (-1*scale[0], -1*scale[1]), (-1*scale[0], 1*scale[1]))
    texts = ((1, 0), (1, 1), (0, 1), (0, 0))
    surf = (0, 1, 2, 3)

    glEnable(GL_TEXTURE_2D)
    
    glBindTexture(GL_TEXTURE_2D, textureID)

    glBegin(GL_QUADS)
    for i in surf:
        glTexCoord2f(texts[i][0], texts[i][1])
        glVertex2f((centerX + verts[i][0]), (centerY + verts[i][1]))
    glEnd()
    
    glDisable(GL_TEXTURE_2D)   

#temporary separate loop to test hitboxes 
def test():
    win_width = 800
    win_height = 600
    display = win_width, win_height
    surface = pygame.display.set_mode(display)
     
    color = (255,0,0)
    x = pygame.Rect(70, 30, 60, 60) 
    y = pygame.Rect(70, 510, 60, 60)  
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    main()
 
        # Drawing Rectangle
        pygame.draw.rect(surface, color, x)
        pygame.draw.rect(surface, color, y)
        pygame.display.flip()
    
#main loop    
def main():
    #window vars
    FPS = 30
    pivot = False
    win_width = 800
    win_height = 600
    
    #sprite vars
    mouse_down = False
    
    displayWindow = pygame.Rect(250, 150, 300, 300)
    
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
    
    #load all textures
    zoomInID = loadTexture("zoomIn.png")
    zoomInPressedID = loadTexture("zoomInPressed.png")
    zoomOutID = loadTexture("zoomOut.png")
    zoomOutPressedID = loadTexture("zoomOutPressed.png")
    zoomBarID = loadTexture("zoomBar.png")
    zoomLevelID = loadTexture("zoomLevel.png")
    background1ID = loadTexture("background1.png")
    hwheelAnimation = [loadTexture("wheelFrame1.png"), loadTexture("wheelFrame2.png"), loadTexture("wheelFrame3.png")]
    vwheelAnimation = [loadTexture("wheelFrame1V.png"), loadTexture("wheelFrame2V.png"), loadTexture("wheelFrame3V.png")]
    
    while True:
        mouseX, mouseY = pygame.mouse.get_pos()
        
        
        #resetup viewport
        glViewport(0,0,win_width,win_height)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        #push identity matrix to manipulate 3D
        glPushMatrix()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(100, aspect, 1, 10) #3D camera
        glMatrixMode(GL_MODELVIEW)

        #event manipulation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    glRotatef(-1, 1, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glRotatef(1, 1, 0, 0)
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
                    pivot = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
                    pivot = False
                    zoom_up_pressed, zoom_down_pressed = False, False

                           
            if event.type == pygame.MOUSEMOTION:
                mouseDirection = event.rel
                if pivot and displayWindow.collidepoint((mouseX, mouseY)):
                    glRotatef(event.rel[1], 1, 0, 0)
                    glRotatef(event.rel[0], 0, 1, 0)
                #----- USED FOR TESTING HITBOXES
                #if x.collidepoint((mouseX, mouseY)):
                    #glMatrixMode(GL_MODELVIEW)
                    #glEnable(GL_TEXTURE_2D)
                    #glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    #test()
                #-----
        if mouse_down:
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
                    
            if hwheelHitbox.collidepoint((mouseX, mouseY)):
                if mouseDirection and mouseDirection[0] != 0:
                    if mouseDirection[0] > 1:
                        glRotatef(2, 0, 1, 0)
                        hwheelAnimationFrame += 1
                        if hwheelAnimationFrame >= len(hwheelAnimation):
                            hwheelAnimationFrame = 0
                    elif mouseDirection[0] < 1:
                        glRotatef(-2, 0, 1, 0)
                        hwheelAnimationFrame -= 1
                        if hwheelAnimationFrame < 0:
                            hwheelAnimationFrame = len(hwheelAnimation) - 1
                            
            if vwheelHitbox.collidepoint((mouseX, mouseY)):
                if mouseDirection and mouseDirection[1] != 0:
                    if mouseDirection[1] > 2:
                        glRotatef(3, 1, 0, 0)
                        vwheelAnimationFrame += 1
                        if vwheelAnimationFrame >= len(vwheelAnimation):
                            vwheelAnimationFrame = 0
                    elif mouseDirection[1] < -2:
                        glRotatef(-3, 1, 0, 0)
                        vwheelAnimationFrame -= 1
                        if vwheelAnimationFrame < 0:
                            vwheelAnimationFrame = len(vwheelAnimation) - 1
                    
        
                
        #clears buffer
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        #apply transformations and save new matrix
        glMultMatrixf(modelMatrix)
        modelMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        
        #reset FOV
        glLoadIdentity()
        glTranslatef(0, 0, zoomVal)
        glMultMatrixf(modelMatrix)
        
        #draw 3D elements
        Cube()

        #reset stack for next loop
        glPopMatrix()
        
        #now switch to drawing 2D sprites
        glClear(GL_DEPTH_BUFFER_BIT)
      
        glMatrixMode (GL_PROJECTION) 
        glLoadIdentity() 
        glOrtho(-aspect*5, aspect*5, -5, 5, -1, 50) #2D viewport
        

        #draw all 2D sprites
        glMatrixMode(GL_MODELVIEW) 
        glLoadIdentity()
        
        drawQuad(-5, 0, background1ID, (2,5))
        drawQuad(5, 0, background1ID, (2,5))
        drawQuad(0, 4, background1ID, (3,1.5))
        drawQuad(0, -4, background1ID, (3,1.5))
        drawQuad(-5, 4, zoomInPressedID, ((1/2),(1/2))) if zoom_up_pressed else drawQuad(-5, 4, zoomInID, ((1/2),(1/2))) 
        drawQuad(-5, -4, zoomOutPressedID, ((1/2),(1/2))) if zoom_down_pressed else drawQuad(-5, -4, zoomOutID, ((1/2),(1/2)))
        drawQuad(-5, 0, zoomLevelID, (.8,3.5))
        drawQuad(zoom_bar_x, zoom_bar_y, zoomBarID, (1.3,(1/5)))
        drawQuad(0, -4.5, hwheelAnimation[hwheelAnimationFrame], (3,1))
        drawQuad(5.5, .5, vwheelAnimation[vwheelAnimationFrame], (1,3))

        #render frame (matching FPS limits)
        pygame.display.flip()
        clock.tick(FPS)       
main()