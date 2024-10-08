import packet

import random
import premade
import utils

from actor import Actor

PLAYER_STATS = {
    'hp':       20,
    'mp':       20,
    'max_hp':   20,
    'max_mp':   20,
    'exp':      0,
    'points':   0,

    'crit_chance':  5,
    'dodge_chance': 5,

    'str': 2,
    'agi': 2,
    'int': 2,
    

}

class Player(Actor):
    def __init__(self, protocol, name, stats = PLAYER_STATS, equipment = [], inventory = {}, room = None):
        self.protocol = protocol
        self.name = name
        self.stats = utils.dc(stats)
        self.status_effects = {}
        self.equipment = utils.dc(equipment)
        self.inventory = utils.dc(inventory)
        self.room = room
        
        self.skills = []
        self.skill_cooldowns = {}

        self.target = None
        self.premade = self.protocol.factory.premade
    
        self.dead = False
        self.respawn_at = 0

        self.logoff = False

        super().__init__()

    def character_sheet(self, short = False):
        if short:
            return {
                'name':         self.name,
                'stats':        self.stats,
                'equipment':    self.equipment
                }

        

        #print(self.skills)
        if self.target == None:
            _target_name = None
        else:
            _target_name = self.target.name
        return {
            'name':             self.name,
            'stats':            self.stats,
            'equipment':        self.equipment,
            'inventory':        self.inventory,
            'target':           _target_name,
            'skills':           self.skills,
            'skill_cooldowns':  self.skill_cooldowns
            }

    def respawn(self):
        self.dead = False
        self.stats['hp'] = self.stats['max_hp']
        self.stats['mp'] = self.stats['max_mp']
        self.room.move_player(self, 'spawn', forced = True)
        self.target = None

    def die(self):
        self.broadcast(f'{self.name} has died!')
        self.protocol.onPacket(self.protocol,packet.FlavouredMessagePacket('You are dead... Respawning in 10 seconds','death'))
        self.stats['hp'] = 0
        self.stats['mp'] = 0
        self.target = None
        super().die()
        #self.room.move_player(self, 'Small Town', forced = True)
        #self.target = None
        
    def set_target(self,target):
        if target == None:
            self.target = None
            return

        if target not in self.room.players and target not in self.room.enemies:
            self.target = None
            self.broadcast('Can\'t find Target!', self)
            return 'Can\'t find Target!'

        if target in self.room.players:
            self.target = self.room.players[target]
            
        if target in self.room.enemies:
            self.target = self.room.enemies[target]
            
        return f'{self.name} targets {self.target.name}'

    def remove_item(self,item_id,quantity):
        if item_id not in self.inventory:
            return 'you do not have this item in the inventory'
        if self.inventory[item_id] < quantity:
            return 'you do not have that quantity of this item'
        if self.inventory[item_id] <= -1:
            return 'cant remove less than 0 of an item'
        # if you drop 0 then you drop everything
        if quantity == 0:
            quantity = self.inventory[item_id]
        
        self.inventory[item_id] -= quantity

        if self.inventory[item_id] == 0:
            del self.inventory[item_id]

    def add_item(self,item_id,quantity):
        if item_id not in self.protocol.factory.premade['items']:
            return
        
        
        if item_id in self.inventory:
            self.inventory[item_id] += quantity
        else:
            self.inventory[item_id] = quantity

    def reload_skills(self):
        self.skills = []
        for e in self.equipment:
            if 'skills' not in self.protocol.factory.premade['items'][e]:
                continue
            for skill in self.protocol.factory.premade['items'][e]['skills']:
                if skill not in self.skills:
                    self.skills.append(skill)

    def equip(self, item_id, forced = False):
        ITEMS = self.premade['items']
        if item_id not in ITEMS:
            return 'item does not exist'
        if item_id not in self.inventory and not forced:
            return 'you do not have that item in the inventory'
        if 'slot' not in ITEMS[item_id]:
            return 'item is not equipable'

        item_dict = ITEMS[item_id]
        
        for equiped_item in self.equipment:
            if ITEMS[equiped_item]['slot'] == item_dict['slot']:
                self.unequip(equiped_item)
                #return f'You have an item already equipped in slot: {ITEMS[equiped_item]["slot"]}'
        
        for s in ITEMS[item_id]['stats']:
            
            self.stats[s] += ITEMS[item_id]['stats'][s]

        self.equipment.append(item_id)
        if not forced: 
            self.remove_item(item_id,1)
        self.reload_skills()
        return f'{item_id} equipped'

    def unequip(self,item_id):
        ITEMS = self.premade['items']
        if item_id not in self.equipment:
            return 'cant unequip a not equiped item'

        self.add_item(item_id,1)

        for s in ITEMS[item_id]['stats']:
            self.stats[s] -= ITEMS[item_id]['stats'][s]

        self.regen()

        self.equipment.remove(item_id)
        self.reload_skills()
        return f'{item_id} unequiped'

    def room_update(self):
        p = packet.RoomPacket(  self.room.name, 
                                self.room.description, 
                                [room.name for room in self.room.exits.values()], 
                                self.room.get_players(),
                                self.room.get_enemies(),
                                self.room.get_npcs())
                                
        self.protocol.onPacket(self.protocol, p)

        p = packet.CharacterSheetPacket(self.character_sheet())
        self.protocol.onPacket(self.protocol, p)

    def tick(self):
        super().tick()
        if not self.dead: 
            if self.protocol.factory.server_time % (30*60) == 0:
                self.regen(hp = 1)
                self.regen(mp = 1)

        if self.protocol.factory.server_time % 10 == 0:
           self.room_update()

        if self.logoff:
            for i in self.status_effects:
                self.status_effects[i] = 0

            # remove any status effects before logging out
            if len(self.status_effects) == 0 and self.dead == False:
                self.room.map.factory.database.save_player(self)
                del self.room.players[self.name]
                self.room = None
                #print(self.name, 'logged off')

        



        
        

        