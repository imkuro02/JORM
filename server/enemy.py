import packet

import random

import utils

from actor import Actor

class Loot:
    def __init__(self, item_index = 'coins', drop_chance = 100, quantity_min = 1, quantity_max = 1):
        self.item_index = item_index
        self.drop_chance = drop_chance
        self.quantity_min = quantity_min
        self.quantity_max = quantity_max

ENEMY_STATS = {
    'hp':       10,
    'mp':       10,
    'max_hp':   10,
    'max_mp':   10,

    'crit_chance':  0,
    'dodge_chance': 0,
    'physic_block': 0,
    'magic_block':  0,

    'physic_damage': 4,
    'magic_damage': 4,

    'str':      1,
    'dex':      1,
    'con':      1,
    'int':      1,
    'wis':      1,
    'cha':      1
}

class Enemy(Actor):
    def __init__(self, name, stats = ENEMY_STATS, skills = ['Guard'], loot_table = []):
        self.name = name
       
        self.room = None
        self.tag = 'enemy'
        self.id = 'No ID'
        self.ticks_passed = 0
        self.target = self
        
        self.stats = utils.dc(stats)
        self.skills = utils.dc(skills)
        self.loot_table = utils.dc(loot_table)

        self.skill_cooldowns = {}
        self.player_damages = {}


        self.roaming_text = ['Groans...','Roams around.','Farts.']
        self.chance_to_roam = 100
    
    def add_loot(self, loot: Loot):
        self.loot_table.append(loot)

    def roll_loot(self, owner):
        all_loot = {}
        for i in self.loot_table:

            if i.item_index not in self.room.map.factory.premade['items']:
                print(f'ERROR: "{self.name}" in room "{self.room.name}" tried to drop item "{i.item_index}" but this does not exist!!!')
                self.broadcast(f'ERROR: "{self.name}" in room "{self.room.name}" tried to drop item "{i.item_index}" but this does not exist!!!')
                return

            drop_chance = random.randrange(0,100)
            if drop_chance > i.drop_chance:
                continue

            if i.quantity_max - i.quantity_min > 1:
                quantity = random.randrange(i.quantity_min,i.quantity_max)
            else:
                quantity = 1
            owner.add_item(i.item_index,quantity)
            all_loot[self.room.map.factory.premade['items'][i.item_index]["name"]] = quantity

        if len(all_loot) <= 0:
            return

        loot_text = 'Loot dropped: '
        for i in all_loot:
            loot_text += f' {i} x{all_loot[i]}   '
        self.broadcast(loot_text, owner)


    def character_sheet(self):
        # return the character sheet 
        return {
            'name':         self.name,
            'stats':        self.stats,
            }

    def die(self):
        _killer = None
        _damage = 0
        for player in self.player_damages:
            if self.player_damages[player] > _damage:
                _killer = player
                _damage = self.player_damages[player] 



        if _killer in self.room.players:
            _killer = self.room.players[_killer]

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

            if self.target != self:
                self.use_skill(random.choice(self.skills))



        self.ticks_passed += 1
        if self.ticks_passed >= 30*3:
            self.ticks_passed = 0

    def take_damage(self, dmg, source):
        self.stats['hp'] -= dmg
        if source.name in self.player_damages:
            self.player_damages[source.name] += dmg
        else:
            self.player_damages[source.name] = dmg

        
        

if __name__ == '__main__':
    e = new('skeleton')
    print(e.name,e.stats,e.skills)