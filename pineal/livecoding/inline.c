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

void square(
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

void line(
    double x1, double y1, double z1,
    double x2, double y2, double z2,
    double sr, double sg, double sb, double sa
)
{
    glColor4f(sr,sg,sb, sa);
    glBegin(GL_LINES);
    glVertex3f(x1, y1, z1);
    glVertex3f(x2, y2, z2);
    glEnd();
}

void point(
    double x, double y, double z,
    double sr, double sg, double sb, double sa
)
{
    glColor4f(sr,sg,sb, sa);
    glBegin(GL_POINTS);
    glVertex3f(x, y, z);
    glEnd();
}

void quad(
    double x1, double y1, double z1,
    double x2, double y2, double z2,
    double x3, double y3, double z3,
    double x4, double y4, double z4,
    double fr, double fg, double fb, double fa,
    double sr, double sg, double sb, double sa
)
{
    glColor4f(fr,fg,fb, fa);
    glBegin(GL_POLYGON);
    glVertex3f(x1, y1, z1);
    glVertex3f(x2, y2, z2);
    glVertex3f(x3, y3, z3);
    glVertex3f(x4, y4, z4);
    glEnd();

    glColor4f(sr,sg,sb, sa);
    glBegin(GL_LINE_LOOP);
    glVertex3f(x1, y1, z1);
    glVertex3f(x2, y2, z2);
    glVertex3f(x3, y3, z3);
    glVertex3f(x4, y4, z4);
    glEnd();
}

void rect(
    double x, double y,
    double w, double h,
    double fr, double fg, double fb, double fa,
    double sr, double sg, double sb, double sa
)
{
    glColor4f(fr,fg,fb, fa);
    glBegin(GL_POLYGON);
    glVertex3f(x,   y,   0);
    glVertex3f(x,   y+h, 0);
    glVertex3f(x+w, y+h, 0);
    glVertex3f(x+w, y,   0);
    glEnd();

    glColor4f(sr,sg,sb, sa);
    glBegin(GL_LINE_LOOP);
    glVertex3f(x,   y,   0);
    glVertex3f(x,   y+h, 0);
    glVertex3f(x+w, y+h, 0);
    glVertex3f(x+w, y,   0);
    glEnd();
}


void triangle(
    double x1, double y1,
    double x2, double y2,
    double x3, double y3,
    double fr, double fg, double fb, double fa,
    double sr, double sg, double sb, double sa
)
{
    glColor4f(fr,fg,fb, fa);
    glBegin(GL_POLYGON);
    glVertex3f(x1, y1, 0);
    glVertex3f(x2, y2, 0);
    glVertex3f(x3, y3, 0);
    glEnd();

    glColor4f(sr,sg,sb, sa);
    glBegin(GL_LINE_LOOP);
    glVertex3f(x1, y1, 0);
    glVertex3f(x2, y2, 0);
    glVertex3f(x3, y3, 0);
    glEnd();
}

// http://slabode.exofire.net/circle_draw.shtml
void polygon(
    double cx, double cy,
    double r,  int n,
    double x_dist,  double y_dist,
    double fr, double fg, double fb, double fa,
    double sr, double sg, double sb, double sa
)
{
    double theta = 2.0*M_PI / n; 
    double c = cos(theta);
    double s = sin(theta);
    double t;

    double x,y;
    int i;

    x = r;
    y = 0;

    glColor4f(fr,fg,fb, fa);
    glBegin(GL_POLYGON); 
    for(i=0; i<n; i++) 
    { 
        glVertex2f(x*x_dist + cx, y*y_dist + cy);

        //apply the rotation matrix
        t = x;
        x = c * x - s * y;
        y = s * t + c * y;
    } 
    glEnd();

    x = r;
    y = 0;

    glColor4f(sr,sg,sb, sa);
    glBegin(GL_LINE_LOOP); 
    for(i=0; i<n; i++) 
    { 
        glVertex2f(x*x_dist + cx, y*y_dist + cy);

        //apply the rotation matrix
        t = x;
        x = c * x - s * y;
        y = s * t + c * y;
    } 
    glEnd();

}
