from loadRom import loadRom
import fontset
import RAM
import graphics
import random
import tkinter as tk
import keyboard

class Chip8:
    def __init__(self, rom):
        self.set_values()
        for c, i in enumerate(loadRom(rom)):
            self.ram[c + 512] = i
        print(self.ram)
        for c, i in enumerate(fontset.fontset):
            self.ram[c + 80] = i
#    for c, i in enumerate([hex_data[4*i:4*(1+i)] for i in range(len(hex_data)//4)]):
#            print("0x%X" % (c*4), i,  str(binascii.unhexlify(''.join(i))))
#        for i in self.ram:
#            print(f"0x{i}")


    def set_values(self):
        self.ram = RAM.ram(4)

        self.V = [0]*16

        self.I = 0
        self.pc = 512

        self.graphics = graphics.Graphics()

        self.delay_timer = 60
        self.sound_timer = 60

        self.stack = [0]*16
        self.stack_pointer = 0
        self.key = [0]*16
        self.key_list = [
            "1", "2", "3", "4",
            "Q", "W", "E", "R",
            "A", "S", "D", "F",
            "Z", "X", "C", "V"
        ]
        self.draw_flag = True
        self.opcode_dict0 = {
            "0x00e0": self._00E0,
            "0x00ee": self._00EE,
        }
        self.opcode_dict1 = {
            "ea1": self._EXA1,
            "f07": self._FX07,
            "f0a": self._FX0A,
            "f15": self._FX15,
            "f18": self._FX18,
            "f1e": self._FX1E,
            "f29": self._FX29,
            "f33": self._FX33,
            "f55": self._FX55,
            "f65": self._FX65,
        }
        self.opcode_dict2 = {
            "50": self._5XY0,
            "80": self._8XY0,
            "81": self._8XY1,
            "82": self._8XY2,
            "83": self._8XY3,
            "84": self._8XY4,
            "85": self._8XY5,
            "86": self._8XY6,
            "87": self._8XY7,
            "8e": self._8XYE,
            "90": self._9XY0,
            "ee": self._EX9E
        }
        self.opcode_dict3 = {
            "0": self._0NNN,
            "1": self._1NNN,
            "2": self._2NNN,
            "3": self._3XNN,
            "4": self._4XNN,
            "6": self._6XNN,
            "7": self._7XNN,
            "a": self._ANNN,
            "b": self._BNNN,
            "c": self._CXNN,
            "d": self._DXYN
        }
    def on_press(self, key):
        self.key[key] = 1
    def listener(self):
        for c, i in enumerate(self.key_list):
            if keyboard.is_pressed(i):
                self.on_press(c)

    def clear_keys(self):
        self.key = [0]*16

    def emulation_cycle(self):
        opcode = int(self.ram[self.pc], 16) << 8 | int(self.ram[self.pc + 1], 16)
        hex_opcode = '0x{0:0{1}X}'.format(opcode,4).lower()
        #print(hex_opcode)
