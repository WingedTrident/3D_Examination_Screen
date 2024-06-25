import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from numpy import array

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

#function to draw text              
def drawText(x, y, text, charNum):                                                
    font = pygame.font.SysFont('consolas', 22)
    textSurface = font.render(text[:charNum], True, (255,255,255,255)).convert_alpha()
    second_line_char = -1
    #draw until char #30 then make a new line when a space is hit
    if charNum >= 30:
        for i in range(30, charNum):
            if text[i] == " ":
                second_line_char = i+1
                break
        if second_line_char != -1:
            textSurface = font.render(text[:second_line_char], True, (255,255,255,255)).convert_alpha()
                
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
    if second_line_char != -1:
        textSurface2 = font.render(text[second_line_char:charNum], True, (255,255,255,255)).convert_alpha()
        textData2 = pygame.image.tostring(textSurface2, "RGBA", True)
        glWindowPos2d(x, y-30)
        glDrawPixels(textSurface2.get_width(), textSurface2.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData2)
    glDisable(GL_BLEND)
    
    #write characters one by one
    if charNum != len(text):
        return charNum + 1
    else:
        return charNum