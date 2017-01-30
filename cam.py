import pygame
import pygame.camera
from pygame.locals import *
import pygame.image
import predict

DEVICE = '/dev/video0'
SIZE = (1280, 720)
FILENAME = 'capture.jpg'

def camstream():
    pygame.init()
    pygame.camera.init()
    display = pygame.display.set_mode(SIZE, 0)
    camera = pygame.camera.Camera(pygame.camera.list_cameras()[0])
    camera.start()
    screen = pygame.surface.Surface(SIZE, 0, display)
    capture = True
    while capture:
        screen = camera.get_image(screen)
        display.blit(screen, (0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                capture = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, FILENAME)
                predict.predict(FILENAME)
                print("-------------")
    camera.stop()
    pygame.quit()
    return

if __name__ == '__main__':
    init()
    camstream()
