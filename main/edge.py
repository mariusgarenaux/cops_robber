import pygame
from object import Object
from settings import *
import numpy as np

class Edge(pygame.sprite.Sprite) :
    def __init__(self, groups, depart, arrivee):
        super().__init__(groups)
        self.group = groups
        self.depart = depart
        self.arrivee = arrivee
        self.control_point = depart
        self.update_pos()

    def hover(self, pos, cursor) :
        """
        if cursor is on this edge, it turns red, else, it stays black
        """
        #pos_in_mask = (pos[0] - self.rect.x, pos[1] - self.rect.y)
        if self.rect.collidepoint(pos) and pygame.sprite.collide_mask(cursor, self):
            self.color_red()
        else :
            self.color_black()

    def color_red(self) :
        if self.color == 'black' :
            pxarray = pygame.PixelArray(self.image)
            pxarray.replace((0,0,0), (255, 0, 0))
            self.color = 'red'
    
    def color_black(self) :
        if self.color == 'red' :
            pxarray = pygame.PixelArray(self.image)
            pxarray.replace( (255, 0, 0), (0,0,0))
            self.color = 'black'

    def is_Clicked(self, pos, events, cursor) :
        #pos_in_mask = (pos[0] - self.rect.x, pos[1] - self.rect.y)
        for event in events :
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos) and pygame.sprite.collide_mask(cursor, self):
                return True
            else :
                return False

    def delete(self) :
        if self.control_point != self.depart :
            self.control_point.delete_control()
        for groupe in self.group :
            groupe.remove(self)
        self.depart.voisins.remove(self.arrivee)
        self.arrivee.voisins.remove(self.depart)

    def update_pos(self) :
        Z = self.bezier()
        self.image = self.create_graph(Z)
        coords =  (min([z[0] for z in Z]), min([z[1] for z in Z]))
        self.rect = self.image.get_rect(topleft = coords)

        self.mask = pygame.mask.from_surface(self.image)
        self.color = 'black'

    def create_graph(self, Z) :
        """
        affiche des lignes entre les points de Z, sur une surface que l'on retourne (return surface)
        """
        A = [z[0] for z in Z]
        B = [z[1] for z in Z]
        a, b = max(A), min(A)
        c, d = max(B), min(B)

        surface = pygame.Surface( (int(a - b), int(c - d)))
        surface.fill('white')
        surface.set_colorkey('white')
        Z = [(z[0]- b, z[1] - d ) for z in Z]
        pygame.draw.lines(surface, color = 'black', closed = False, points = Z)

        return surface
    
    def bezier(self) :
        X = np.linspace(0, 1, 10)
        points = [np.array([self.depart.rect.centerx,self.depart.rect.centery]), 
        np.array([self.control_point.rect.centerx,self.control_point.rect.centery]),
        np.array([self.control_point.rect.centerx,self.control_point.rect.centery]),
        np.array([self.arrivee.rect.centerx, self.arrivee.rect.centery])
        ]
        Z = [Edge.bezier_pol_4(t, points) for t in X]
        return Z
		
    def bezier_pol_4(t, points) :
        return( points[0]*(1-t)**3 + 3*points[1]*t*(1-t)**2 + 3*points[2]*(t**2)*(1-t) + points[3]*t**3)