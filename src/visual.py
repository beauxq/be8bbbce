import pygame

from be8bbbce.visualcomponents.visualmain import VisualMain
from be8bbbce.computer import Computer
# from be8bbbce.programs.programs8bit.sqrt import p
from be8bbbce.programs.programs8bit.p2 import p
from be8bbbce.asm import Assembler

pygame.init()

address_length = 4
a = Assembler(address_length)
computer = Computer(address_length)
p(computer, a)
computer.ram.memory[15] = 4
vm = VisualMain(computer)

vm.run()

pygame.quit()
