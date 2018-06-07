import sys
import math

from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtOpenGL import *

from scipy.spatial import ConvexHull
import numpy as np


cameraPos = [0.0, 0.0, 2.2]
cameraFront = [0.0, 0.0, 0.0]
cameraUp = [0.0, 1.0, 0.0]


def calNorm(p1, p2, p3):
    u = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    v = (p3[0] - p1[0], p3[1], p1[1], p3[2] - p1[2])

    crossProduct = (u[1]*v[2] - u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1] - u[1]*v[0])
    return crossProduct

def dotProduct(v1, v2):
    return (v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2])

def inFrontOfPlane(v1, v2):
    if dotProduct(v1, v2) >= 0:
        return True
    else:
        return False


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.widget = glWidget(self)

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.widget)

        self.setLayout(mainLayout)

    def screenLocation(self):
        self.move(480, 100)


    def keyPressEvent(self, event):
        global cameraPos
        global cameraUp
        global cameraFront

        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

        if event.key() == QtCore.Qt.Key_F: # Front
            cameraPos = [0.0, 0.0, 2.2]
            cameraUp = [0.0, 1.0, 0.0]


        if event.key() == QtCore.Qt.Key_R: # Right
            cameraPos = [2.2, 0.0, 0.0]
            cameraUp = [0.0, 1.0, 0.0]

        if event.key() == QtCore.Qt.Key_L: # Left
            cameraPos = [-2.2, 0.0, 0.0]
            cameraUp = [0.0, 1.0, 0.0]


        if event.key() == QtCore.Qt.Key_B: # Back
            cameraPos = [0.0, 0.0, -2.2]
            cameraUp = [0.0, 1.0, 0.0]

        if event.key() == QtCore.Qt.Key_U: # Up
            cameraPos= [0.0, 2.2, 0.0]
            cameraUp = [0.0, 0.0, -1.0]

        if event.key() == QtCore.Qt.Key_Up:
            cameraPos[1] += 0.1
            cameraFront[1] += 0.1
            cameraUp = [0.0, 1.0, 0.0]

        if event.key() == QtCore.Qt.Key_Right:
            cameraPos[0] += 0.1
            cameraFront[0] += 0.1

        if event.key() == QtCore.Qt.Key_Left:
            cameraPos[0] -= 0.1
            cameraFront[0] -= 0.1

        if event.key() == QtCore.Qt.Key_Down:
            cameraPos[1] -= 0.1
            cameraFront[1] -= 0.1

        if event.key() == QtCore.Qt.Key_I:
            if cameraUp[2] == 0.0:
                if cameraPos[0] > 0.0:
                    cameraPos[0] -= 0.1
                elif cameraPos[0] < 0.0:
                    cameraPos[0] += 0.1
                else:
                    cameraPos[2] -= 0.1
            else:
                cameraPos[1] -= 0.1


        if event.key() == QtCore.Qt.Key_O:
            if cameraUp[2] == 0.0:
                if cameraPos[0] > 0.0:
                    cameraPos[0] += 0.1
                elif cameraPos[0] < 0.0:
                    cameraPos[0] -= 0.1
                else:
                    cameraPos[2] += 0.1
            else:
                cameraPos[1] += 0.1

        self.widget.updateGL()


