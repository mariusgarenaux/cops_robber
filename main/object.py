import pygame
from settings import *

class Object(pygame.sprite.Sprite):
    def __init__(self, groups, pos , name, center_x = False, center_y = False, scale = 1, adapt_screen = False):
        super().__init__(groups)
        self.group = groups
        self.image = pygame.image.load('../picture/'+name).convert_alpha()
        if center_x :    
            pos = ((xres - self.image.get_width())/2, pos[1])
        if center_y :
            pos = (pos[0], (yres - self.image.get_width())/2)

        if adapt_screen :
            self.image = pygame.transform.scale(self.image, (xres, yres))
            
        if scale != 1 :
            self.image = pygame.transform.scale(self.image, (self.image.get_width()*scale, self.image.get_height()*scale))

        
        self.rect = self.image.get_rect(topleft = pos)
        self.image_dict = {'base' : self.image}
        self.is_selected = False

        
        #animation
        self.frame_index = 0
        self.animation_speed = 0.005
        self.animation_frame = [self.image]

    def is_Clicked(self, pos, events) :
        for event in events :
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos) :
                return True
            else :
                return False
    
    def hover(self, pos) :
        """
        change the image of the object to 'hover' (from the dictionnary image_dict) when the mouse
        is on the hitbox of the object
        """
        if 'hover' in self.image_dict :
            if self.rect.collidepoint(pos) :
                self.image = self.image_dict['hover']
                return True
            else :
                self.image = self.image_dict['base']
                return False
        else :
            return False
    def add_image(self, name, key) : 
        """
        add an image to image_dict, located at ../picture/name; and with the key 'key' in image_dict
        """
        self.image_dict[key] = pygame.transform.scale(
                pygame.image.load('../picture/'+name).convert_alpha(),
             (self.image.get_width(), self.image.get_height())
            )
    
    
    def animate(self) :
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation_frame) :
            self.frame_index = 0
        self.image = self.animation_frame[int(self.frame_index)]

    def delete_control(self) :
        for groupe in self.group :
            groupe.remove(self)
