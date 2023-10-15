import pygame 
from object import Object

class Vertice(Object):

    def __init__(self, groups, pos, id, scale = 1):
        self.scale = scale
        newpos = (pos[0]-20*scale, pos[1]-20*scale)
        super().__init__(groups = groups, pos = newpos, name = 'create_graphe/vertice.png', scale = scale)
        groups[0].change_layer(self, 1)
        self.add_image('create_graphe/vertice_down.png', 'hover')
        self.voisins = pygame.sprite.Group() #liste des voisins de self; on les rajoute/enleves au fur et a mesure de la creation
        self.voisins.add(self)
        self.group.append(self.voisins)
        self.id = id
        self.hitbox = pygame.Rect((pos[0]-65*scale, pos[1]-65*scale), (130*scale, 130*scale))

    def new_voisin(self, i, vertices) :
        for vertice in vertices :
            if vertice.id == i :
                self.voisins.add(vertice)

    def draw(vertice_list, surface) :
        for vertice_1 in vertice_list :
            for vertice_2 in vertice_list :
                if vertice_1 in vertice_2.voisins :
                    pygame.draw.line(surface, color = 'black', start_pos = vertice_1.rect.center, end_pos = vertice_2.rect.center)

    def delete(self, edges) :
        for edge in edges :
            if self == edge.depart or self == edge.arrivee :
                edge.delete()
        for groupe in self.group :
            groupe.remove(self)
        for voisin in self.voisins :
            voisin.voisins.remove(self)

    def hitbox_update(self) :
        pos = self.rect.topleft
        self.hitbox.topleft = (pos[0]-65*self.scale, pos[1]-65*self.scale)