from visualcomponents.visualmain import VisualMain
from computer import Computer
from programs.programs8bit.p4 import p
from asm import Assembler

import pygame
pygame.init()

address_length = 4
a = Assembler(address_length)
computer = Computer(address_length)
p(computer, a)
computer.ram.memory[15] = 4
vm = VisualMain(computer)

vm.run()

pygame.quit()
