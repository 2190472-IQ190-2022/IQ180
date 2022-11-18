import pygame
import os

class Animation:

    def __init__(self, window, size, pos, frame, screen_size, ident, pictures=[], current_frame=0, rerun=True,
                run_every_frame=1, speed=(0, 0), self_replicate=False):
        self.window = window
        self.size = size
        self.pos = pos
        self.pictures = pictures
        self.frame = len(self.pictures)
        self.current_frame = current_frame
        self.rerun = rerun
        self.run_every_frame=run_every_frame
        self.finished = False
        self.total_frame = 0
        self.speed = speed
        self.pause = False
        self.self_replicate = self_replicate
        self.screen_size = screen_size
        self.ident = ident
        # print("__init__ pic" + str(self.pictures))

    def play(self):
        """start the animation if the animation is paused"""
        self.pause = False

    def pause_animation(self):
        """stop the animation in place if the animation is paused"""
        self.pause = True

    def move_position(self, new_position):
        """if can change the position of where it was blit"""
        self.pos = new_position

    def get_size(self):
        return self.size

    def get_pos(self):
        return self.pos

    def get_finish(self):
        return self.finished

    def get_ident(self):
        return self.ident

    def get_current_frame(self):
        return self.current_frame

    def get_frame(self):
        return self.frame

    def set_speed(self, speed):
        self.speed = speed

    def set_finish(self, finish):
        self.set_finish = finish

    def draw_animation(self):
        """check draw/not draw and blit the animation if allowed"""
        # print(f"pictures {self.pictures}")
        if self.self_replicate:
            # print("hello" + str(len(self.pictures)))
            position = self.pos
            while position[0] < self.screen_size[0] + self.size[0]:
                # print(f"current frame: {self.current_frame}")
                while position[1] < self.screen_size[1] + self.size[1]:
                    self.window.blit(self.pictures[self.current_frame], position)
                    position = (position[0], position[1] + self.size[1])
                position = (position[0] + self.size[0], self.pos[1])
            if self.pos[0] + self.size[0] < 0:
                self.pos = (0, self.pos[1])
        else:
            self.window.blit(self.pictures[self.current_frame], self.pos)
        self.total_frame += 1
        if not self.pause:
            if self.total_frame % self.run_every_frame == 0:
                self.current_frame += 1
                self.pos = (self.pos[0] + self.speed[0], self.pos[1] + self.speed[1])
                if self.current_frame >= self.frame or self.current_frame >= len(self.pictures):
                    if self.rerun:
                        # print("reset frame")
                        self.current_frame = 0
                    else:
                        self.finished = True
        # print(f"next frame = {self.current_frame}")
        # print(f"pictures {self.pictures}")
        # print(f"position {self.pos}")
        # print(f"rerun {self.rerun}")

    @staticmethod
    def create_animation_from_sheet(full_sheet, frame_size, scale_size, color=None):
        """sprite sheet -> pygame pictures list"""
        # full sheet is pygame image obj so let so one once handle loading
        pictures = []
        for i in range(full_sheet.get_height() // frame_size[1]):
            for j in range(full_sheet.get_width() // frame_size[0]):
                pic = pygame.Surface(frame_size).convert_alpha()
                pic.blit(full_sheet, (0, 0), (j * frame_size[0], i * frame_size[1], frame_size[0], frame_size[1]))
                pic = pygame.transform.scale(pic, scale_size)
                if not color is None:
                    pic.set_colorkey(color)
                pictures.append(pic)
        return pictures
    
    @staticmethod
    def create_animation_from_file_path(path, scale_size=(-1, -1)):
        """bunch of picture file -> pygame pictures list"""
        pictures = []
        for p in os.listdir(path):
            full_path = os.path.join(path, p)
            if os.path.isfile(full_path): # maybe add file type check here later
                pic = pygame.image.load(full_path)
                if not scale_size == (-1, -1):
                    pic = pygame.transform.scale(pic, scale_size)
                pictures.append(pic)
        return pictures

