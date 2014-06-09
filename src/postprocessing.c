#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define GET(p,x,y, offset) p[(y*w + x)*4 + offset]
#define R(p,x,y) GET(p,x,y, 0)
#define G(p,x,y) GET(p,x,y, 1)
#define B(p,x,y) GET(p,x,y, 2)
//#define A(p,x,y) GET(p,x,y, 3)

void mirror(char *p, int w, int h)
{
    int x,y, nx,ny;
    for(x=w/2+1; x<w; x++)
    for(y=0; y<h; y++)
    {
        nx = w-1-x;
        ny = y;
        R(p,x,y) = R(p,nx,ny);
        G(p,x,y) = G(p,nx,ny);
        B(p,x,y) = B(p,nx,ny);
    }
}
