#include <gba_types.h>
#include <gba_video.h>
#include <gba_systemcalls.h>
#include <stdlib.h>

u16* video = (u16*)VRAM;

void placePX(u8 posx, u8 posy, u8 r, u8 g, u8 b){
    //u8 y = 160 - posy;
    video[posy*240 + posx] = RGB5(r,g,b);
}

void drawLine(int x0, int y0, int x1, int y1, u8 r, u8 g, u8 b){
    int dx = abs(x1 - x0);
    int dy = abs(y1 - y0);

    int sx = (x0 < x1) ? 1 : -1;
    int sy = (y0 < y1) ? 1 : -1;

    int err = dx - dy;

    while (1){
        placePX(x0, y0, r, g, b);

        if (x0 == x1 && y0 == y1){
            break;
        }

        int e2 = 2 * err;

        if (e2 > -dy){
            err -= dy;
            x0 += sx;
        }

        if (e2 < dx){
            err += dx;
            y0 += sy;
        }
    }
}


int main(void)
{
    REG_DISPCNT = MODE_3 | BG2_ENABLE;


    // écran rouge plein
    for (int i = 0; i < 240 * 160; i++)
    {
        video[i] = RGB5(31, 31, 31);
    }
    for (int i=0; i<240;i++){
        placePX(i,3,20,0,0);
    }
    drawLine(0,1 ,239 ,160,0,0,0);
    drawLine(0,160,239 ,0,0,0,0 );
    while (1)
    {
        VBlankIntrWait();
    }
}
