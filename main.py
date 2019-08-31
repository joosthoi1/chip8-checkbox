import chip8
import json
import sys
import time

class main:
    def __init__(self):
        self.chip8 = chip8.Chip8("Pong.ch8")
        self.main()
        self.chip8.graphics.root.mainloop()

    def main(self):
        while True:
            if self.chip8.delay_timer > 0:
                self.chip8.delay_timer -= 1
            if self.chip8.sound_timer > 0:
                self.chip8.sound_timer -= 1
            if self.chip8.draw_flag:
                self.chip8.graphics.root.update()
                self.chip8.graphics.clear_previous()
                self.chip8.draw_flag = False
                self.chip8.clear_keys()
                self.chip8.listener()
            if self.chip8.emulation_cycle():
                break


if __name__ == "__main__":
    main()
