#include <GL/freeglut.h>
#include <math.h>

void rotate(double angx, double angy, double angz)
{
    glRotatef(180.0*angx/M_PI, 1,0,0);
    glRotatef(180.0*angy/M_PI, 0,1,0);
    glRotatef(180.0*angz/M_PI, 0,0,1);
}

void translate(double x, double y, double z)
{
    glTranslatef(x, y, z);
}

void scale(double x, double y, double z)
{
    glScalef(x, y, z);
}

void push(void)
{
    glPushMatrix();
}

void pop(void)
{
    glPopMatrix();
}

void cube(
    double r,
    double fr, double fg, double fb, double fa,
    double sr, double sg, double sb, double sa
)
{
    glColor4f(fr, fg, fb, fa);
    glutSolidCube(r);
    glColor4f(sr, sg, sb, sa);
    glutWireCube(r);
}

void tetrahedron(
    double r,
    double fr, double fg, double fb, double fa,
    double sr, double sg, double sb, double sa
)
{
    glPushMatrix();
    glScalef(r,r,r);

    glColor4f(fr, fg, fb, fa);
    glutSolidTetrahedron();
    glColor4f(sr, sg, sb, sa);
    glutWireTetrahedron();
    glPopMatrix();
}

void dodecahedron(
    double r,
    double fr, double fg, double fb, double fa,
    double sr, double sg, double sb, double sa
)
{
    glPushMatrix();
    glScalef(r,r,r);

    glColor4f(fr, fg, fb, fa);
    glutSolidDodecahedron();
    glColor4f(sr, sg, sb, sa);
    glutWireDodecahedron();
    glPopMatrix();
}

void octahedron(
    double r,
    double fr, double fg, double fb, double fa,
    double sr, double sg, double sb, double sa
)
{
    glPushMatrix();
    glScalef(r,r,r);

    glColor4f(fr, fg, fb, fa);
    glutSolidOctahedron();
    glColor4f(sr, sg, sb, sa);
    glutWireOctahedron();
    glPopMatrix();
}

void quad(
    double l,
    double x, double y, double z,
    double fr, double fg, double fb, double fa,
    double sr, double sg, double sb, double sa
)
{
    glColor4f(fr,fg,fb, fa);
    glBegin(GL_POLYGON);
    glVertex3f(x-l/2, y-l/2, z);
    glVertex3f(x-l/2, y+l/2, z);
    glVertex3f(x+l/2, y+l/2, z);
    glVertex3f(x+l/2, y-l/2, z);
    glEnd();

    glColor4f(sr,sg,sb, sa);
    glBegin(GL_LINE_LOOP);
    glVertex3f(x-l/2, y-l/2, z);
    glVertex3f(x-l/2, y+l/2, z);
    glVertex3f(x+l/2, y+l/2, z);
    glVertex3f(x+l/2, y-l/2, z);
    glEnd();
}

