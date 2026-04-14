
#include <gba_console.h>
#include <gba_video.h>
#include <gba_interrupt.h>
#include <gba_systemcalls.h>
#include <gba_input.h>
#include <stdio.h>
#include <stdlib.h>


int main(void) {


	// the vblank interrupt must be enabled for VBlankIntrWait() to work
	// since the default dispatcher handles the bios flags no vblank handler
	// is required
	irqInit();
	irqEnable(IRQ_VBLANK);

	consoleDemoInit();

	// ansi escape sequence to set print co-ordinates
	// /x1b[line;columnH
	BG_COLORS[0] = RGB5(31,0,0);
	BG_COLORS[241] = RGB5(0,31,0);
	iprintf("\x1b[10;10HHello World!\n");

	while (1) {
		VBlankIntrWait();
	}
}


