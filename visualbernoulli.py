import pygame

from visualcomponents.visualmain import VisualMain
from computer import Computer
from asm import Assembler

from programs.programs16bit.multisub import p as p1
from programs.programs16bit.dividsub import p as p2
from programs.programs16bit.gcdsub import p as p4
from programs.programs16bit.addfrsub import p as p5
from programs.programs16bit.reducsub import p as p6

from programs.programs16bit.bernoulli import p as bern

pygame.init()

address_length = 12
a = Assembler(address_length)
computer = Computer(address_length)
p1(computer, a)
p2(computer, a)
p4(computer, a)
p5(computer, a)
p6(computer, a)
bern(computer, a)

vm = VisualMain(computer)

vm.run()

pygame.quit()
