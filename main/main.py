import pygame, sys
from settings import *
from level import Level
from start_menu import Start_menu
from debug import debug

class Game :
    def __init__(self) :
        pygame.init()
        self.screen = pygame.display.set_mode((xres, yres))
        pygame.display.set_caption("Cops and Robber")
        self.clock = pygame.time.Clock()
        self.cop_victory = 0  #nbre de victoires cop
        self.robber_victory = 0   #nbre de victoires robber
        self.cop_numb = 2
        self.round_numb = 4
        self.graphe_id = 1
        self.start_menu = Start_menu(self.cop_victory, self.robber_victory, self.cop_numb, self.round_numb, self.graphe_id)
        self.level = Level()
        
    def run(self):
        while True :
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()
            self.screen.fill('grey')

            if self.level.is_Finished :
                if self.level.winner == 'Cop' :
                    self.cop_victory += 1
                elif self.level.winner == 'Robber' :
                    self.robber_victory += 1

                self.reinitialiser()

            if self.start_menu.is_Finished :
                if self.level.is_Initialised :       
                    self.level.run(ev)
                else :
                    self.cop_numb = self.start_menu.cop_numb
                    self.round_numb = self.start_menu.round_numb
                    self.level.initialisation(self.cop_numb, self.round_numb+1, self.graphe_id)
            else :
                self.start_menu.run(ev)
                if self.graphe_id != self.start_menu.graph_id :
                    self.graphe_id = self.start_menu.graph_id                
            #debug(pygame.mouse.get_pos())
            pygame.display.update()

    def reinitialiser(self) : #relance une partie
        del self.start_menu
        self.start_menu = Start_menu(self.cop_victory, self.robber_victory, self.cop_numb, self.round_numb, self.graphe_id)
        del self.level
        self.level = Level()

if __name__ == '__main__' :
    game = Game()
    game.run()