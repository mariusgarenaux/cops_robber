import pygame
from mini_graph import Mini_Graph
from object import Object
from debug import *
from settings import *

class Choose_Graphe() :
    def __init__(self, graph_id = 0) :
        """
        Screen for the selection of graphs. 9 mini-graphs are displayed, with data from data/graph.
        """
        self.screen = pygame.display.get_surface()

        #groups 
        self.visible_sprites = pygame.sprite.LayeredUpdates()
        self.hover_sprite = pygame.sprite.Group()
        self.mini_graphe = pygame.sprite.Group()

        #graphes
        self.graph_1 = Mini_Graph(groups = [self.visible_sprites, self.hover_sprite, self.mini_graphe], pos = (92, 70), graph_id = 1)
        self.graph_2 = Mini_Graph(groups = [self.visible_sprites, self.hover_sprite, self.mini_graphe], pos = (328, 70), graph_id = 2)
        self.graph_3 = Mini_Graph(groups = [self.visible_sprites, self.hover_sprite, self.mini_graphe], pos = (563, 70), graph_id = 3)
        self.graph_4 = Mini_Graph(groups = [self.visible_sprites, self.hover_sprite, self.mini_graphe], pos = (92, 230), graph_id = 4)
        self.graph_5 = Mini_Graph(groups = [self.visible_sprites, self.hover_sprite, self.mini_graphe], pos = (328, 230), graph_id = 5)
        self.graph_6 = Mini_Graph(groups = [self.visible_sprites, self.hover_sprite, self.mini_graphe], pos = (563, 230), graph_id = 6)
        self.graph_7 = Mini_Graph(groups = [self.visible_sprites, self.hover_sprite, self.mini_graphe], pos = (92, 390), graph_id = 7)
        self.graph_8 = Mini_Graph(groups = [self.visible_sprites, self.hover_sprite, self.mini_graphe], pos = (328, 390), graph_id = 8)
        self.graph_9 = Mini_Graph(groups = [self.visible_sprites, self.hover_sprite, self.mini_graphe], pos = (563, 390), graph_id = 9)

        #objects
        self.btn_close = Object(groups = [self.visible_sprites, self.hover_sprite], pos = (xres-50, 10), name = 'create_graphe/close_btn.png')
        self.btn_close.add_image('create_graphe/close_btn_down.png', 'hover')
        self.curseur = Object(groups = [self.visible_sprites], pos = (0,0), name = 'create_graphe/cursor_void.png')
        self.visible_sprites.change_layer(self.curseur, 3)  #layer 0 = almost all sprite, layer 1 = vertices, layer 2 = msg, layer 3 = cursor
        self.curseur.add_image('create_graphe/cursor_hand.png', 'hand')

        #booleans
        self.is_Open = False

        #variables
        self.graphe_id = graph_id
        self.graphe_selected = None #type : object Mini_Graph, currently selected

    def run(self, events) :
        """
        main loop
        """
        pos = pygame.mouse.get_pos()
        self.curseur.rect.topleft = (pos[0]-15, pos[1]-15)

        if self.btn_close.is_Clicked(pos, events) :
            self.is_Open = False

        #update hovered images
        hover = False
        for hovered_sprite in self.hover_sprite :
            if hovered_sprite.hover(pos) : 
                hover = True
        
        if hover :
            pygame.mouse.set_visible(False)
            self.curseur.image = self.curseur.image_dict['hand']            
        else : 
            self.curseur.image = self.curseur.image_dict['base']
            pygame.mouse.set_visible(True)

        for mini_graphe in self.mini_graphe :
            if mini_graphe == self.graphe_selected :
                mini_graphe.image = mini_graphe.image_dict['selected']
            elif mini_graphe.hover(pos) :
                mini_graphe.image = mini_graphe.image_dict['hover']
            else :
                mini_graphe.image = mini_graphe.image_dict['base']

        #update self.graphe_selected
        for mini_graphe in self.mini_graphe :
            if mini_graphe.is_Clicked(pos, events) :
                self.graphe_selected = mini_graphe
                self.graphe_id = mini_graphe.graph_id

        self.visible_sprites.draw(self.screen)