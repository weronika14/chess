import pygame
import chesss
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

def main():
    chesss.displayingBoard()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYUP:
            if event.key == 27:
                exit()

    pygame.display.flip()

'''
while True:
    main()
'''
