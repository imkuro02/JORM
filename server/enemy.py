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
        self.ticks_passed = 0

        self.roaming_text = ['Groans...','Roams around.','Farts.']
        self.chance_to_roam = 100
    
    def character_sheet(self):
        # return the character sheet 
        return {
            'name':         self.name,
            'stats':        self.stats,
            }

    def tick(self):
        if self.ticks_passed == 0:

            roam_text = random.randrange(1,self.chance_to_roam)
            if roam_text == 1:
                for player in self.room.players:
                    p = packet.ChatPacket(f'{self.name} {random.choice(self.roaming_text)}')
                    self.room.players[player].protocol.onPacket(None, p)

        self.ticks_passed += 1
        if self.ticks_passed >= 10:
            self.ticks_passed = 0
        
        

        