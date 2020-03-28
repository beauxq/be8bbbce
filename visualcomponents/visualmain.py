from computer import Computer
from components.register import Register
from visualcomponents.ramreader import RamReader
from visualcomponents.irreader import IRReader
from visualcomponents.signalwatcher import SignalWatcher
import pygame
from typing import Tuple, List, Union

MAX_CLOCK_HZ = 250


class VisualMain:
    def __init__(self, computer: Computer):
        self.screen = pygame.display.set_mode((700, 700), pygame.RESIZABLE)
        self.computer = computer
        self.running = False
        self.ram_reader = RamReader(computer.ram)
        self.i_r_reader = IRReader(computer.ir)
        self.sw = SignalWatcher(computer.signals)
        self.paused = False
        self.fps = 20

        self.load_fonts()

    def load_fonts(self):
        # print("setting font size", int(self.led_size()) + 1)
        # print("width", self.screen.get_width())
        self.button_font = pygame.font.Font('freesansbold.ttf',
                                            int(self.led_size()) + 1)
        self.output_font = pygame.font.Font('freesansbold.ttf',
                                            (int(self.led_size()) + 1) * 2)
        self.label_font = self.button_font
        self.signal_font = pygame.font.Font(
            'visualcomponents/LiberationMono-Bold.ttf',
            (int(self.led_size()) - 2) +
            int((self.computer.bit_count - 8) * .125)
        )

    def run(self):
        self.running = True
        pygame_clock = pygame.time.Clock()

        while self.running:
            pygame_clock.tick(self.fps)

            if not self.paused:
                # computer clock toggle
                if self.computer.clock.value:
                    self.computer.clock.go_low()
                else:
                    self.computer.clock.go_high()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.VIDEORESIZE:
                    # https://stackoverflow.com/questions/11603222/allowing-resizing-window-pygame
                    old_surface_saved = self.screen
                    self.screen = pygame.display.set_mode((event.w, event.h),
                                                          pygame.RESIZABLE)
                    self.screen.blit(old_surface_saved, (0, 0))
                    del old_surface_saved
                    self.load_fonts()
                    # note this pygame bug with resizing window:
                    # https://github.com/pygame/pygame/issues/201
                    # Resizing from the corner of the window doesn't work.
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_p) or (event.key == pygame.K_SPACE):
                        self.paused = not self.paused
                    elif event.key == pygame.K_r:
                        self.computer.control.reset()
                    elif (event.key == pygame.K_c) and self.paused:
                        self.computer.clock.go_high()
                    elif event.key == pygame.K_LEFTBRACKET:
                        self.fps = max(.5, self.fps / 1.4)
                    elif event.key == pygame.K_RIGHTBRACKET:
                        self.fps = min(MAX_CLOCK_HZ * 2, self.fps * 1.4)
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_c) and self.paused:
                        self.computer.clock.go_low()

            self.screen.fill((180, 180, 160))

            self.draw()

            pygame.display.flip()

    def draw(self):
        bit_count = self.computer.bit_count

        self.draw_value(self.computer.bus, bit_count,
                        .5, .05, (1, 0, 0), "Bus")
        self.draw_value(self.computer.clock, 1,
                        .32, .08, (0, 0, 1), "Clock")
        self.draw_value(self.computer.ram.mar,
                        self.computer.address_length,
                        .25, .22, (1, 1, 0), "Memory Address")
        self.draw_value(self.ram_reader, bit_count,
                        .2, .4, (1, 0, 0), "Memory Contents")
        self.i_r_reader.instruction_part = True
        self.draw_value(self.i_r_reader,
                        self.computer.instruction_length,
                        .2, .7, (0, 0, 1), "")
        self.i_r_reader.instruction_part = False
        self.draw_value(self.i_r_reader,
                        self.computer.address_length,
                        .35, .7, (1, 1, 0), "Instruction Register")
        self.draw_value(self.computer.control, 3,
                        .1, .75, (0, 1, 0), "Control")
        # right side
        self.draw_value(self.computer.pc,
                        self.computer.address_length,
                        .75, .08, (0, 1, 0), "Program Counter")
        self.draw_value(self.computer.reg_a, bit_count,
                        .85, .25, (1, 0, 0), '"A" Register')
        self.draw_value(self.computer.flags, 2,
                        .96, .28, (0, 1, 0), ["CF", "ZF"], 2)
        self.draw_value(self.computer.alu, bit_count,
                        .76, .4, (1, 0, 0), "Sum Register")
        self.draw_value(self.computer.reg_b, bit_count,
                        .85, .55, (1, 0, 0), '"B" Register')
        self.draw_value(self.sw, 16,
                        .6, .9, (0, 0, 1),
                        ["HLT", "MI", "RI", "RO", "IO", "II", "AI", "AO",
                         "ΣO", "SU", "BI", "OI", "CE", "CO", "J", "FI"],
                        3)

        # controls
        # clock stuff
        color = (0, 150, 0)
        if self.paused:
            color = (200, 0, 0)
        x = self.screen.get_width() * .02
        y = self.screen.get_height() * .1
        size = self.led_size() * 2
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y, size * 4, size))
        # pause
        text = self.button_font.render('P', True, (10, 0, 120))
        text_rect = text.get_rect()
        text_rect.center = (x + (size * 3.5), y + self.led_size())
        self.screen.blit(text, text_rect)
        # clock tick
        text = self.button_font.render("C", True, (0, 150, 0))
        text_rect = text.get_rect()
        text_rect.center = (x + (size * 2.5), y + self.led_size())
        self.screen.blit(text, text_rect)
        # speed up
        max_fps = MAX_CLOCK_HZ * 2
        sqrt_max_fps = max_fps ** .5
        color = int(252 * (self.fps ** .5) / sqrt_max_fps)
        text = self.button_font.render("]", True, (color, color, 140))
        text_rect = text.get_rect()
        text_rect.center = (x + (size * 1.5), y + self.led_size())
        self.screen.blit(text, text_rect)
        # slow down
        text = self.button_font.render("[", True, (color, color, 120))
        text_rect = text.get_rect()
        text_rect.center = (x + (size * 0.5), y + self.led_size())
        self.screen.blit(text, text_rect)

        # reset button
        color = (120, 120, 170)
        x = self.screen.get_width() * .02
        y = self.screen.get_height() * .6
        size = self.led_size() * 2
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y, size, size))
        # r
        text = self.button_font.render('R', True, (80, 80, 0))
        text_rect = text.get_rect()
        text_rect.center = (x + (size * 0.5), y + (size * 0.5))
        self.screen.blit(text, text_rect)


        # output
        color = (50, 0, 0)
        x = self.screen.get_width() * .65
        y = self.screen.get_height() * .7
        size = self.led_size() * 3
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y, size * 3, size))
        # number
        text = self.output_font.render(str(self.computer.out.value), True, (250, 20, 20))
        textRect = text.get_rect()
        textRect.center = (x + (size * 1.5), y + (size * 0.5))
        self.screen.blit(text, textRect)

    def led_size(self):
        return (min(self.screen.get_width(), self.screen.get_height()) /
                ((self.computer.bit_count * 2.5) + 12)
               )

    def draw_value(self,
                   component: Register,
                   bit_count: int,
                   x_portion: float,
                   y_portion: float,
                   led_color: Tuple[float],
                   label_text: Union[str, List[str]],
                   vertical_label_height=0):
        """
        component is anything with value attribute - duck typing
        bit_count is number of LEDs to show
        x_portion is [0, 1] x location on screen - 0 left, 1 right
        y_portion is [0, 1] y location on screen - 0 top, 1 bottom
        led_color is tuple of 3 rgb floats [0, 1]
        """
        bit_size = self.led_size()
        width = bit_count * bit_size
        x = (self.screen.get_width() - width) * x_portion
        y = (self.screen.get_height() - bit_size) * y_portion
        """
        pygame.draw.rect(self.screen,
                         (20, 20, 20),
                         pygame.Rect(x, y, width, bit_size))
                         """
        value = component.value
        radius = bit_size / 2
        circle_y = y + radius
        if vertical_label_height:
            pygame.draw.rect(self.screen, (240, 240, 240),
                             pygame.Rect(x, y + bit_size, width,
                                         bit_size * vertical_label_height))
        for bit in range(bit_count):
            brightness = 255 if (value % 2) else 80
            color = tuple((c * brightness for c in led_color))
            circle_x = x + width - (bit_size * bit + radius)
            pygame.draw.circle(self.screen,
                               color,
                               (int(circle_x), int(circle_y)),
                               int(radius))
            if vertical_label_height:
                this_label = label_text[-(1+bit)]
                label_y = circle_y
                for letter in this_label:
                    label_y += bit_size
                    text = self.label_font.render(letter, True,
                                                  (16, 16, 16))
                    text_rect = text.get_rect()
                    text_rect.center = (circle_x, label_y)
                    self.screen.blit(text, text_rect)
            value >>= 1
        if (not vertical_label_height) and label_text:
        font = self.label_font
        if label_text.startswith(" "):
            font = self.signal_font
        text = font.render(label_text, True,
                           (16, 16, 16), (240, 240, 240))
            text_rect = text.get_rect()
            x_text = x + (width / 2)
            if isinstance(component, IRReader):
                x_text = x + (width / 3)
            text_rect.center = (x_text, y + (bit_size * 1.6))
            self.screen.blit(text, text_rect)
