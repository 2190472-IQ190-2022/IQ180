import sys
from turtle import color, left
import pygame
import pygame_gui
import os
import random

 # hello editing to solve merge conflict
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("IQ180")
MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT))
TEXT_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 350), (600, 50)), manager=MANAGER, object_id="#main_text_entry")

def draw_window():
    WIN.fill((128, 128, 128))
    show_randomized_number()
    pygame.display.update()

def randomize_five_number(array):
    length = len(array)
    for i in range(0, length, 1):
        array[i] = random.randint(0,9)

def show_randomized_number():
    number_set = [0, 0, 0, 0, 0]
    length  = len(number_set)
    randomize_five_number(number_set)

    transition_x = 0
    for i in range(0, length, 1):
        number_text = pygame.font.SysFont("arial", 70).render(f"{number_set[i]}", True, "black")
        number_text_rect = number_text.get_rect(center=(150+transition_x, 100))
        WIN.blit(number_text, number_text_rect)
        transition_x += 125

def main():
    clock = pygame.time.Clock()
    draw_window()
    while True:
        UI_REFRESH_RATE = clock.tick(FPS)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            MANAGER.process_events(event)
        MANAGER.update(UI_REFRESH_RATE)
        MANAGER.draw_ui(WIN)
        pygame.display.update()

if __name__ == "__main__":
    main()
