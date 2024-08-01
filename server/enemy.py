import packet

import random

import utils
import premade
from actor import Actor

def new(enemy_id, name = None):
    names = 'Geo Nuggy Sinclair Nigghtz Doey Shmoo Kuro Mana Redpot'
    names = names.split()

    stats = utils.dc(premade.ENEMY_STATS)

    if name == None:
        name = random.choice(names)

    match enemy_id:
        case 'skeleton':
            name += ' The Skeleton'
            skills = ['slash','guard']
        case 'slime':
            name += ' The Slime'
            skills = ['stab']
            stats['max_hp'] = 20

    stats['hp'] = stats['max_hp']
    stats['mp'] = stats['max_mp']
            
    enemy = Enemy(name,stats,skills)
    return enemy

class Enemy(Actor):
    def __init__(self, name, stats, skills):
        self.name = name
        self.stats = utils.dc(stats)
        self.room = None
        self.tag = 'enemy'
        self.ticks_passed = 0
        self.target = self
        self.skills = utils.dc(skills)
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
        for player in self.room.players:
            p = packet.FlavouredMessagePacket(f'{self.name} Died.')
            self.room.players[player].protocol.onPacket(None, p)

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
        
        

if __name__ == '__main__':
    e = new('skeleton')
    print(e.name,e.stats,e.skills)