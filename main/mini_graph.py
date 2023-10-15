from re import S
import pygame
import pickle
from vertice import Vertice
from edge import Edge
from object import Object

class Mini_Graph(Object) :
    def __init__(self, groups, pos, graph_id) :
        super().__init__(groups, pos, name = 'choose_graphe_bg.png')
        self.graph_id = graph_id
        self.add_image('choose_graphe_bg_down.png', 'hover')
        self.add_image('choose_graphe_bg_selected.png', 'selected')
        self.visible_sprites = pygame.sprite.LayeredUpdates()
        self.vertices = pygame.sprite.LayeredUpdates()
        self.initialisation()
        self.visible_sprites.draw(self.image)
        self.visible_sprites.draw(self.image_dict['selected'])
        self.visible_sprites.draw(self.image_dict['hover'])
        

    def initialisation(self) :
        with open('../data/graph', 'rb') as f :
            D = pickle.load(f)
        n = len(D)

        if self.graph_id <= n :
            (X, U) = D[str('graphe_'+str(self.graph_id))]
            vertice_number = 0
            for vertex in X :
                new_pos = (vertex[0]/4, vertex[1]/4)
                Vertice(groups =  [self.visible_sprites, self.vertices] , pos = new_pos, id = vertice_number, scale = 0.25)
                vertice_number += 1
            for edge in U :
                for vertex_1 in self.vertices :
                    for vertex_2 in self.vertices :
                        if (vertex_1.id in edge) and (vertex_2.id in edge) :
                            vertex_1.voisins.add(vertex_2)
                            vertex_2.voisins.add(vertex_1)
                            Edge([self.visible_sprites], vertex_1, vertex_2)