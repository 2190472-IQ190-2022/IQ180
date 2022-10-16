############## MAYBE DONT USE THIS CLASS YET IT'S NOT FINISH AND I'M RETARDED #################
# Note: all the image related things are not implemented yet
# Note: don't use "operation" parameter yet

import pygame

class Button:
    """
        This class create usable Button
        param (required):
            window - the game's window (from pygame.display.set_mode(W, H))
            button_font - the button's font (from pygame.font.SysFont('arial', 69))
        param (optional):
            pos - button's position (tuple of two int e.g. (width, height))
            size - button's size (tuple of two int e.g. (width, height))
            enabled_color - button's color when it's clickable (tuple of three int e.g. (R, G, B))
            hover_color - button's color when the mouse hover over the button (tuple of three int e.g. (R, G, B))
            disabled_color - button's color when the button's disabled (tuple of three int e.g. (R, G, B))
            text - text on the button (string)
            disabled - Whether the button is disabled, if button is disabled, you can't click and it will not do the assigned operation
                    (see "operarion" parameter below) (Boolean)
            img - pygame image object that are used when the button is ENABLED (from pygame.image.load(<Image Path>))
            img_hover - pygame image object that are used when the button is HOVERED (from pygame.image.load(<Image Path>))
            img_pressed - pygame image object that are used when the button is PRESSED (from pygame.image.load(<Image Path>))
            operation - name of function that you wants to be called when pressed
                    (just used name of the function with out the bracket, e.g. operation=test_func)
            any other parameter name that are not listed above can be enter to be used as "operation" function parameter
                    e.g. operation=test_func, word="hello" will call test_func(word="hello"), hopefully
    """

    def __init__(self, window, button_font, pos=(300, 300), size=(100, 100), enabled_color=(100, 100, 100),
                 hover_color=(170, 170, 170), disabled_color=(50, 50, 50), text="text", disabled=False,
                 img=None, img_hover=None, img_pressed=None, operation=None, ** op_args):
        self.window = window
        self.button_font = button_font
        self.pos = pos
        self.size = size
        self.enabled_color = enabled_color
        self.hover_color = hover_color
        self.disabled_color = disabled_color
        self.text = text
        self.clicked = False
        if operation is None:
            self.disabled = True
        else:
            self.disabled = False
            self.operation = operation
        if disabled:
            self.disabled = True
        print(op_args)

    def set_pos(self, pos):
        self.pos = pos

    def set_text(self, text):
        self.text = text

    def is_hovering(self, mouse_pos):
        if self.pos[0] < mouse_pos[0] < self.pos[0]+self.size[0] and self.pos[1] < mouse_pos[1] < self.pos[1]+self.size[1] and not self.disabled:
            return True
        return False

    def draw(self, mouse):
        color = self.enabled_color
        if self.is_hovering(mouse):
            color = self.hover_color

        if self.disabled:
            color = self.disabled_color

        pygame.draw.rect(self.window, color, [self.pos[0], self.pos[1], self.size[0], self.size[1]])
        self.text_rendered = self.button_font.render(self.text, 1, (0, 0, 0))
        self.window.blit(self.text_rendered, (self.pos[0]+self.size[0]/2-self.text_rendered.get_width()/2,
                self.pos[1]+self.size[1]/2-self.text_rendered.get_height()/2))

    def press(self):
        if not self.disabled:
            self.operation()

    def set_operation(self, operation):
        self.operation = operation

    def disable_button(self):
        self.disabled = True

    def enable_button(self):
        self.disabled = False