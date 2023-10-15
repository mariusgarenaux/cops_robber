from re import I
import pygame
from vertice import Vertice
from object import Object
from edge import Edge
import pickle
from settings import *
from debug import debug

class Create_level :
    def __init__(self) :
        """
        Open a graphe editor from start_menu.
        Edges are saved in self.edges (pygame.sprite.Group() object)
        Vertices are saved in self.vertices (pygame.sprite.Group() object)
        """

        self.display_surface = pygame.display.get_surface()

        #sprite groups
        self.visible_sprites = pygame.sprite.LayeredUpdates()
        self.vertices = pygame.sprite.Group()
        self.edges = pygame.sprite.Group()
        self.control_points = pygame.sprite.Group()
        self.hover_sprite = pygame.sprite.Group()

        #objects
        self.vertice_btn = Object(groups = [self.visible_sprites, self.hover_sprite], pos = (10, 10), name = 'create_graphe/vertice_btn.png')
        self.vertice_btn.add_image('create_graphe/vertice_btn_down.png', 'hover') #for hovering effect
        self.edge_btn = Object(groups = [self.visible_sprites, self.hover_sprite], pos = (50, 10), name = 'create_graphe/edge_btn.png')
        self.edge_btn.add_image('create_graphe/edge_btn_down.png', 'hover')
        self.rubber_btn = Object(groups = [self.visible_sprites, self.hover_sprite], pos = (90, 10), name = 'create_graphe/rubber_btn.png' )
        self.rubber_btn.add_image('create_graphe/rubber_btn_down.png', 'hover')
        self.hand_btn = Object(groups = [self.visible_sprites, self.hover_sprite], pos = (130, 10), name = 'create_graphe/hand_btn.png')
        self.hand_btn.add_image('create_graphe/hand_btn_down.png', 'hover')
        self.save_btn = Object(groups = [self.visible_sprites, self.hover_sprite], pos = (170, 10), name = 'create_graphe/save_btn.png')
        self.save_btn.add_image('create_graphe/save_btn_down.png', 'hover')
        #self.bezier_btn = Object(groups = [self.visible_sprites, self.hover_sprite], pos = (210, 10), name = 'create_graphe/bezier_btn.png')
        #self.bezier_btn.add_image('create_graphe/bezier_btn_down.png')
        self.close_btn = Object(groups = [self.visible_sprites, self.hover_sprite], pos = (xres-50, 10), name = 'create_graphe/close_btn.png' )
        self.close_btn.add_image('create_graphe/close_btn_down.png', 'hover')
        self.curseur = Object(self.visible_sprites, pos = (0,0), name = 'create_graphe/cursor_void.png')
        self.visible_sprites.change_layer(self.curseur, 3)  #layer 0 = almost all sprite, layer 1 = vertices, layer 2 = msg, layer 3 = cursor
        self.curseur.add_image('create_graphe/cursor_vertice.png', 'vertice')
        self.curseur.add_image('create_graphe/cursor_rubber.png', 'rubber')
        self.curseur.add_image('create_graphe/cursor_hand.png', 'hand')
        self.curseur.image_dict['edge'] = self.curseur.image_dict['hand']
        self.curseur.image_dict['save'] = self.curseur.image_dict['base']
        self.item_hitbox = pygame.Rect(0, 0, xres, 50)
        self.saved_msg = Object(groups = [self.visible_sprites], pos = (350, 250), name = 'saved_void.png')
        self.saved_msg.add_image('saved.png', '1')
        self.visible_sprites.change_layer(self.saved_msg, 2)
        self.btn = {'vertice' : self.vertice_btn, 'edge' : self.edge_btn,'rubber' : self.rubber_btn ,'hand' : self.hand_btn,'save' : self.save_btn}


        #variables
        self.is_selected = 'none'
        self.vertice_number = 0
        self.vertice_selected_1 = False
        self.is_Open = False
        self.graphe_id = 0
        self.timer = 0

    def run(self, events) :
        """
        main loop of create_level
        redirect to different method according to self.is_selected
        events = pygame.event.get()
        """
        pos = pygame.mouse.get_pos()
        self.curseur.rect.topleft = (pos[0]-15, pos[1]-15)

        if self.close_btn.is_Clicked(pos, events) :
            self.is_selected = 'none'
            self.is_Open = False

        if self.is_selected == 'edge' :
            self.add_edge(pos, events)

        elif self.is_selected == 'vertice' :
            self.add_vertex(pos, events)
                
        elif self.is_selected == 'rubber' :
            self.rubber_run(pos, events)

        elif self.is_selected == 'hand' :
            self.hand_run(pos, events)

        elif self.is_selected == 'save' :
            if self.timer >= 1 :
                self.timer = 0
                self.saved_msg.image = self.saved_msg.image_dict['base']
                self.save_run()
            else :
                self.saved_msg.image = self.saved_msg.image_dict['1']
                self.timer += 0.005
        
        elif self.is_selected == 'bezier' :
            self.bezier_run(pos, events)
        else :
            pass

        self.update(pos, events)
        self.visible_sprites.draw(self.display_surface)

    def update(self, pos, events) :
        """
        update the tool selected  (update self.is_selected)
        doesnt do anything if the user doesnt change tool
        pos = (x, y) -> mouse position at the moment
        events = liste of events (pygame.event.get())
        """
        is_selected = self.is_selected

        #update value of is_selected
        for btn in self.btn:
            if self.btn[btn].is_Clicked(pos, events) :
                is_selected = btn

        #update the cursor image
        if is_selected == 'none' :
            self.curseur.image = self.curseur.image_dict['base']
            pygame.mouse.set_visible(True)
        else :
            pygame.mouse.set_visible(False)
            self.curseur.image = self.curseur.image_dict[is_selected]
        
        if self.is_selected != is_selected :
            self.is_selected = is_selected

        self.update_hover(pos)
        
    def update_hover(self, pos) :
        """
        update the hovered sprites
        """
        hover = False
        for hovered_sprite in self.hover_sprite :
            if hovered_sprite.hover(pos) :
                hover = True
        if hover :
            pygame.mouse.set_visible(False)
            self.curseur.image = self.curseur.image_dict['hand']            
        elif self.is_selected == 'none' : 
            self.curseur.image = self.curseur.image_dict['base']
            pygame.mouse.set_visible(True)

    def no_collision(self, pos, except_vertex = None) :
        """
        to check the user doesnt add a vertex too near of an other
        pos = (x, y) -> mouse position 
        return Boolean :
            True = the mouse doesnt collide any vertex
            False = the mouse collide a vertex
        """
        test = True
        if  pos[1] < 60 or pos[0] < 70 or pos[1] > yres - 60 or pos[0]> xres-60 :
            test = False

        elif not self.vertices :
            return True

        else :
            for vertice in self.vertices :  
                if vertice.hitbox.collidepoint(pos) and vertice != except_vertex :
                    test = False
        return test

    def rubber_run(self, pos, events) :
        """
        Use the tool to delete some objects
        pos = (x, y) -> mouse position at the moment
        events = liste of events (pygame.event.get())
        """
        for edge in self.edges :
            edge.hover(pos, self.curseur)
            if edge.is_Clicked(pos, events, self.curseur) :
                edge.delete()

        for vertice in self.vertices :
            vertice.hover(pos)
            if vertice.is_Clicked(pos, events) :
                vertice.delete(self.edges)
        
        for control_point in self.control_points :
            if control_point.is_Clicked(pos, events) :
                for edge in self.edges :
                    if edge.control_point == control_point :
                        edge.control_point = edge.depart
                        edge.update_pos()
                control_point.delete_control()

    def add_edge(self, pos, events) :
        """
        Use the tool to add an edge
        pos = (x, y) -> mouse position at the moment
        events = liste of events (pygame.event.get())
        """
        for event in events :
            if event.type == pygame.MOUSEBUTTONDOWN  and  self.vertices:
                for vertice in self.vertices :
                    if vertice.rect.collidepoint(pos) :
                        if self.vertice_selected_1 : 
                            self.vertice_selected_1.voisins.add(vertice)
                            vertice.voisins.add(self.vertice_selected_1)
                            Edge([self.visible_sprites, self.edges], self.vertice_selected_1, vertice)
                            self.vertice_selected_1 = False
                        else :
                            self.vertice_selected_1 = vertice

    def add_vertex(self, pos, events) :
        """
        Use the tool to add a vertex
        pos = (x, y) -> mouse position at the moment
        events = liste of events (pygame.event.get())
        """
        for event in events :
            if event.type == pygame.MOUSEBUTTONDOWN  and self.no_collision(pos):
                Vertice(groups =  [self.visible_sprites, self.vertices] ,pos = pos, id = self.vertice_number)
                self.vertice_number += 1

    def hand_run(self, pos, events) :
        """
        Use the tool to move vertices
        pos = (x, y) -> mouse position at the moment
        events = liste of events (pygame.event.get())
        """
        someone_is_selected = False
        for vertex in self.vertices :
            if vertex.is_selected :
                someone_is_selected = True
                vertex_selected = vertex
                vertex.is_selected = True
                for edge in self.edges :
                    if edge.depart == vertex or edge.arrivee == vertex: 
                        edge.update_pos()
        
        if someone_is_selected :
            vertex_selected.rect.topleft = (pos[0]- 20, pos[1] - 20)
            vertex_selected.hitbox_update()
            for event in events :
                if event.type == pygame.MOUSEBUTTONDOWN and self.no_collision(pos, vertex_selected):
                    vertex_selected.is_selected = False
        else :
            for event in events :
                if event.type == pygame.MOUSEBUTTONDOWN :
                    for vertex in self.vertices :
                        if vertex.rect.collidepoint(pos) :
                            vertex.is_selected = True

    def save_run(self) :
        """
        transform the current graph in two list stored a pickle:
        X = vertices pos (x, y)
        U = list of edges (elements are lists of two integers)
        """
        with open ('../data/graph', 'rb') as d :
            D = pickle.load(d)
        n = len(D)
        X = []
        U = []
        i = 0
        for vertex_1 in self.vertices :
            vertex_1.id = i 
            i+= 1
            X.append((vertex_1.rect.x+20, vertex_1.rect.y+20))

        for vertex_1 in self.vertices :    
            for vertex_2 in self.vertices :
                if vertex_1 in vertex_2.voisins and not(  ([vertex_1.id, vertex_2.id] in U ) or ([vertex_2.id, vertex_1.id] in U) ) and vertex_1 != vertex_2:
                    U.append([vertex_1.id, vertex_2.id])

        if self.graphe_id > 0 :
            name = 'graphe_'+str(self.graphe_id)
        else :
            name = 'graphe_'+str(n+1)

        D[name] = (X, U)

        with open('../data/graph', 'wb') as d :
            pickle.dump(D, d)

        self.is_selected = 'none'
        #self.msg_save.animate()

    def bezier_run(self, pos, events) : 
        """
        abandoned function
        ( it was to have curves instead of straight lines for edges )
        """
        control_point_selected = None
        #si edge n'a pas de control point, on le rajoute
        for edge in self.edges :
            edge.hover(pos, self.curseur)
            if edge.is_Clicked(pos, events, self.curseur)  :#and (edge.control_point != edge.depart):
                X = Object([self.visible_sprites, self.control_points], pos = pos, name = 'create_graphe/control_point.png')
                edge.control_point = X

        #trouve le control point selectionné, s'il y en a un
        for control_point in self.control_points :
            if control_point.is_Clicked(pos, events) :
                control_point.is_selected = not(control_point.is_selected)

        #update la position du control_point selectionné, + de l'arete correspondante
        for control_point in self.control_points :
            if control_point.is_selected :
                control_point.rect.center = pos
                control_point_selected = control_point
                break

        if control_point_selected :
            for edge in self.edges :
                if edge.control_point == control_point_selected :
                    edge.update_pos()

    def is_not_empty(self) : 
        """
        Boolean :
            True = vertices and edges (= graphe exist)
            False = no vertices OR no edges (= graphe don't exist)
        """
        return (self.vertices and self.edges)

    def initialisation(self) :
        """
        launched when the graph editor is opened
        - reinitialize sprites groups 
        - draw the graph number self.graphe_id from the data
        """
        for vertice in self.vertices :
            self.visible_sprites.remove(vertice)
            self.vertices.remove(vertice)
        for edge in self.edges :
            self.visible_sprites.remove(edge)
            self.edges.remove(edge)
        self.vertice_number = 0

        if self.graphe_id > 0 :
            with open('../data/graph', 'rb') as d :
                D = pickle.load(d)

            (X, U) = D['graphe_'+str(self.graphe_id)]
            for vertex in X :
                Vertice(groups =  [self.visible_sprites, self.vertices] ,pos = vertex, id = self.vertice_number)
                self.vertice_number += 1
            for edge in U :
                for vertex_1 in self.vertices :
                    for vertex_2 in self.vertices :
                        if (vertex_1.id in edge) and (vertex_2.id in edge) :
                            vertex_1.voisins.add(vertex_2)
                            vertex_2.voisins.add(vertex_1)
                            Edge([self.visible_sprites, self.edges], vertex_1, vertex_2)
