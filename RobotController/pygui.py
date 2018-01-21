import pygame
from pygame import gfxdraw
import math

HEXAGON_HEIGHT = math.sqrt(0.75)

ALIGN_LEFT = 0
ALIGN_CENTER = 1
ALIGN_RIGHT = 2

font = "open_sans.ttf"
fonts = dict()
bold_font = "open_sans_bold.ttf"
bold_fonts = dict()

def hexagon(display, colour, center_x, center_y, radius, width=0):
    points_list = [(center_x - (radius * 0.5), (center_y - (HEXAGON_HEIGHT * radius))),
                   (center_x + (radius * 0.5), (center_y - (HEXAGON_HEIGHT * radius))), (center_x + radius, center_y),
                   (center_x + (radius * 0.5), (center_y + (HEXAGON_HEIGHT * radius))),
                   (center_x - (radius * 0.5), (center_y + (HEXAGON_HEIGHT * radius))), (center_x - radius, center_y)]
    gfxdraw.aapolygon(display, points_list, colour)
    pygame.draw.polygon(display, colour, points_list, width)


def honeycomb_coords(center_x, center_y, radius, hexagon_radius, grid=False):
    coords = []
    column_height = radius * 2 + 1
    original_column_height = column_height
    for column in range(0, radius + 1):
        if column_height % 2 == 1:
            for row in range(0, int(column_height / 2) + 1):
                coords.append((center_x + (column * hexagon_radius * 1.5), center_y + (row * HEXAGON_HEIGHT * hexagon_radius * 2)))
                if row != 0:
                    coords.append((center_x + (column * hexagon_radius * 1.5), center_y - (row * HEXAGON_HEIGHT * hexagon_radius * 2)))
                if column != 0:
                    coords.append((center_x - (column * hexagon_radius * 1.5), center_y + (row * HEXAGON_HEIGHT * hexagon_radius * 2)))
                    coords.append((center_x - (column * hexagon_radius * 1.5), center_y - (row * HEXAGON_HEIGHT * hexagon_radius * 2)))
        else:
            for row in range(0, column_height / 2):
                coords.append((center_x + (column * hexagon_radius * 1.5), center_y + (HEXAGON_HEIGHT * hexagon_radius) + (2 * HEXAGON_HEIGHT * row * hexagon_radius)))
                coords.append((center_x + (column * hexagon_radius * 1.5), center_y - (HEXAGON_HEIGHT * hexagon_radius) - (2 * HEXAGON_HEIGHT * row * hexagon_radius)))
                coords.append((center_x - (column * hexagon_radius * 1.5), center_y + (HEXAGON_HEIGHT * hexagon_radius) + (2 * HEXAGON_HEIGHT * row * hexagon_radius)))
                coords.append((center_x - (column * hexagon_radius * 1.5), center_y - (HEXAGON_HEIGHT * hexagon_radius) - (2 * HEXAGON_HEIGHT * row * hexagon_radius)))
        if not grid or column_height == original_column_height:
            column_height -= 1
        else:
            column_height = original_column_height
    return coords

class TextObject(object):
    text_render = None
    x = 0
    y = 0

    def __init__(self, text_render=None, x=0, y=0):
        self.text_render = text_render
        self.x = x
        self.y = y

def create_text_object(text_font, text, colour, x, y, w, h, align_horizontal):
    text_render = text_font.render(text, True, colour)
    text_rect = text_render.get_rect()
    if align_horizontal == ALIGN_LEFT:
        text_x = x
        text_y = y  # + (h / 2 - text_rect.h / 2)
    elif align_horizontal == ALIGN_RIGHT:
        text_x = w - text_rect.w + x
        text_y = y  # + (h / 2 - text_rect.h / 2)
    else:
        text_x = x + (w / 2 - text_rect.w / 2)
        text_y = y  # + (h / 2 - text_rect.h / 2)
    text_obj = TextObject(text_render, text_x, text_y)
    return text_obj

def get_text_width(text_font, text):
    return text_font.render(text, True, (0, 0, 0)).get_rect().w

