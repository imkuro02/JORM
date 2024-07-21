import queue
import packet
from autobahn.twisted.websocket import WebSocketServerProtocol

import utils
import premade
from actor import Actor

class ServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        super().__init__()
        self._packet_queue: queue.Queue[tuple['ServerProtocol', packet.Packet]] = queue.Queue()
        self._state: callable = self.LOGIN
        self._actor = None

    def COMBAT(self, sender: 'ServerProtocol', p: packet.Packet):
        if p.action == packet.Action.Combat:
            self.send_client(p)
            
    def PLAY(self, sender: 'ServerProtocol', p: packet.Packet):
        if p.action == packet.Action.Chat:  
            if sender == self:
                message         = p.payloads[0]
                message_sender  = self._actor.name
                p = packet.ChatPacket(message,message_sender)
                self.broadcast(p,exclude_self=False)
        
        if p.action == packet.Action.Premade:
            if sender == self:
                self.send_client(p)

        if p.action == packet.Action.CharacterSheet:
            if sender == self:
                self.send_client(p)

        if p.action == packet.Action.Equip:
            if sender == self:
                self._actor.equip(p.payloads[0])

        if p.action == packet.Action.Unequip:
            if sender == self:
                self._actor.unequip(p.payloads[0])

        if p.action == packet.Action.Room:
            if sender == self:
                self.send_client(p)

        if p.action == packet.Action.Go:
            if sender == self:
                self._actor.room.move_player(self._actor,p.payloads[0])

        if p.action == packet.Action.Disconnect:
            if sender == self:
                self.send_client(p)


    def LOGIN(self, sender: 'ServerProtocol', p: packet.Packet):
        if p.action == packet.Action.Register:
            self.send_client(packet.DenyPacket('Registered'))

        if p.action == packet.Action.Login:
            self.send_client(packet.OkPacket())
            self._state = self.PLAY

            self.onPacket(self,packet.PremadePacket(self.factory.premade))

            name = p.payloads[0]
            stats = utils.dc(premade.PLAYER_STATS)
            inventory = {}
            equipment = []

            room = self.factory.map.rooms['village']
            
            self._actor = Actor(self, name, stats, equipment, inventory, None)
            room.add_player(self._actor)

            self._actor.add_item('coins',42069)
            self._actor.add_item('potion0',1)
            self._actor.add_item('katana',1)
            self._actor.add_item('sword0',1)
            self._actor.add_item('sword0',1)
            self._actor.add_item('helmet0',1)
            self._actor.add_item('rock',11)

            print(self._actor.equip('sword0'))
            print(self._actor.unequip('sword0'))
            print(self._actor.equip('sword0'))
   
          

            #print(self._actor.stats)

            

            #p = packet.ChatPacket(f'{self._actor.name} Logged in')
            #self.broadcast(p,exclude_self=False)

    def tick(self):
        if not self._packet_queue.empty():
            s, p = self._packet_queue.get()
            self._state(s, p)
    
    def broadcast(self, p: packet.Packet, exclude_self: bool = True):
        for client in [self._actor.room.players[player_name].protocol for player_name in self._actor.room.players]:
            if client == self and exclude_self == True:
                continue
            if client._state != client.PLAY:
                continue

            client.send_client(p)
        return

    def onPacket(self, sender: 'ServerProtocol', p: packet.Packet):
        self._packet_queue.put((sender, p))

    # Override
    def onConnect(self, request):
        print('Client connecting: ', request.peer)

    # Override
    def onOpen(self):
        print('Websocket connection open')
        self._state = self.LOGIN 

    # Override
    def onClose(self, wasClean, code, reason):
        if self._state == self.PLAY:
            #p = packet.ChatPacket(f'{self._actor.name} Disconnected')
            #self.broadcast(p,exclude_self=True)

            self._actor.room.remove_player(self._actor)

        self.factory.remove_protocol(self)
        print('Websocket connection closed ', 'unexpectedly' if not wasClean else 'cleanly', ' with code ', code,':', reason) 

    # Override
    def onMessage(self, payload, isBinary):
        #print(payload)
        try:
            decoded_payload = payload.decode('utf-8')

            p: packet.Packet = packet.from_json(decoded_payload)
            if p != None:
                self.onPacket(self, p)
        except Exception as e:
            print(f'Could not load message as packet: {e}. Message was: {payload.decode("utf8")}')

    def send_client(self, p: packet.Packet):
        b = bytes(p)
        try:
            self.sendMessage(b)
        except Exception as e:
            print(e)


