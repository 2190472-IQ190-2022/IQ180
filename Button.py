# Note: all the image related things are not implemented yet
# Note: Button should work now
# Note: you currently cannot change the button color, no need to implement if use image

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
            XXX_color - color when the button is XXX (tuple of three int e.g. (R, G, B))
            text - text on the button (string)
            disabled - Whether the button is disabled, if button is disabled, you can't click and it will not do the assigned operation
                    (see "operarion" parameter below) (Boolean)
            img_XXX - pygame image object that are used when the button is XXX (from pygame.image.load(<Image Path>))
            operation - name of function that you wants to be called when pressed
                    (just used name of the function with out the bracket, e.g. operation=test_func)
            any other parameter name that are not listed above can be enter to be used as "operation" function parameter
                    e.g. operation=test_func, word="hello" will call test_func(word="hello"), hopefully
    """

    def __init__(self, window, button_font, pos=(300, 300), size=(100, 100), enabled_color=(100, 100, 100),
                 hover_color=(170, 170, 170), pressed_color=(20, 20, 20), disabled_color=(50, 50, 50), text="text",
                 disabled=False, img=None, img_hover=None, img_pressed=None, img_disabled=None, operation=None, ** op_args):
        self.window = window
        self.button_font = button_font
        self.pos = pos
        self.size = size
        self.mouse = pygame.mouse
        self.enabled_color = enabled_color
        self.hover_color = hover_color
        self.disabled_color = disabled_color
        self.pressed_color = pressed_color
        self.text = text
        self.op_args = op_args
        self.status = 0  # 0 is disbled 1 is enabled 2 is hovered 3 is pressed
        self.text_rendered = self.button_font.render(self.text, 1, (0, 0, 0))
        if operation is None:
            self.status = 0
        else:
            self.status = 1
            self.operation = operation
        if disabled:
            self.status = 0

    def set_pos(self, pos):
        self.pos = pos
        self.draw()

    def get_pos(self):
        return self.pos

    def set_text(self, text):
        self.text = text
        self.text_rendered = self.button_font.render(self.text, 1, (0, 0, 0))
        self.draw()

    def get_text(self):
        return self.text

    def get_text_rendered(self):
        return self.text_rendered

    def set_operation(self, operation):
        self.operation = operation

    def disable_button(self):
        self.status = 0

    def enable_button(self):
        self.status = 1

    def is_hovering(self):
        if self.pos[0] < self.mouse.get_pos()[0] < self.pos[0]+self.size[0] and self.pos[1] < self.mouse.get_pos()[1] < self.pos[1]+self.size[1] and self.status != 0:
            return True
        return False

    def is_mouse_down(self):
        if self.mouse.get_pressed()[0]:
            return True
        return False

    def is_pressed(self):
        return self.is_hovering() and self.is_mouse_down()

    def update_button(self):
        """
            This function control all the hover and press interaction of the EACH button
            Put this function on the MAIN LOOP, NOT EVENT LOOP
        """
        # status = 0
        if self.status == 0:
            self.draw()
            return None
        # status = 1 not press and not hover
        if not self.is_hovering() and not self.is_mouse_down():
            self.status = 1
        # status = 2 not press and hover
        if self.is_hovering() and not self.is_mouse_down():
            self.status = 2
        # status = 3 press and hover
        if self.is_hovering() and self.is_mouse_down() and self.status != 3:
            self.status = 3
            self.operation(** self.op_args)
        if self.status == 3 and not self.is_hovering() and not self.is_mouse_down():
            self.status = 1
        if self.status == 3 and self.is_hovering() and not self.is_mouse_down():
            self.status = 2
        if self.status == 3 and not self.is_hovering() and self.is_mouse_down():
            self.status = 1

        self.draw()

    def draw(self):
        """
            call this function to draw THIS ONE BUTTON OBJECT ONLY, drawing multiple button is outside the capability of this function.
        """
        color = self.enabled_color

        if self.status == 2:
            color = self.hover_color

        if self.status == 0:
            color = self.disabled_color

        if self.status == 3:
            color = self.pressed_color

        pygame.draw.rect(self.window, color, [
                         self.pos[0], self.pos[1], self.size[0], self.size[1]])
        self.window.blit(self.text_rendered, (self.pos[0]+self.size[0]/2-self.text_rendered.get_width()/2,
                                              self.pos[1]+self.size[1]/2-self.text_rendered.get_height()/2))
