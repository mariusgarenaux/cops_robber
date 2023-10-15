import pygame
import pickle
from player import Player
from vertice import Vertice
from round import Round
from object import Object
from edge import Edge
from settings import *


class Level :
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.vertices = pygame.sprite.Group()
        self.edges = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.visible_sprite = pygame.sprite.LayeredUpdates()  #sprites a afficher 
        self.hover_sprite = pygame.sprite.Group()
        self.is_Initialised = False
        self.is_Finished = False
        self.every_isPlaced = False

        #small white rectangle telling the number of rounds (obj_2 is the text and the rectangle, obj is the number)
        self.round_numb_obj_2 =  Object(groups = [self.visible_sprite], pos = (300, 250), name = 'round_number_text_void.png')
        self.round_numb_obj_2.add_image('round_number_text.png', '1')
        self.round_numb_obj = Object(groups = [self.visible_sprite], pos = (310, 265), name = 'numbers/void.png')
        self.visible_sprite.change_layer(self.round_numb_obj_2, 2)
        self.visible_sprite.change_layer(self.round_numb_obj, 2)
        for i in range(1, 10) :
            self.round_numb_obj.add_image('numbers/number_'+str(i)+'.png', str(i))
        
        #numbers
        self.cop_numb = 2
        self.round_numb = 5
        self.compteur_new_round = 0 #for the animation when a new round starts (ie prints round_numb_obj)

        
        self.curseur = Object(groups = [self.visible_sprite], pos = (0,0), name = 'create_graphe/cursor_void.png')
        self.curseur.add_image('create_graphe/cursor_hand.png', 'hand')
        self.curseur.image_dict['vertice_hover'] = pygame.image.load('../picture/vertice_down.png').convert_alpha()

        self.visible_sprite.change_layer(self.curseur, 3)

        self.round = Round(self.players, self.vertices, self.curseur) 
        
    def run(self, event) :
        self.every_isplaced() #check si tout le monde est placé
        if not self.round.is_Finished :  #si un round est en cours, on le continue
            if self.every_isPlaced :
                self.round.collision()        #regarde si robber est sur la meme case que cop
            self.round.run(event)
            if self.round.is_Finished_victory : #si cop a gagné
                self.is_Finished = True
                self.winner = 'cop'
        elif self.compteur_new_round <= 1  and self.round_numb > 1:
            self.round_numb_obj_2.image = self.round_numb_obj_2.image_dict['1']
            self.round_numb_obj.image = self.round_numb_obj.image_dict[str(self.round_numb-1)]
            self.compteur_new_round += 0.0005
        else :  #sinon, on en crée un nouveau
            self.compteur_new_round = 0
            self.round_numb -= 1
            self.round_numb_obj_2.image = self.round_numb_obj_2.image_dict['base']
            self.round_numb_obj.image = self.round_numb_obj.image_dict['base']
            if self.round_numb == 0 :  #si robber a gagné
                self.is_Finished = True
                self.winner = 'robber'
            else :
                self.round = Round(self.players, self.vertices, self.curseur)

        self.visible_sprite.draw(self.display_surface) #affichage

    def initialisation(self, cop_numb, round_numb, graph_id):
        """
        create the graph and the instances of Player
        """
        self.cop_numb = cop_numb
        self.round_numb = round_numb
        
        self.create_graphe(graph_id)

        for j in range(self.cop_numb) :
            Player(groups = [self.visible_sprite, self.players ], type = 'cop', vertices_sprite = self.vertices)
        Player(groups = [self.visible_sprite, self.players ], type = 'robber', vertices_sprite = self.vertices)
        
        self.is_Initialised = True

    def every_isplaced(self) :
        """
        update the value of self.every_isPlaced 
        """
        test = True
        if not self.every_isPlaced :
            for player in self.players :
                if not player.is_Placed :
                    test = False
            self.every_isPlaced = test
        
    def create_graphe(self, graphe_id) :
        """
        extract the data from '../data/graph' pickle, and create the graph
        """
        if graphe_id == 0 :
            (X, U) = (Y, V)  #default Petersen's Graph
        else :
            with open('../data/graph', 'rb') as f :
                D = pickle.load(f)
            (X, U) = D[str('graphe_'+str(graphe_id))]
        self.create_obj(X, U)
            
    def create_obj(self, X, U) :
        """
        create instances of Edges and Vertices according to X = 'list of coordinates of vertices' and U = 'vertices'
        """
        vertice_number = 0
        for vertex in X :
            Vertice(groups =  [self.visible_sprite, self.vertices] , pos = vertex, id = vertice_number)
            vertice_number += 1
        for edge in U :
            for vertex_1 in self.vertices :
                for vertex_2 in self.vertices :
                    if (vertex_1.id in edge) and (vertex_2.id in edge) :
                        vertex_1.voisins.add(vertex_2)
                        vertex_2.voisins.add(vertex_1)
                        Edge([self.visible_sprite, self.edges], vertex_1, vertex_2)