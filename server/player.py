import packet

import random
import premade
import utils

from actor import Actor

class Player(Actor):
    def __init__(self, protocol, name, stats = premade.PLAYER_STATS, equipment = [], inventory = {}, room = None):
        self.protocol = protocol
        self.name = name
        self.stats = utils.dc(stats)
        self.equipment = utils.dc(equipment)
        self.inventory = utils.dc(inventory)
        self.room = room

        self.target = self

        self.ticks_passed = 0

        self.premade = self.protocol.factory.premade
    
    def character_sheet(self):
        return {
            'name':         self.name,
            'stats':        self.stats,
            'equipment':    self.equipment,
            'inventory':    self.inventory,
            'target':       self.target.name
            }

    def set_target(self,target):
        if target not in self.room.players and target not in self.room.enemies:
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
        if self.inventory[item_id] <= 0:
            return 'cant remove less than 0 of an item'
        
        self.inventory[item_id] -= quantity

        if self.inventory[item_id] == 0:
            del self.inventory[item_id]

    def add_item(self,item_id,quantity):
        if item_id in self.inventory:
            self.inventory[item_id] += quantity
        else:
            self.inventory[item_id] = quantity

    def equip(self,item_id):
        ITEMS = self.premade['items']
        if item_id not in ITEMS:
            return 'item does not exist'
        if item_id not in self.inventory:
            return 'you do not have that item in the inventory'
        if 'slot' not in ITEMS[item_id]:
            return 'item is not equipable'

        item_dict = ITEMS[item_id]
        
        for equiped_item in self.equipment:
            if ITEMS[equiped_item]['slot'] == item_dict['slot']:
                return f'You have an item already equipped in slot: {ITEMS[equiped_item]["slot"]}'
        
        for s in ITEMS[item_id]['stats']:
            self.stats[s] += ITEMS[item_id]['stats'][s]

        self.equipment.append(item_id)
        self.remove_item(item_id,1)
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
        return f'{item_id} unequiped'

    def tick(self):
        
        if self.ticks_passed % (30*3) == 0:
            self.regen(hp = self.stats['con'])
            self.regen(mp = self.stats['int'])

        if self.ticks_passed % 3 == 0:
            #print(self.character_sheet())
            # send player a updated version of the room
            p = packet.RoomPacket(  self.room.name, 
                                    self.room.description, 
                                    [room_name for room_name in self.room.exits], 
                                    self.room.get_players(),
                                    self.room.get_enemies())
            self.protocol.onPacket(self.protocol, p)

            p = packet.CharacterSheetPacket(self.character_sheet())
            self.protocol.onPacket(self.protocol, p)

        self.ticks_passed += 1

        if self.ticks_passed >= 30*10:
            self.ticks_passed = 0
        
        

        