#        print(self.pc)
        try:
            hex_opcode245 = f'{hex_opcode[2]}{hex_opcode[4]}{hex_opcode[5]}'
            hex_opcode25 = f'{hex_opcode[2]}{hex_opcode[5]}'
            hex_opcode2 = f'{hex_opcode[2]}'
        except:
            print(hex_opcode)
            return True

        if hex_opcode in self.opcode_dict0:
            print(self.opcode_dict0[hex_opcode].__name__, hex_opcode)
            self.opcode_dict0[hex_opcode]()
        if hex_opcode245 in self.opcode_dict1:
            print(self.opcode_dict1[hex_opcode245].__name__, hex_opcode)
            self.opcode_dict1[hex_opcode245](hex_opcode[2:])
        if hex_opcode25 in self.opcode_dict2:
            print(self.opcode_dict2[hex_opcode25].__name__, hex_opcode)
            self.opcode_dict2[hex_opcode25](hex_opcode[2:])
        elif hex_opcode2 in self.opcode_dict3:
            print(self.opcode_dict3[hex_opcode2].__name__, hex_opcode)
            self.opcode_dict3[hex_opcode2](hex_opcode[2:])
        #print(self.pc)

    def _0NNN(self,opcode):
        self.pc += 2

    def _00E0(self):
        self.draw_flag = True
        self.pc += 2

    def _00EE(self):
        self.stack_pointer -= 1
        self.pc = self.stack[self.stack_pointer] + 2

    def _1NNN(self,opcode):
        self.pc = int(opcode[1:], 16)

    def _2NNN(self,opcode):
        self.stack[self.stack_pointer] = self.pc
        self.stack_pointer += 1
        self.pc = int(opcode[1:], 16)
        print(self.pc)

    def _3XNN(self,opcode):
        if self.V[int(opcode[1],16)] == int(opcode[2:],16):
            self.pc += 2
        self.pc += 2

    def _4XNN(self, opcode):
        if self.V[int(opcode[1],16)] != int(opcode[2:],16):
            self.pc += 2
        self.pc += 2

    def _5XY0(self,opcode):
        if self.V[int(opcode[1],16)] == self.V[int(opcode[2],16)]:
            self.pc += 2
        self.pc += 2

    def _6XNN(self,opcode):
        self.V[int(opcode[1],16)] = int(opcode[2:],16)
        #print(self.V)
        self.pc += 2

    def _7XNN(self,opcode):
        self.V[int(opcode[1], 16)] += int(opcode[2:], 16)
        self.pc += 2

    def _8XY0(self,opcode):
        self.V[int(opcode[1], 16)] = self.V[int(opcode[2], 16)]
        self.pc += 2

    def _8XY1(self,opcode):
        self.V[int(opcode[1], 16)] |= self.V[int(opcode[2], 16)]
        self.pc += 2

    def _8XY2(self,opcode):
        self.V[int(opcode[1], 16)] &= self.V[int(opcode[2], 16)]
        self.pc += 2

    def _8XY3(self,opcode):
        self.V[int(opcode[1], 16)] ^= self.V[int(opcode[2], 16)]
        self.pc += 2

    def _8XY4(self,opcode):
        op1 = int(opcode[1], 16)
        self.V[op1] += self.V[int(opcode[2], 16)]
        if self.V[op1] > 255:
            print(self.V[op1])
            self.V[15] = 1
        else:
            self.V[15] = 0
        self.pc += 2

    def _8XY5(self,opcode):
        op1 = int(opcode[1], 16)
        self.V[op1] -= self.V[int(opcode[2], 16)]
        if self.V[op1] < 0:
            self.V[15] = 0
        else:
            self.V[15] = 1
        self.pc += 2

    def _8XY6(self,opcode):
        self.V[15] = self.V[int(opcode[1], 16)] & 1
        self.V[int(opcode[1], 16)] >>= 1
        self.pc += 2

    def _8XY7(self,opcode):
        op1 = int(opcode[1], 16)
        self.V[op1] = self.V[int(opcode[2], 16)] - self.V[op1]
        if self.V[op1] < 0:
            self.V[15] = 0
        else:
            self.V[15] = 1
        self.pc += 2

    def _8XYE(self,opcode):
        vx = self.V[int(opcode[1], 16)]
        self.V[15] = int(format(vx,'08b')[0])
        self.V[int(opcode[1], 16)] <<= 1
        self.pc += 2

    def _9XY0(self,opcode):
        if self.V[int(opcode[1], 16)] != self.V[int(opcode[2], 16)]:
            self.pc += 2
        self.pc += 2

    def _ANNN(self, opcode):
        self.I = int(opcode[1:], 16)
        #print(hex(self.I))
        self.pc += 2

    def _BNNN(self,opcode):
        self.pc = self.V[0] + int(opcode[1:], 16)

    def _CXNN(self,opcode):
        self.V[int(opcode[1], 16)] = random.randint(0,255) & int(opcode[2:], 16)
        self.pc += 2

    def _DXYN(self,opcode):
        x = self.V[int(opcode[1], 16)]
        y = self.V[int(opcode[2], 16)]
        height = int(opcode[3], 16)
        #print(x)
        mem = self.ram[self.I:(self.I+height)]
        self.V[15] = self.graphics.draw(x,y,mem, height)
        self.draw_flag = True
        self.pc += 2

    def _EX9E(self,opcode):
        if self.key[self.V[int(opcode[1],16)]] == 1:
            self.pc += 2
        self.pc += 2

    def _EXA1(self,opcode):
        if self.key[self.V[int(opcode[1],16)]] == 0:
            self.pc += 2
        self.pc += 2

    def _FX07(self,opcode):
        self.V[int(opcode[1],16)] = self.delay_timer
        self.pc += 2

    def _FX0A(self,opcode):
        while True:
            if any(i for i in self.key):
                for key, i in enumerate(self.key):
                    if i:
                        self.V[int(opcode[1],16)] = key
                        break
        self.pc += 2

    def _FX15(self,opcode):
        self.delay_timer = int(opcode[1],16)
        self.pc += 2

    def _FX18(self,opcode):
        self.sound_timer = int(opcode[1],16)
        self.pc += 2

    def _FX1E(self,opcode):
        self.I += self.V[int(opcode[1],16)]
        self.pc += 2

    def _FX29(self,opcode):
        self.I = 80 + int(opcode[1], 16)
        self.pc += 2

    def _FX33(self,opcode):
        self.I = int(str(self.V[int(opcode[1],16)])[::-1])
        self.pc += 2

    def _FX55(self,opcode):
        op1 = int(opcode[1],16)
        for c, i in enumerate(self.V[0:op1+1]): # 0-15
            self.ram[self.I+c] = i
        self.pc += 2

    def _FX65(self,opcode):
        op1 = int(opcode[1],16)
        for i in range(op1+1):
            self.V[i] = self.ram[self.I+i]
        self.pc += 2

if __name__ == "__main__":
    chip8 = Chip8("Pong.ch8")
    chip8.pc = 0x200
    chip8.emulation_cycle()
    print(chip8.ram)
#    pc = 38
#    print(hex(int(chip8.hex_data[pc], 16) << 8 | int(chip8.hex_data[pc + 1], 16)))
