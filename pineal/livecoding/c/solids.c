#include <GL/freeglut.h>
#include <math.h>

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

