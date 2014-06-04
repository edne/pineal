#include <stdio.h>
#include <stdlib.h>

void test(char *p, int w, int h)
{
    int i;
    for(i=0; i<w*h*4; i+=4)
    {
        p[i]   = 0xFF-p[i];
        p[i+1] = 0xFF-p[i+1];
        p[i+2] = 0xFF-p[i+2];
    }
}
