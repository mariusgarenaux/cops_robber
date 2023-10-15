import pygame
from object import Object
from param import Param
from vertice import Vertice
from create_level import Create_level
from choose_graphe import Choose_Graphe
from settings import *
from debug import debug

class Start_menu :
    def __init__(self, cop_victory, robber_victory, cop_numb, round_numb, graph_id) :
        #sprites groups
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.LayeredUpdates()
        self.visible_sprites_param = pygame.sprite.LayeredUpdates()
        self.hover_sprite = pygame.sprite.Group()
        self.hover_sprite_param = pygame.sprite.Group()
        self.mini_graphe = pygame.sprite.Group()

        #boolean
        self.is_Finished = False    #True if the game starts
        self.graph_id = graph_id

        #objects 
        self.btn = Object(groups = [self.visible_sprites, self.hover_sprite], pos = (0, 270), name = 'start_up.png', center_x = True) # start button
        self.btn.add_image('start_down.png', 'hover')
        self.param_btn = Object(groups = [self.visible_sprites, self.hover_sprite], pos = (xres - 50, 10), name = 'param_btn.png')
        self.param_btn.add_image('param_btn_down.png', 'hover')
        self.choose_graphe_btn =  Object(groups = [self.visible_sprites, self.hover_sprite], pos = (0, 450), name = 'choose_graphe_btn.png', center_x=True)
        self.choose_graphe_btn.add_image('choose_graphe_btn_down.png', 'hover')
        self.create_level_btn = Object(groups = [self.visible_sprites, self.hover_sprite], pos = (0, 360), name = 'create_graphe/create_level_btn.png', center_x = True)
        self.create_level_btn.add_image('create_graphe/create_level_btn_down.png', 'hover')
        Object(groups = self.visible_sprites,pos = (0, 20), name = 'start_img.png', center_x = True)  #title
        self.param = Param([self.visible_sprites_param, self.hover_sprite_param], cop_numb, round_numb)
        #self.visible_sprites.change_layer(self.param, 2)
        self.create_level = Create_level()
        self.choose_graphe = Choose_Graphe(self.graph_id)
        self.curseur = Object(groups = [self.visible_sprites, self.visible_sprites_param], pos = (0,0), name = 'create_graphe/cursor_void.png')
        self.visible_sprites.change_layer(self.curseur, 3)  #layer 0 = almost all sprite, layer 1 = vertices, layer 2 = msg, layer 3 = cursor
        self.visible_sprites_param.change_layer(self.curseur, 3)
        self.curseur.add_image('create_graphe/cursor_hand.png', 'hand')

        #all the numbers
        self.cop_numb = self.param.cop_numb
        self.round_numb = self.param.round_numb
        self.cop_victory = cop_victory
        self.robber_victory = robber_victory
        self.cop_victory_obj = Object(groups = self.visible_sprites, pos = (306, 148), name = 'numbers/void.png', scale = 0.5 )
        self.robber_victory_obj = Object(groups = self.visible_sprites, pos = (572, 148), name = 'numbers/void.png', scale = 0.5 )
        for i in range(1,10) :
            self.cop_victory_obj.add_image('numbers/number_'+str(i)+'.png', str(i))
            self.robber_victory_obj.add_image('numbers/number_'+str(i)+'.png', str(i))
        if self.cop_victory == 0 :
            self.cop_victory_obj.image = self.cop_victory_obj.image_dict['base']
        else :
            self.cop_victory_obj.image = self.cop_victory_obj.image_dict[str(self.cop_victory)]
        if self.robber_victory == 0 :
            self.robber_victory_obj.image = self.robber_victory_obj.image_dict['base']
        else :
            self.robber_victory_obj.image = self.robber_victory_obj.image_dict[str(self.robber_victory)]

    def run(self, events) :
        pos = pygame.mouse.get_pos()
        self.curseur.rect.topleft = (pos[0]-15, pos[1]-15)

        if self.param.isOpen :
            self.param.run(events)
            self.update_numbers()
            self.visible_sprites.draw(self.display_surface)  #pour continuer a afficher le fond
            self.visible_sprites_param.draw(self.display_surface)  #affiche les parametres
            
            #update les images hover
            hover = False
            for hovered_sprite in self.hover_sprite_param :
                if hovered_sprite.hover(pos) :
                    hover = True
            
            if hover :
                pygame.mouse.set_visible(False)
                self.curseur.image = self.curseur.image_dict['hand']          
            else : 
                self.curseur.image = self.curseur.image_dict['base']
                pygame.mouse.set_visible(True)

        elif self.create_level.is_Open :
            self.create_level.run(events)

        elif self.choose_graphe.is_Open :
            self.choose_graphe.run(events)
        else:
            self.update(events)
        
    def open_param(self, events) :
        for event in events :
            if event.type == pygame.MOUSEBUTTONDOWN and self.param_btn.rect.collidepoint(pygame.mouse.get_pos()) :
               self.param.isOpen = True

    def update_numbers(self) :
        self.cop_numb = self.param.cop_numb
        self.round_numb = self.param.round_numb

    def update(self, events) :
        pos = pygame.mouse.get_pos()
        

        #push start_button          
        if self.param.cop_numb !=0 :
            if self.btn.is_Clicked(pos, events) :
                self.is_Finished = True

        #push create_level btn
        if self.create_level_btn.is_Clicked(pos, events) :
            self.create_level.is_Open = True
            self.create_level.graphe_id = self.graph_id
            self.create_level.initialisation()
            
        if self.choose_graphe_btn.is_Clicked(pos, events) :
            self.choose_graphe.is_Open = True
            self.choose_graphe.run(events)

        #check if user open the parameters
        self.open_param(events)

        #update les images hover
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

        #update les mini_graphes
        for mini_graphe in self.mini_graphe :
            if mini_graphe.is_Clicked(pos, events) :
                self.graph_id = mini_graphe.graph_id
        self.graph_id = self.choose_graphe.graphe_id
        self.visible_sprites.draw(self.display_surface)
