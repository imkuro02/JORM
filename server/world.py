
import packet
import premade
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

    def connect_room(self,room):
        self.exits[room.name]=room

    def add_enemy(self, enemy_id, name = None):
        retry = True
        stats = utils.dc(premade.ENEMY_STATS)
        retries = 0
        while retry:
            # define a list of possible names for monsters to spawn as
            names = 'Geo Nuggy Sinclair Nigghtz Doey Shmoo Kuro Mana Redpot'
            names = names.split()
            
            # if no name was defined when function was called get a random name from the list
            if name == None:
                name = random.choice(names)
            
            # add name prefix and customize stats
            match enemy_id:
                case 'skeleton':
                    name += ' The Skeleton'
                    skills = ['slash','guard']
                case 'slime':
                    name += ' The Slime'
                    skills = ['spit','push']
                    stats['max_hp'] = 20
                    stats['magic_damage'] = 10
                    stats['physic_damage'] = 10

            
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
        stats['hp'] = stats['max_hp']
        stats['mp'] = stats['max_mp']
                
        # create copy of this enemy
        e = utils.dc(enemy.Enemy(name,stats,skills))

        # ad the enemy to self.enemies and set the room for the enemy
        self.enemies[e.name] = e
        e.room = self

    def remove_enemy(self,e):
        #self.enemies[player.name].protocol.broadcast(p,exclude_self=True)
        del self.enemies[e.name]

    def add_player(self,player):
        self.players[player.name] = player
        player.room = self

        p = packet.ChatPacket(f'{player.name} entered.')
        self.players[player.name].protocol.broadcast(p,exclude_self=True)

    def remove_player(self,player):
        p = packet.ChatPacket(f'{player.name} left.')
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

        village = Room(self, 'Village',   'The Village, you see a path leading to the Forest, and a kømlokk or smth leading to the Sewers below.')
        forest  = Room(self, 'Forest',    'You find yourself deep in the Forest, there is a path leading to the Village here.')
        sewers  = Room(self, 'Sewers',    'Stinky stinky sewers, theres only one way; UP.. to the Village.')

        village.connect_room(forest)
        village.connect_room(sewers)
        sewers.connect_room(village)
        forest.connect_room(village)

        forest.add_enemy('skeleton')
        forest.add_enemy('skeleton')
        forest.add_enemy('slime')
        forest.add_enemy('slime')
        forest.add_enemy('skeleton')


     

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
    