import pygame as sdl  # to-may-to, to-maaaa-to


sdl.init()
screen = sdl.display.set_mode((640, 400))
running = 1

red = sdl.Color(255,0,0)

while running:
    event = sdl.event.poll()
    if event.type == sdl.KEYDOWN: #pygame.QUIT:
        running = 0
        