class glWidget(QGLWidget):
    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(1024, 800)

    def paintGL(self):
        filename = "Samples\Female\Body"

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glLoadIdentity()
        gluLookAt(cameraPos[0], cameraPos[1], cameraPos[2], cameraFront[0], cameraFront[1], cameraFront[2], cameraUp[0], cameraUp[1], cameraUp[2])

        glScale(0.09, 0.09, 0.09)

        h = [] 
        n = []
        t = []
        ll = []
        lr = []
        fl = []
        fr = []
        al = []
        ar = []
        hl = []
        hr = []
        s = []

        f = open(filename+".BodyInfo", "r")

        for i in range(21):
            f.readline()

        # torso
        f.readline() # Name
        l = f.readline() #N Node
        num = int(l.split("=")[1])
        for i in range(num):
            l = f.readline()            
            l = l.replace("\n", "")
            t.append(int(l))

        # skirt
        f.readline() # Name
        l = f.readline() #N Node
        num = int(l.split("=")[1])
        for  i in range(num):
            l = f.readline()            
            l = l.replace("\n", "")
            s.append(int(l))

        # right leg
        f.readline() # Name
        l = f.readline() #N Node
        num = int(l.split("=")[1])
        for  i in range(num):
            l = f.readline()            
            l = l.replace("\n", "")
            lr.append(int(l))

        # left leg
        f.readline() # Name
        l = f.readline() #N Node
        num = int(l.split("=")[1])
        for  i in range(num):
            l = f.readline()            
            l = l.replace("\n", "")
            ll.append(int(l))

        # right arm
        f.readline() # Name
        l = f.readline() #N Node
        num = int(l.split("=")[1])
        for  i in range(num):
            l = f.readline()            
            l = l.replace("\n", "")
            ar.append(int(l))

        # left arm
        f.readline() # Name
        l = f.readline() #N Node
        num = int(l.split("=")[1])
        for  i in range(num):
            l = f.readline()            
            l = l.replace("\n", "")
            al.append(int(l))

        # right hand
        f.readline() # Name
        l = f.readline() #N Node
        num = int(l.split("=")[1])
        for  i in range(num):
            l = f.readline()            
            l = l.replace("\n", "")
            hr.append(int(l))

        # left hand
        f.readline() # Name
        l = f.readline() #N Node
        num = int(l.split("=")[1])
        for  i in range(num):
            l = f.readline()            
            l = l.replace("\n", "")
            hl.append(int(l))

        # right foot
        f.readline() # Name
        l = f.readline() #N Node
        num = int(l.split("=")[1])
        for  i in range(num):
            l = f.readline()            
            l = l.replace("\n", "")
            fr.append(int(l))

        # left foot
        f.readline() # Name
        l = f.readline() #N Node
        num = int(l.split("=")[1])
        for  i in range(num):
            l = f.readline()            
            l = l.replace("\n", "")
            fl.append(int(l))

        # head
        f.readline() # Name
        l = f.readline() #N Node
        num = int(l.split("=")[1])
        for  i in range(num):
            l = f.readline()            
            l = l.replace("\n", "")
            h.append(int(l))

        # neck
        f.readline() # Name
        l = f.readline() #N Node
        num = int(l.split("=")[1])
        for  i in range(num):
            l = f.readline()            
            l = l.replace("\n", "")
            n.append(int(l))


        f.close()

        '''
        v = open(filename+"vertices.txt", "r")

        vertices = []
        while True:
            l = v.readline()
            l = l.replace("\n", "")
            ls = l.split(' ')
            if not l: break
            vertices.append(ls)

        v.close()
        '''

        glScale(1.001, 1.001, 1.001)
        glBegin(GL_POINTS)
        
        # head
        glColor4f(1, 1, 1, 0.3)
        for i in h:
            x = float(vertices[int(i)][0])
            y = float(vertices[int(i)][1])
            z = float(vertices[int(i)][2])
            glVertex3f(x, y, z)

        # neck
        glColor4f(1, 1, 1, 0.3)
        for i in n:
            x = float(vertices[int(i)][0])
            y = float(vertices[int(i)][1])
            z = float(vertices[int(i)][2])
            glVertex3f(x, y, z)

        #skirt
        for i in s:
            x = float(vertices[int(i)][0])
            y = float(vertices[int(i)][1])
            z = float(vertices[int(i)][2])
            glVertex3f(x, y, z)

        # torso
        glColor4f(1, 1, 1, 0.3)
        for i  in t:
            x = float(vertices[int(i)][0])
            y = float(vertices[int(i)][1])
            z = float(vertices[int(i)][2])
            glVertex3f(x, y, z)

        # left leg
        glColor4f(1, 1, 1, 0.3)
        for i in ll:
            x = float(vertices[int(i)][0])
            y = float(vertices[int(i)][1])
            z = float(vertices[int(i)][2])
            glVertex3f(x, y, z)

        # right leg
        glColor4f(1, 1, 1, 0.3)
        for i in lr:
            x = float(vertices[int(i)][0])
            y = float(vertices[int(i)][1])
            z = float(vertices[int(i)][2])
            glVertex3f(x, y, z)

        # left foot
        glColor4f(1, 1, 1, 0.3)
        for i in fl:
            x = float(vertices[int(i)][0])
            y = float(vertices[int(i)][1])
            z = float(vertices[int(i)][2])
            glVertex3f(x, y, z)

        # right foot
        glColor4f(1, 1, 1, 0.3)
        for i in fr:
            x = float(vertices[int(i)][0])
            y = float(vertices[int(i)][1])
            z = float(vertices[int(i)][2])
            glVertex3f(x, y, z)

        # left arm
        glColor4f(1, 1, 1, 0.3)
        for i in al:
            x = float(vertices[int(i)][0])
            y = float(vertices[int(i)][1])
            z = float(vertices[int(i)][2])
            glVertex3f(x, y, z)

        # right arm
        glColor4f(1, 1, 1, 0.3)
        for i in ar:
            x = float(vertices[int(i)][0])
            y = float(vertices[int(i)][1])
            z = float(vertices[int(i)][2])
            glVertex3f(x, y, z)

        # left hand
        glColor4f(1, 1, 1, 0.3)
        for i in hl:
            x = float(vertices[int(i)][0])
            y = float(vertices[int(i)][1])
            z = float(vertices[int(i)][2])
            glVertex3f(x, y, z)

        # right hand
        glColor4f(1, 1, 1, 0.3)
        for i in hr:
            x = float(vertices[int(i)][0])
            y = float(vertices[int(i)][1])
            z = float(vertices[int(i)][2])
            glVertex3f(x, y, z)

        glColor3f(1, 0, 0)
        glEnd()
        glFlush()


    def initializeGL(self):
        glClearDepth(1.0)              
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glViewport(0, 0, 1024, 800)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()                    
        gluPerspective(45.0, 1024.0/800.0, 0.01, 100.0) 
        glMatrixMode(GL_MODELVIEW)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.screenLocation()
    window.show()

    #Volume = Cylinder()
    #Volume.draw(50, 50, 10)
    sys.exit(app.exec_())