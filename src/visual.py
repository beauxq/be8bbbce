import pygame

from be8bbbce.visualcomponents.visualmain import VisualMain
from be8bbbce.computer import Computer
from be8bbbce.programs.programs8bit.intro import p
from be8bbbce.asm import Assembler

pygame.init()

address_length = 4
a = Assembler(address_length)
computer = Computer(address_length)
p(computer, a)
vm = VisualMain(computer)

vm.run()

pygame.quit()
