# NOTE : not finish dont use this
# popup can now should position themselves on the middle as well provide appropriate box size

import pygame

class Popup:
    
    def __init__(self, window, text_object=[], bg_color=(200, 200, 200), 
                two_line_padding=10, side_padding=10, box_pos=(0, 0)):
        self.window = window
        self.text_object = text_object
        self.bg_color = bg_color
        self.two_line_padding = two_line_padding # space between two text line
        self.side_padding = side_padding # space between text line with longest length two box border
        # self.box_pos = box_pos # really dont know what to do with this yet tbh
        self.box_size = self.calculate_pop_up_box_size() # cal box size
        self.box_pos = self.calculate_pop_up_position()
        self.text_position = self.calculate_text_position()

    def calculate_pop_up_box_size(self):
        size_y = self.two_line_padding
        size_x = 0
        for text in self.text_object:
            size_y = size_y + text.get_height() + self.two_line_padding
            text_width = text.get_width()
            if text_width > size_x:
                size_x = text_width
        return (size_x + (2 * self.side_padding), size_y)

    def calculate_pop_up_position(self):
        half_size_x, half_size_y = self.window.get_size()
        half_size_x = half_size_x // 2
        half_size_y = half_size_y // 2
        return (half_size_x-self.box_size[0]//2, half_size_y-self.box_size[1]//2)

    def calculate_text_position(self):
        text_pos = []
        position_y = self.two_line_padding + self.box_pos[1]
        for text in self.text_object:
            position_x = self.box_pos[0] + (self.box_size[0] - text.get_width())//2
            text_pos.append((position_x, position_y))
            position_y = position_y + text.get_height() + self.two_line_padding
        return text_pos

    def draw(self):
        """draw all the text in text object"""
        pygame.draw.rect(self.window, self.bg_color, 
                        [self.box_pos[0], self.box_pos[1], self.box_size[0], self.box_size[1]])

        for i in range(len(self.text_object)):
            self.window.blit(self.text_object[i], self.text_position[i])
