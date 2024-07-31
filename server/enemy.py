import packet

import random

import utils

from actor import Actor

class Enemy(Actor):
    def __init__(self, name, stats):
        self.name = name
        self.base_stats = utils.dc(stats)
        self.stats = utils.dc(self.base_stats)
        self.room = None
        self.tag = 'enemy'
        self.ticks_passed = 0
        self.target = self
        self.skills = ['slash','stab','guard']
        self.skill_cooldowns = {}
        

        self.roaming_text = ['Groans...','Roams around.','Farts.']
        self.chance_to_roam = 100
    
    def character_sheet(self):
        # return the character sheet 
        return {
            'name':         self.name,
            'stats':        self.stats,
            }

    def die(self):
        
        self.room.remove_enemy(self)
        self.room = None

    def tick(self):
        super().tick()

        if self.ticks_passed == 0:

            roam_text = random.randrange(1,self.chance_to_roam)
            if roam_text == 1:
                choice = random.choice(self.roaming_text)
                for player in self.room.players:
                    p = packet.FlavouredMessagePacket(f'{self.name} {choice}')
                    self.room.players[player].protocol.onPacket(None, p)

            
            for player in self.room.players:
                if self.room.players[player].target == self:
                    self.target = self.room.players[player]

            if self.target != self:
                self.use_skill(random.choice(self.skills))



        self.ticks_passed += 1
        if self.ticks_passed >= 30*3:
            self.ticks_passed = 0
        
        

        