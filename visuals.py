from OpenGL.GL import *
from OpenGL.GLU import *
from cube import vertices, edges, surfaces, colors

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
    x=0
    for surface in surfaces:
        for vertex in surface:
            glColor4fv(colors[x])
            glVertex3fv(vertices[vertex])
        x+=1
    glEnd()
    
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
    
def Grid():
    glBegin(GL_LINES)
    for i in range(-6,7,1):
        glVertex3f(i-(0.5*i),-5,0)
        glVertex3f(i-(0.5*i),5,0)
            
        glVertex3f(-5,i-(0.5*i),0)
        glVertex3f(5,i-(0.5*i),0)      
    glEnd() 