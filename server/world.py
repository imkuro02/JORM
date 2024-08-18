
import packet
import enemy
import utils
import random

class Room:
    def __init__(self, map, name: str, description: str):
        self.map = map
        self.name = name
        self.description = description
        self.exits = {}
        self.players = {}
        self.enemies = {}
        self.enemy_spawns = []
        self.ticks_passed = 0

    def connect_room(self,room):
        self.exits[room.name]=room

    def add_enemy_spawn(self, enemy_id: str, quantity: int, spawn_rate: int):
        self.enemy_spawns.append({'enemy_id': enemy_id, 'quantity': quantity, 'spawn_rate': spawn_rate})

    def add_enemy(self, enemy_id, name = None):
        retry = True
        retries = 0
        while retry:
            # define a list of possible names for monsters to spawn as
            names = ''
            names += ' Alice Bob Charlie Diana Edward Fiona George Hannah Ian Julia Kevin Laura Mike Nancy Oliver Patricia Quinn Rachel Steve Tina Ursula'
            names += ' Geo Nuggy Sinclair Nigghtz Doey Shmoo Kuro Mana Redpot'
            names = names.split()
            
            # if no name was defined when function was called get a random name from the list
            if name == None:
                name = random.choice(names)
            
            _enemy = enemy.Enemy(name)
            _enemy.id = enemy_id

            # add name prefix and customize stats
            match enemy_id:
                case 'skeleton':
                    _enemy.name += ' The Skeleton'
                    _enemy.skills = ['slash','guard']
                    _enemy.stats['max_hp'] = 10
                    _enemy.loot_table = [
                        enemy.Loot(item_index = 'money', drop_chance = .5, quantity_min = 10, quantity_max = 20),
                        enemy.Loot(item_index = 'rock', drop_chance = .25, quantity_min = 1, quantity_max = 3)
                    ]
                case 'slime':
                    _enemy.name += ' The Slime'
                    _enemy.skills = ['spit','push']
                    _enemy.stats['max_hp'] = 15
                    _enemy.stats['magic_damage'] = 10
                    _enemy.stats['physic_damage'] = 10
                    _enemy.loot_table = [
                        enemy.Loot(item_index = 'money', drop_chance = 1, quantity_min = 1, quantity_max = 10)
                    ]
                case 'gamer':
                    _enemy.name += ' The Gamer'
                    _enemy.skills = ['spit','push']
                    _enemy.roaming_text = ['farts violently',' calls you a "!@#$%^&*" ']
                    _enemy.stats['max_hp'] = 20
                    _enemy.stats['physic_block'] = 10
                    _enemy.stats['magic_block'] = 10
                    _enemy.loot_table = [
                        enemy.Loot(item_index = 'rock', drop_chance = 1, quantity_min = 1, quantity_max = 10),
                        enemy.Loot(item_index = 'gamer_katana', drop_chance = .1, quantity_min = 1, quantity_max = 10)
                    ]
            
            # if name is not already taken do not retry and the initialization and continue
            if name not in self.enemies:
                retry = False
            # otherwise, set name to None so it can get randomized again
            else:
                name = None

            # if this has repeated for more 10 or more times simply stop trying and dont spawn the enemy
            retries += 1
            if retries >= 10:
                return

        # set hp and mp to their maximum
        _enemy.stats['hp'] = _enemy.stats['max_hp']
        _enemy.stats['mp'] = _enemy.stats['max_mp']

        # ad the enemy to self.enemies and set the room for the enemy
        self.enemies[_enemy.name] = _enemy
        _enemy.room = self
        for _player in self.players:
            self.players[_player].room_update()
        _enemy.broadcast(f'{_enemy.name} appears!')

    def remove_enemy(self,e):
        #self.enemies[player.name].protocol.broadcast(p,exclude_self=True)
        del self.enemies[e.name]

    def add_player(self,player):
        self.players[player.name] = player
        player.room = self

        for _player in self.players:
            self.players[_player].room_update()

        p = packet.FlavouredMessagePacket(f'{player.name} entered.')
        self.players[player.name].protocol.broadcast(p,exclude_self=True)

    def remove_player(self,player):
        p = packet.FlavouredMessagePacket(f'{player.name} left.')
        self.players[player.name].protocol.broadcast(p,exclude_self=True)
        
            
        del self.players[player.name]

    def move_player(self,player,new_room):
        
        if new_room not in self.exits:
            return 'not a valid destination'

        followers = []
        for p in self.players:
            if self.players[p].target == self.players[p]:
                continue
            if self.players[p].target == player:
                followers.append(self.players[p])

        


        self.remove_player(player)
        self.exits[new_room].add_player(player)

        for p in followers:
            self.move_player(p,new_room)

    
    def get_players(self):
        players = {}
        for i in self.players:
            players[i] = self.players[i].character_stats()
        return players

    def get_enemies(self):
        enemies = {}
        for i in self.enemies:
            enemies[i] = self.enemies[i].character_stats()
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
        smalltown_ruins =           Room(self, 'Small Town Ruins',           'Small Town Ruins, some Slimes seek refuge here, you can see Small Town Gate from here.')
        smalltown_gate =            Room(self, 'Small Town Gate',            'The gateway to Small Town, need to pass through the Small Town Ruins first though. There is a path leading to the Forest West Of Small Town')
        forest_west_smalltown =     Room(self, 'Forest West Of Small Town',  'The forest, wilderness.. A path leads deeper into the Forest East Of Big Town, and another path leading straight to Small Town Gate.')
        forest_east_bigtown =       Room(self, 'Forest East Of Big Town',    'the forest, wilderness.. A path leads deeper into the Forest West Of Small Town, and another path leading straight to Big Town Gate')
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

        village = Room(self, 'Village',   'The Village, you see a path leading to the Forest. and a gate to the Sewers.')
        forest  = Room(self, 'Forest',    'You find yourself deep in the Forest, there is a path leading to the Village here')
        sewers  = Room(self, 'Sewers',    'Stinky stinky sewers, theres only one way; UP.. to the Village ')
    
        
        village.connect_room(forest)
        village.connect_room(sewers)
        sewers.connect_room(village)
        forest.connect_room(village)

        forest.add_enemy_spawn('skeleton',6,10)
        sewers.add_enemy_spawn('slime',3,15)
        sewers.add_enemy_spawn('gamer',1,60)

        smalltown_ruins.add_enemy_spawn('slime',3,15)
        smalltown_ruins.add_enemy_spawn('skeleton',1,60)
        forest_west_smalltown.add_enemy_spawn('slime',5,16)
        forest_east_bigtown.add_enemy_spawn('gamer',1,15)
        bigtown_gate.add_enemy_spawn('gamer',3,15)


        '''
        forest.add_enemy('skeleton')
        forest.add_enemy('slime')
        '''



     

        self.add_room(village)
        self.add_room(forest)
        self.add_room(sewers)

    def add_room(self,room):
        self.rooms[room.name] = room

    

if __name__ == '__main__':

    world = Map()

    r = world.rooms

    print(r)
    for i in r:
        print(r[i].name,r[i].exits)
    