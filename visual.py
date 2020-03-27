from visualcomponents.visualmain import VisualMain
from computer import Computer

import pygame
pygame.init()

address_length = 4
computer = Computer(address_length)
vm = VisualMain(computer)

vm.run()

pygame.quit()
