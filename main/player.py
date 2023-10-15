import pygame
from object import Object
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, type, vertices_sprite):
        super().__init__(groups)
        groups[0].change_layer(self, 1)
        self.type = type  #string : 'cop' or 'robber'
        self.image = pygame.image.load('../picture/void.png').convert_alpha()
        self.image_dict = {'base' : self.image}
        
        if self.type == 'cop' :
            self.add_image('cop.png', 'image')
            self.add_image('cop_isPlaying.png', 'isPlaying')
        elif self.type == 'robber' :
            self.add_image('robber.png', 'image')
            self.add_image('robber_isPlaying.png', 'isPlaying')

        self.rect = self.image.get_rect(topleft = (0,0))
        self.vertices_sprites = vertices_sprite  #groupe de sprites
        self.has_Played = False #True if the player has played on the current round
        self.is_Placed = False #n'est pas encore placé au moment de l'initialisation
        self.cursor = Object(groups[0], (0,0), '../picture/void.png')
        groups[0].change_layer(self.cursor, 2)
        self.cursor.add_image('../picture/cop.png', 'cop')
        self.cursor.add_image('../picture/robber.png', 'robber')


    def move(self, event, curseur):
        no_collision = True
        for ev in event:
            (x,y) = pygame.mouse.get_pos()
            for sprite in self.vertices_sprites :
                if self.is_Placed :   #if True, self can move only to neighboor vertices
                    
                    if sprite.rect.collidepoint((x,y)) and (sprite in self.vertice.voisins) :
                        curseur.image = curseur.image_dict['vertice_hover']
                        curseur.rect.topleft = (sprite.rect.topleft[0] , sprite.rect.topleft[1])

                        if ev.type == pygame.MOUSEBUTTONDOWN :
                            self.vertice = sprite
                            self.rect = self.image.get_rect(topleft = (self.vertice.rect.topleft[0] -10,self.vertice.rect.topleft[1] -10))
                            self.has_Played = True
                            self.image = self.image_dict['image']
                        no_collision = False

                else :  #else, we're on the round 0, and one can choose its vertice
                    mouse_pos =  pygame.mouse.get_pos()
                    self.cursor.rect.topleft = (mouse_pos[0] - 18, mouse_pos[1] - 18)
                    pygame.mouse.set_visible(False)    
                    self.cursor.image = self.cursor.image_dict[self.type]
                    if ev.type == pygame.MOUSEBUTTONDOWN and sprite.rect.collidepoint((x,y)) :
                        self.vertice = sprite
                        self.rect = self.image.get_rect(topleft = (self.vertice.rect.topleft[0] -10,self.vertice.rect.topleft[1] -10))
                        self.has_Played = True
                        self.is_Placed = True
                        pygame.mouse.set_visible(True)
                        self.cursor.image = self.cursor.image_dict['base']
                        self.image = self.image_dict['image']
            if no_collision :
                    curseur.image = curseur.image_dict['base']

    def add_image(self, name, key):
        self.image_dict[key] = pygame.image.load('../picture/'+str(name)).convert_alpha()