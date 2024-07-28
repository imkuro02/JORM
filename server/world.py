
import packet
import premade
from enemy import Enemy
import utils

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

    def add_enemy(self,enemy):
        self.enemies[enemy.name] = enemy
        enemy.room = self

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

        name = 'Josh The Skeleton'
        stats = utils.dc(premade.ENEMY_STATS)
        enemy0 = Enemy(name, stats)
        forest.add_enemy(utils.dc(enemy0))

        name = 'Jake The Slime'
        stats = utils.dc(premade.ENEMY_STATS)
        enemy1 = Enemy(name, stats)


        forest.add_enemy(utils.dc(enemy0))
        forest.add_enemy(utils.dc(enemy1))

     

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
    