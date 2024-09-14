
import packet
import enemy
import npc
import utils
import random
import yaml

class Room:
    def __init__(self, map, name: str, description: str):
        self.map = map
        self.name = name
        self.description = description
        self.exits = {}
        self.players = {}
        self.enemies = {}
        self.npcs = {}
        self.enemy_spawns = []
        self.ticks_passed = 0

    def connect_room(self,room):
        self.exits[room.name]=room

    def add_enemy_spawn(self, enemy_id: str, quantity: int, spawn_rate: int):
        self.enemy_spawns.append({'enemy_id': enemy_id, 'quantity': quantity, 'spawn_rate': spawn_rate})

    def add_enemy(self, enemy_id, name = None):

        # define a list of possible names for monsters to spawn as
        names = ''
        names += ' Alice Bob Charlie Diana Edward Fiona George Hannah Ian Julia Kevin Laura Mike Nancy Oliver Patricia Quinn Rachel Steve Tina Ursula'
        names += ' Geo Nuggy Sinclair Nigghtz Doey Shmoo Kuro Mana Redpot'
        names = names.split()
        
        # if no name was defined when function was called get a random name from the list
        if name == None:
            name = random.choice(names)
        
        enemies = self.map.factory.premade['enemies']
        

        enemy_type = enemies[enemy_id]
        name = f'{name} The {enemy_type["name"]}'

        if name in self.enemies:
            return

        _enemy = enemy.Enemy(   name = name, 
                                id = enemy_id, 
                                stats = enemy_type['stats'], 
                                skills = enemy_type['skills'], 
                                loot_table = enemy_type['loot_table'], 
                                room = self,
                                description = enemy_type['description']
                            )

        self.enemies[_enemy.name] = _enemy

        # set hp and mp to their maximum
        _enemy.stats['hp'] = _enemy.stats['max_hp']
        _enemy.stats['mp'] = _enemy.stats['max_mp']

        for _player in self.players:
            self.players[_player].room_update()
        _enemy.broadcast(f'{_enemy.name} appears!')

    def remove_enemy(self,e):
        #self.enemies[player.name].protocol.broadcast(p,exclude_self=True)
        del self.enemies[e.name]

    def add_player(self,player):
        self.players[player.name] = player
        player.room = self
        self.players[player.name].protocol.onPacket(self,packet.FlavouredMessagePacket(f'Arrived at {self.name}','new_room'))

        for _player in self.players:
            
            self.players[_player].room_update()

        #p = packet.FlavouredMessagePacket(f'{player.name} entered.')
        self.players[player.name].broadcast(f'{player.name} entered.', exclude_self = True)
        

    def remove_player(self,player):
        #p = packet.FlavouredMessagePacket(f'{player.name} left.')
        self.players[player.name].broadcast(f'{player.name} left.', exclude_self = True)
        
            
        del self.players[player.name]


    def move_player(self, player, new_room, forced = False):
        
        if new_room not in self.exits and not forced:
            return 'not a valid destination'

        '''
        followers = []
        for p in self.players:
            if self.players[p].target == self.players[p]:
                continue
            if self.players[p].target == player:
                followers.append(self.players[p])
        '''
        


        self.remove_player(player)
        self.map.rooms[new_room].add_player(player)
 

        '''
        for p in followers:
            self.move_player(p,new_room)
        '''

    def get_npcs(self):
        npcs = {}
        for i in self.npcs:
            npcs[i] = {
                'name': self.npcs[i].name
            } 
        return npcs

    def get_players(self):
        players = {}
        for i in self.players:
            players[i] = self.players[i].character_sheet(short = True)
        return players

    def get_enemies(self):
        enemies = {}
        for i in self.enemies:
            enemies[i] = self.enemies[i].character_sheet()
        return enemies
       
        
    def tick(self):
        self.ticks_passed += 1
        

        for spawn in self.enemy_spawns:
            exisisting_enemies = 0
            for e in self.enemies:
                if self.enemies[e].id == spawn['enemy_id']:
                    exisisting_enemies += 1
            if exisisting_enemies >= spawn['quantity']:
                continue
            if (self.map.factory.server_time/30) % spawn['spawn_rate'] == 0:
                self.add_enemy(spawn['enemy_id'])


        # create a temporary array of players since the original list will be changing if the player decides to move around
        player_names = []
        for p in self.players:
            player_names.append(p)

        enemy_names = []
        for p in self.enemies:
            enemy_names.append(p)
            
        for i in player_names:
            self.players[i].tick()

        for i in enemy_names:
            self.enemies[i].tick()
        


class Map:
    def __init__(self, factory):
        self.factory = factory
        self.rooms = {}

        smalltown =                 Room(self, 'Small Town',                 'Welcome to Small Town! its a.. well.. a small town, the Small Town Gate is just west of here, need to pass through the Small Town Ruins to get to it.')
        smalltown_ruins =           Room(self, 'Small Town Ruins',           'Small Town Ruins, Goblins are roaming the streets.')
        smalltown_gate =            Room(self, 'Small Town Gate',            'The gateway to Small Town, altho half the city is in ruins, this gate still stands somewhat tall.')
        forest_west_smalltown =     Room(self, 'Forest West Of Small Town',  'The forest, wilderness.. Watch out for Goblins and Hobgoblins!')
        forest_east_bigtown =       Room(self, 'Forest East Of Big Town',    'The forest, wilderness.. Watch out for Goblins and Hobgoblins!')
        bigtown_gate =              Room(self, 'Big Town Gate',              'The Big Town Gate, guarded by gamers... a path leads away into the Forest East Of Big Town')

        smalltown.connect_room(smalltown_ruins)
        smalltown_ruins.connect_room(smalltown)
        smalltown_ruins.connect_room(smalltown_gate)
        smalltown_gate.connect_room(smalltown_ruins)
        smalltown_gate.connect_room(forest_west_smalltown)
        forest_west_smalltown.connect_room(smalltown_gate)
        forest_west_smalltown.connect_room(forest_east_bigtown)
        forest_east_bigtown.connect_room(forest_west_smalltown)
        forest_east_bigtown.connect_room(bigtown_gate)
        bigtown_gate.connect_room(forest_east_bigtown)

        self.add_room(smalltown)
        self.add_room(smalltown_ruins)
        self.add_room(smalltown_gate)
        self.add_room(forest_west_smalltown)
        self.add_room(forest_east_bigtown)
        self.add_room(bigtown_gate)

        npc_jerry = npc.NPC('Jerry The Oimer',smalltown,'jerry')

        smalltown_ruins.add_enemy_spawn('goblin',3,15)

        smalltown_gate.add_enemy_spawn('goblin',1,15)

        forest_west_smalltown.add_enemy_spawn('goblin',3,15)
        forest_west_smalltown.add_enemy_spawn('hobgoblin',1,15)


        forest_east_bigtown.add_enemy_spawn('hobgoblin',3,15)
        forest_east_bigtown.add_enemy_spawn('goblin_shaman',2,40)

        forest_east_bigtown.add_enemy_spawn('gamer',2,40)


    def add_room(self,room):
        self.rooms[room.name] = room

    

if __name__ == '__main__':

    world = Map()

    r = world.rooms

    print(r)
    for i in r:
        print(r[i].name,r[i].exits)
    