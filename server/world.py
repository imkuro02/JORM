
import packet

class Room:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.exits = {}
        self.players = {}

    def connect_room(self,room):
        self.exits[room.name]=room

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

        self.remove_player(player)
        self.exits[new_room].add_player(player)
       
        
    def tick(self):
        # create a temporary array of players since the original list will be changing if the player decides to move around
        player_names = []
        for p in self.players:
            player_names.append(p)
            
        for i in player_names:
            self.players[i].tick()
        


class Map:
    def __init__(self):
        self.rooms = {}

        village = Room('village',   'starter Village')
        forest  = Room('forest',    'You find yourself in a dark forest, something something ~scenery~ and such, lots of cool thins, very awasome')
        sewers  = Room('sewers',    'village sewers')

        village.connect_room(forest)
        village.connect_room(sewers)
        sewers.connect_room(village)
        forest.connect_room(village)

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
    