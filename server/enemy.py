import packet

import random

import utils

from actor import Actor

ENEMY_STATS = {
    'hp':       10,
    'mp':       10,
    'max_hp':   10,
    'max_mp':   10,

    'crit_chance':  10,
    'dodge_chance': 10,
    'str': 2,
    'agi': 2,
    'int': 2,
    
    'crit_chance':  5,
    'dodge_chance': 5,
}

class Enemy(Actor):
    def __init__(self, name, stats = ENEMY_STATS, skills = ['Guard'], loot_table = []):
        self.name = name
       
        self.room = None
        self.tag = 'enemy'
        self.id = 'No ID'
        self.ticks_passed = 0
        self.target = None
        
        self.stats = utils.dc(stats)
        self.status_effects = {}
        self.skills = utils.dc(skills)
        self.loot_table = utils.dc(loot_table)

        self.skill_cooldowns = {}
        self.player_damages = {}


        self.roaming_text = ['Groans...','Roams around.','Farts.']
        self.chance_to_roam = 100

    def roll_loot(self, owner):
        all_loot = {}
        for i in self.loot_table:

            if i not in self.room.map.factory.premade['items']:
                print(f'ERROR: "{self.name}" in room "{self.room.name}" tried to drop item "{i}" but this does not exist!!!')
                self.broadcast(f'ERROR: "{self.name}" in room "{self.room.name}" tried to drop item "{i}" but this does not exist!!!')
                return

            drop_chance = random.randrange(0,1_000_000)/1_000_000

            if drop_chance > self.loot_table[i]['drop_chance']:
                continue

            if self.loot_table[i]['quantity_max'] - self.loot_table[i]['quantity_min'] > 1:
                quantity = random.randrange(self.loot_table[i]['quantity_min'],self.loot_table[i]['quantity_max'])
            else:
                quantity = 1
            owner.add_item(i,quantity)
            all_loot[self.room.map.factory.premade['items'][i]["name"]] = quantity

        if len(all_loot) <= 0:
            return

        loot_text = 'Loot dropped: '
        for i in all_loot:
            loot_text += f' {i} x{all_loot[i]}   '
        self.broadcast(loot_text, owner)


    def character_sheet(self, short = False):
        # return the character sheet 
        return {
            'name':         self.name,
            'stats':        self.stats,
            }

    def die(self):
        _killer = {'name':'what the fuck this is a bug'}
        _damage = 0
        for player in self.player_damages:
            # untarget if dead
            if player in self.room.players:
                if self.room.players[player].target == self:
                    self.room.players[player].target = None


            if self.player_damages[player] > _damage:
                _killer = player
                _damage = self.player_damages[player] 



        
        if _killer in self.room.players:
            _killer = self.room.players[_killer]
        else:
            self.broadcast(f'{self.name} Died...')
            self.room.remove_enemy(self)
            self.room = None
            return



        self.broadcast(f'{self.name} Died at the hands of {_killer.name}')
        self.roll_loot(_killer)
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


            self.use_skill(random.choice(self.skills))




        self.ticks_passed += 1
        if self.ticks_passed >= 30*3:
            self.ticks_passed = 0

    def take_damage(self, damage, stat, source, skill = None):
        
    
        if source.name in self.player_damages:
            self.player_damages[source.name] += damage
        else:
            self.player_damages[source.name] = damage

        super().take_damage(damage, stat, source, skill)

        
        

if __name__ == '__main__':
    e = new('skeleton')
    print(e.name,e.stats,e.skills)