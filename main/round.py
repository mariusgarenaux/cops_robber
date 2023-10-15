from player import Player

class Round: 
    exist = False #True s'il existe une instance en vie
    R = []

    def __init__(self, players, vertices, curseur) :
        self.players = players #sprite group
        self.vertices = vertices  #sprite group
        self.is_Finished = False  #tells if the round is finished
        self.is_Finished_victory = False #dit si qq a gagné
        self.curseur = curseur
        Round.R.append(self)
        Round.exist = True

    def run(self, event) :
        everyhas_Played = True  #pour arreter le round si tout le monde a joué
        if self.is_Finished :
            del self
            Round.R = []
            Round.exist = False
            
        else :
            for player in self.players : 
                if not player.has_Played :
                    everyhas_Played = False
                    if player.is_Placed : #si player est placé et est en train de jouer, on update son image
                        player.image = player.image_dict['isPlaying']
                    player.move(event, self.curseur)
                    break

            if everyhas_Played:
                self.is_Finished = True  #si on est la, tous les joueurs ont joué
                for player in self.players :
                    player.has_Played = False #on reinitialise pour le prochain round
    
    def collision(self) :
        for player in self.players :
            if player.type == 'robber' :
                robber = player
        for player in self.players :
            if player.vertice == robber.vertice and player.type == 'cop':
                self.is_Finished = True
                self.is_Finished_victory = True
  
