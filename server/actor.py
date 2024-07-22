import packet

import random

import utils

class Actor:
    def __init__(self, protocol, name, stats, equipment, inventory, room):
        self.protocol = protocol
        self.name = name
        self.base_stats = utils.dc(stats)
        self.stats = utils.dc(self.base_stats)
        self.equipment = equipment
        self.inventory = inventory
        self.room = room
        self.ticks_passed = 0

        self.premade = self.protocol.factory.premade
    
    def character_sheet(self):
        ITEMS = self.premade['items']
        # create a copy of base stats and reset stats
        self.stats = utils.dc(self.base_stats)
        
        # check every piece of equipment
        for equipment in self.equipment:
            # add each stat in the equipment to the stat in self.stats
            for stat in ITEMS[equipment]['stats']:
                self.stats[stat] += ITEMS[equipment]['stats'][stat]

        # return the character sheet 
        return {
            'name':         self.name,
            'stats':        self.stats,
            'equipment':    self.equipment,
            'inventory':    self.inventory
            }

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
        
        self.equipment.append(item_id)
        self.remove_item(item_id,1)
        return f'{item_id} equipped'

    def unequip(self,item_id):
        if item_id not in self.equipment:
            return 'cant unequip a not equiped item'

        self.add_item(item_id,1)
        self.equipment.remove(item_id)
        return f'{item_id} unequiped'


    def tick(self):
        
        if self.ticks_passed == 0:
            #print(self.character_sheet())
            # send player a updated version of the room
            p = packet.RoomPacket(  self.room.name, 
                                    self.room.description, 
                                    [room_name for room_name in self.room.exits], 
                                    [self.room.players[player_name].character_sheet() for player_name in self.room.players],
                                    [self.room.enemies[enemy_name].character_sheet() for enemy_name in self.room.enemies])
            self.protocol.onPacket(self.protocol, p)

            p = packet.CharacterSheetPacket(self.character_sheet())
            self.protocol.onPacket(self.protocol, p)

            ''' DEBUG 
            # move the player to a random room
            exits = []
            for i in self.room.exits:
                exits.append(i)

            random_exit = random.choice(exits)
            self.room.move_player(self,random_exit)
             DEBUG '''


        self.ticks_passed += 1

        if self.ticks_passed >= 10:
            self.ticks_passed = 0
        
        

        