class Colour(object):
    bg_normal  = (255, 255, 255)
    bg_hover   = (200, 200, 200)
    bg_click   = ( 63,  63,  63)
    bg_disable = (255, 255, 255)
    fg_normal  = (  0,   0,   0)
    fg_hover   = (  0,   0,   0)
    fg_click   = (255, 255, 255)
    fg_disable = (127, 127, 127)

COLOUR_LIGHT = Colour()
COLOUR_DARK = Colour()
COLOUR_DARK.bg_normal = ( 31,  31,  31)
COLOUR_DARK.bg_hover  = ( 63,  63,  63)
COLOUR_DARK.bg_click  = (120, 120, 120)
COLOUR_DARK.fg_normal = (255, 255, 255)
COLOUR_DARK.fg_hover  = (255, 255, 255)
COLOUR_DARK.fg_click  = (255, 255, 255)

COLOUR_RED = Colour()
COLOUR_RED.bg_normal  = (255,  0,   0)

class Window(object):
    clock = pygame.time.Clock()
    exit = False
    widgets = []

    def __init__(self, title="", w=800, h=600, fps=30, bg=(255, 255, 255), fullscreen=False, allow_esc_exit=False):
        # type: (object, object, object, object, object, object, object) -> object
        self.title = title
        self.w = w
        self.h = h
        self.fps = fps
        self.bg = bg
        self.mouse_pos = (0, 0)
        self.mouse_dyn = (0, 0)

        pygame.init()
        if not fullscreen:
            self.display = pygame.display.set_mode((w, h))
        else:
            info = pygame.display.Info()
            self.w = info.current_w
            self.h = info.current_h
            self.display = pygame.display.set_mode((self.w, self.h), pygame.FULLSCREEN)
        pygame.display.set_caption(title)
        self.allow_esc_exit = allow_esc_exit

    def reset_widgets(self):
        del self.widgets[:]

    def add(self, widget):
        self.widgets.append(widget)

    def remove(self, widget):
        self.widgets.remove(widget)

    def render_gui(self):
        final_render = []
        for widget in self.widgets:
            if isinstance(widget, Dialog):
                final_render.append(widget)
            else:
                widget.render(self.display)
        for widget in final_render:
            widget.render(self.display)

    def update_gui(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            self.mouse_dyn = event.rel
        has_dialog = any(isinstance(widget, Dialog) for widget in self.widgets)
        for widget in self.widgets:
            if not has_dialog:
                if widget.update(event) == 1:
                    break
            elif isinstance(widget, Dialog):
                widget.update(event)

    def main_loop(self):
        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.allow_esc_exit:
                        self.exit = True
                    self.update_gui(event)

            self.display.fill(self.bg)
            self.render_gui()

            pygame.display.update()
            self.clock.tick(self.fps)

class PyGame(object):
    def __init__(self, update_func=None, render_func=None):
        self.update_func = update_func
        self.render_func = render_func

    def render(self, display):
        if self.render_func is not None:
            self.render_func(display)

    def update(self, event):
        if self.update_func is not None:
            self.update_func(event)

class Label(object):
    colour = COLOUR_DARK

    def __init__(self, text, x=0, y=0, w=0, h=0, font_size=24, align_horizontal=ALIGN_CENTER, line_h=30, word_wrap=False, bold=True):
        global bold_fonts
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        if bold:
            if font_size in bold_fonts:
                self.font = bold_fonts[font_size]
            else:
                self.font = pygame.font.Font(bold_font, font_size)
                bold_fonts[font_size] = self.font
        else:
            if font_size in fonts:
                self.font = fonts[font_size]
            else:
                self.font = pygame.font.Font(font, font_size)
                fonts[font_size] = self.font
        self.font_size = font_size
        self.align_horizontal = align_horizontal
        self.line_h = line_h
        self.word_wrap = word_wrap
        self.text_objects = []
        self.text_height = 0
        self.create_text()

    ####################################################################
    # TODO: THIS SYSTEM SHOULD BE IMPLEMENTED IN OTHER WIDGETS AS WELL #
    ####################################################################
    def create_text(self):
        del self.text_objects[:]
        current_y = self.y
        line_array = self.text.split("\n")
        for line in line_array:
            if self.word_wrap:
                word_array = line.split(" ")
                text_to_add = ""
                word_index = 0
                for word in word_array:
                    new_str = text_to_add + word + " "
                    new_str_length = get_text_width(self.font, new_str)
                    if new_str_length > self.w:
                        self.text_objects.append(create_text_object(self.font, text_to_add, self.colour.bg_normal, self.x, current_y, self.w, self.h, self.align_horizontal))
                        current_y += self.line_h
                        text_to_add = word + " "
                    else:
                        text_to_add = new_str
                    word_index += 1
                self.text_objects.append(create_text_object(self.font, text_to_add, self.colour.bg_normal, self.x, current_y, self.w, self.h, self.align_horizontal))
            else:
                self.text_objects.append(create_text_object(self.font, line, self.colour.bg_normal, self.x, current_y, self.w, self.h, self.align_horizontal))
            current_y += self.line_h
        self.text_height = current_y

    def set_text(self, text):
        self.text = text
        self.create_text()

    def set_colour(self, colour):
        self.colour = colour
        self.create_text()

    def set_align(self, horizontal):
        self.align_horizontal = horizontal
        self.create_text()

    def render(self, display):
        for text_obj in self.text_objects:
            display.blit(text_obj.text_render, [text_obj.x, text_obj.y])

    def update(self, event):
        pass

class TextField(object):
    colour = Colour()
    focused = False
    mask = None
    enabled = True

    def __init__(self, text, x=0, y=0, w=0, h=0, font_size=24, align=ALIGN_LEFT, bold=True, only_numbers=False):
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        if bold:
            if font_size in bold_fonts:
                self.font = bold_fonts[font_size]
            else:
                self.font = pygame.font.Font(bold_font, font_size)
                bold_fonts[font_size] = self.font
        else:
            if font_size in fonts:
                self.font = fonts[font_size]
            else:
                self.font = pygame.font.Font(font, font_size)
                fonts[font_size] = self.font
        self.font_size = font_size
        self.rect = pygame.Rect(x, y, w, h)
        self.align = align
        self.only_numbers = only_numbers

    def render(self, display):
        bg = self.colour.bg_normal
        if self.focused:
            bg = self.colour.bg_hover
        display.fill(bg, [self.x, self.y, self.w, self.h])

        text_to_draw = self.text
        if self.mask is not None:
            text_to_draw = ""
            for x in xrange(0, len(self.text)):
                text_to_draw += self.mask
        if self.focused:
            text_to_draw += "_"
        colour_to_use = self.colour.fg_normal
        if not self.enabled:
            colour_to_use = self.colour.fg_disable
        text = self.font.render(text_to_draw, True, colour_to_use)
        text_rect = text.get_rect()
        if self.align == ALIGN_LEFT:
            display.blit(text, [self.x + 5, self.y + (self.h / 2 - text_rect.h / 2)])
        elif self.align == ALIGN_RIGHT:
            display.blit(text, [self.w - text_rect.w + self.x - 5, self.y + (self.h / 2 - text_rect.h / 2)])
        else:
            display.blit(text, [self.x + (self.w / 2 - text_rect.w / 2), self.y + (self.h / 2 - text_rect.h / 2)])

    def update(self, event):
        if self.enabled:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(mouse_pos):
                    self.focused = True
                else:
                    self.focused = False
                    if self.only_numbers and self.text == "":
                        self.text = "0"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.rect.collidepoint(mouse_pos):
                    self.focused = False
                    if self.only_numbers and self.text == "":
                        self.text = "0"
            elif event.type == pygame.KEYDOWN and self.focused:
                if event.key > 31:
                    if not self.only_numbers:
                        self.text += event.unicode
                    elif event.unicode in "0123456789":
                        self.text += event.unicode
                elif event.key == 8 and len(self.text) > 0:
                    self.text = self.text[:-1]

class Button(object):
    colour = Colour()
    button_hover = False
    button_down = False
    enabled = True

    def __init__(self, text, x=0, y=0, w=0, h=0, font_size=24, listener=None, align=ALIGN_CENTER, bold=True):
        global bold_fonts
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        if bold:
            if font_size in bold_fonts:
                self.font = bold_fonts[font_size]
            else:
                self.font = pygame.font.Font(bold_font, font_size)
                bold_fonts[font_size] = self.font
        else:
            if font_size in fonts:
                self.font = fonts[font_size]
            else:
                self.font = pygame.font.Font(font, font_size)
                fonts[font_size] = self.font
        self.font_size = font_size
        self.listener = listener
        self.rect = pygame.Rect(x, y, w, h)
        self.align = align

    def render(self, display):
        bg = self.colour.bg_normal
        fg = self.colour.fg_normal
        if self.button_hover:
            bg = self.colour.bg_hover
            fg = self.colour.fg_hover
            if self.button_down:
                bg = self.colour.bg_click
                fg = self.colour.fg_click
        if not self.enabled:
            bg = self.colour.bg_normal
            fg = self.colour.fg_disable
        display.fill(bg, [self.x, self.y, self.w, self.h])
        text = self.font.render(self.text, True, fg)
        text_rect = text.get_rect()
        if self.align == ALIGN_LEFT:
            display.blit(text, [self.x, self.y + (self.h / 2 - text_rect.h / 2)])
        elif self.align == ALIGN_RIGHT:
            display.blit(text, [self.w - text_rect.w + self.x, self.y + (self.h / 2 - text_rect.h / 2)])
        else:
            display.blit(text, [self.x + (self.w / 2 - text_rect.w / 2), self.y + (self.h / 2 - text_rect.h / 2)])

    def update(self, event):
        if self.enabled:
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(mouse_pos):
                    self.button_hover = True
                else:
                    self.button_hover = False
                    self.button_down = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(mouse_pos):
                    self.button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(mouse_pos):
                    if self.listener is not None:
                        self.listener(self)
                        return 1
                self.button_down = False
            return 0

DIALOG_OK = ["OK"]
DIALOG_YES_NO = ["No", "Yes"]
DIALOG_YES_NO_CANCEL = ["Cancel", "No", "Yes"]
DIALOG_BUTTON_WIDTH = 100
class Dialog(object):
    TRANSLUCENT_GREY = (0, 0, 0, 127)
    GREY = (80, 80, 80)
    DARK_GREY = (40, 40, 40)
    REALLY_DARK_GREY = (20, 20, 20)

    ########################################
    # TODO: ONLY UPDATE DIALOG IF IN FOCUS #
    ########################################

    def button_listener(self, widget):
        self.win.remove(self)
        if self.listener is not None:
            self.listener(widget.text)

    def __init__(self, win, text="", w=0, h=0, font_size=24, options=DIALOG_OK, image=None, listener=None):
        self.win = win
        self.w = w
        self.h = h
        self.x = win.w / 2 - w / 2
        self.y = win.h / 2 - h / 2
        self.text_x = self.x
        self.text_width = w
        self.options = options
        if image is not None:
            self.text_width -= image.get_width()
            self.text_x = self.x + (w - self.text_width)
        self.image = image
        self.surf = pygame.Surface((win.w, win.h), pygame.SRCALPHA, 32)
        self.surf.fill(self.TRANSLUCENT_GREY)
        self.text_label = Label(text, self.text_x, self.y, self.text_width, font_size, font_size, ALIGN_LEFT, font_size + 6, True, False)
        self.text_label.set_colour(COLOUR_LIGHT)

        self.buttons = []
        current_x = self.x + w - 110

        for option in options:
            option_button = Button(option, current_x, self.y + h - 40, DIALOG_BUTTON_WIDTH, 30, 24, self.button_listener)
            self.buttons.append(option_button)
            current_x -= 110

        # self.ok_button = Button("OK", self.x + w - 110, self.y + h - 40, 100, 30, 24, self.button_listener)

        self.listener = listener

    def render(self, display):
        display.blit(self.surf, (0, 0))
        display.fill(self.REALLY_DARK_GREY, [self.x - 30, self.y - 30, self.w + 60, self.h + 60])
        display.fill(self.DARK_GREY, [self.x - 20, self.y - 20, self.w + 40, self.h + 40])
        display.fill(self.GREY, [self.x - 10, self.y - 10, self.w + 20, self.h + 20])
        self.text_label.render(display)
        for button in self.buttons:
            button.render(display)
        if self.image is not None:
            display.blit(self.image, [self.x, self.y])

    def update(self, event):
        for button in self.buttons:
            button.update(event)