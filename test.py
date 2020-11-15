import pygame

pygame.init()
window_surface = pygame.display.set_mode((800,800))

try:
    #raise FileNotFoundError('Test')
    self.background = pygame.image.load("Ressources/menu_bg.jpg")
except OSError as e:
    print (str(e))
except:
    background = pygame.Surface((800,800))
    background.fill(pygame.Color('#000000'))

print("Finished")