import pygame
from object import Object
from settings import *

class Param() :
    def __init__(self, groups, cop_numb, round_numb) :
        
        #numbers and objects
        self.bg = Object(groups = groups[0], pos = (0,0), name = 'param_bg.png', adapt_screen = True)
        self.frame = Object(groups = groups[0], pos = (0,100), name = 'param_frame.png', center_x = True)
        pos_btn_close = (self.frame.rect.x + self.frame.image.get_width() - 45, self.frame.rect.y + 10 )
        self.param_btn_close = Object(groups = [groups[0], groups[1]], pos = pos_btn_close, name = '/create_graphe/close_btn.png', scale = 0.6)
        self.param_btn_close.add_image('/create_graphe/close_btn_down.png', 'hover')
        self.cop_numb = cop_numb
        self.round_numb = round_numb
        self.cop_numb_obj = Object(groups = groups[0], pos = (self.frame.rect.x + 225, self.frame.rect.y + 50), name = 'numbers/void.png', scale = 0.7)
        self.round_numb_obj = Object(groups = groups[0], pos = (self.frame.rect.x + 250, self.frame.rect.y + 105), name = 'numbers/void.png', scale = 0.7)
        for i in range(1,10) :
            self.cop_numb_obj.add_image('numbers/number_'+str(i)+'.png', str(i))
            self.round_numb_obj.add_image('numbers/number_'+str(i)+'.png', str(i))
        self.cop_numb_obj.image = self.cop_numb_obj.image_dict[str(self.cop_numb)]
        self.round_numb_obj.image = self.round_numb_obj.image_dict[str(self.round_numb)]

        #boolean
        self.isOpen = False
        self.user_isTyping = False
        self.user_hasSelect = None  #what the user has selected

    def run(self, events) :
         #change cop_number and round_number
        self.input(events)
        if self.user_isTyping :
            if self.user_hasSelect == self.round_numb_obj :
                self.update_round_numb(events)
            elif self.user_hasSelect == self.cop_numb_obj :
                self.update_cop_numb(events)

    def input(self, events) :
        for event in events :
            if event.type == pygame.MOUSEBUTTONDOWN :
                (x,y) = pygame.mouse.get_pos()
                if self.cop_numb_obj.rect.collidepoint((x,y)):
                    self.user_isTyping = True
                    self.user_hasSelect = self.cop_numb_obj
                    self.cop_numb_obj.animation_frame = [self.cop_numb_obj.image, self.cop_numb_obj.image_dict['base']]
                elif self.round_numb_obj.rect.collidepoint((x,y)):
                    self.user_isTyping = True
                    self.user_hasSelect = self.round_numb_obj
                    self.round_numb_obj.animation_frame = [self.round_numb_obj.image, self.round_numb_obj.image_dict['base']]

                elif  self.param_btn_close.rect.collidepoint((x,y)):
                    self.isOpen = False
                else :
                    self.user_isTyping = False

    def update_round_numb(self, events) :
        self.round_numb_obj.animate()
        for event in events :
            if event.type == pygame.KEYDOWN :
                new_round_numb = Param.user_number(event)
                if new_round_numb !=0 :
                    self.round_numb = new_round_numb
                    self.user_isTyping = False
                    self.round_numb_obj.image = self.round_numb_obj.image_dict[str(self.round_numb)]

    def update_cop_numb(self, events) :
        self.cop_numb_obj.animate()
        for event in events :
            if event.type == pygame.KEYDOWN :
                new_cop_numb = Param.user_number(event)
                if new_cop_numb !=0 :
                    self.cop_numb = new_cop_numb
                    self.user_isTyping = False
                    self.cop_numb_obj.image = self.cop_numb_obj.image_dict[str(self.cop_numb)]

    def user_number(event) :
        if event.key == pygame.K_1 :
                return 1
        elif event.key == pygame.K_2 :
                return 2
        elif event.key == pygame.K_3 :
                return 3
        elif event.key == pygame.K_4 :
                return 4
        elif event.key == pygame.K_5 :
                return 5
        elif event.key == pygame.K_6:
                return 6
        elif event.key == pygame.K_7 :
                return 7
        elif event.key == pygame.K_8 :
                return 8
        elif event.key == pygame.K_9 :
                return 9
        else :
                return 0
        
