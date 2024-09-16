import queue
import packet
from autobahn.twisted.websocket import WebSocketServerProtocol

import utils
import premade
from player import Player

class ServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        super().__init__()
        self._packet_queue: queue.Queue[tuple['ServerProtocol', packet.Packet]] = queue.Queue()
        self._state: callable = self.LOGIN
        self._actor = None

   
            
    def PLAY(self, sender: 'ServerProtocol', p: packet.Packet):
        if p.action == packet.Action.Chat:  
            if sender == self:
                
                message = p.payloads[0]

                # commands
                try:
                    if message[0] == '/':
                        if 'additem' in message:
                            cmd, item_id, quantity = message.split()
                            self._actor.add_item(item_id, int(quantity))
                            return


                        if 'sethp' in message:
                            cmd, stat = message.split()
                            self._actor.stats['hp'] = int(stat)
                            return

                        if 'setmp' in message:
                            cmd, stat = message.split()
                            self._actor.stats['mp'] = int(stat)
                            return

                        
                except Exception as e:
                    pass
            

                message_sender  = self._actor.name
                p = packet.FlavouredMessagePacket(f'{message_sender} says: {message}')
                self.broadcast(p,exclude_self=True)
            
        
        if p.action == packet.Action.FlavouredMessage:
            self.send_client(p)

        if p.action == packet.Action.NpcInteraction:
            if sender == self:
                npc = p.payloads[0]
                interaction = p.payloads[1]
                room = self._actor.room

                if npc in room.npcs:
                    npc_response = room.npcs[npc].dialog(self._actor,interaction)
                    p = packet.NpcInteractionPacket(npc, npc_response)
                    self.onPacket(None, p)
            else:
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

        if p.action == packet.Action.Drop:
            if sender == self:
                self._actor.remove_item(p.payloads[0],p.payloads[1])

        if p.action == packet.Action.UseSkill:
            if sender == self:
                self._actor.use_skill(p.payloads[0])

        if p.action == packet.Action.UseItem:
            if sender == self:
                self._actor.use_item(p.payloads[0])
                
        if p.action == packet.Action.Room:
            if sender == self:
                self.send_client(p)

        if p.action == packet.Action.Go:
            if sender == self:
                self._actor.room.move_player(self._actor,p.payloads[0])

        if p.action == packet.Action.Target:
            if sender == self:
                if p.payloads[0] == '': 
                    target= self._actor.name
                else:
                    target = p.payloads[0]
                response = self._actor.set_target(target)
                p = packet.ChatPacket(response)
                self.onPacket(None,p)

        if p.action == packet.Action.Disconnect:
            if sender == self:
                self.send_client(p)     

        if p.action == packet.Action.ServerTime:
            if sender == self:
                self.send_client(p) 

        if p.action == packet.Action.Ok:
            if sender == self:
                self.send_client(p) 

        if p.action == packet.Action.Premade:
            if sender == self:
                self.send_client(p) 
        

    def new_player(self, name):
        room = self.factory.map.rooms['Town Square']
            
        self._actor = Player(self, name)
        room.add_player(self._actor)

        # add basic gear
        basic_items = '''
                basic_dagger
                potion0
                potion0
                potion1
                potion1
                potion0
                money
                money
                money
                money
                money
            '''.split()

        for i in basic_items:
            self._actor.add_item(i,1)
            self._actor.equip(i)
        
        self._actor.regen(hp=1000,mp=1000)


        #self.factory.database.save_player(self._actor)
        #self.factory.database.load_player(self._actor.name)
        return

    def LOGIN(self, sender: 'ServerProtocol', p: packet.Packet):
        if p.action == packet.Action.Register:
            
            self.send_client(packet.DenyPacket('Registered'))
            
            username = '@'+p.payloads[0]
            password = p.payloads[1]
            if self.factory.database.load_player(username) != None:
                self.send_client(packet.SystemMessagePacket('Register','Username Taken'))
                return
            
            self.factory.database.create_account(username,password)
            self.send_client(packet.SystemMessagePacket('Register','Registration succesful'))

        if p.action == packet.Action.Login:
            username = '@'+p.payloads[0]
            password = p.payloads[1]
            account = self.factory.database.get_account(username,password)

            if len(account) != 1:
                self.send_client(packet.SystemMessagePacket('Login','Login failed, Wrong username or password.'))
                return

            for client in self.factory.clients:
                if client._actor != None:
                    if client._actor.name == username:
                        self.send_client(packet.SystemMessagePacket('Login','Login failed, account already logged in.'))
                        return

            player = self.factory.database.load_player(username)
            self.new_player(username)

            if player == None:
                #print('player not found')
                self.factory.database.save_player(self._actor)
            else:
                #print('player found')
                self._actor.equipment = []
                self._actor.inventory = player['inventory']
                self._actor.stats = player['stats']
                self._actor.skills = []
                for e in player['equipment']:
                    self._actor.equip(e,forced = True) 

               

            self._state = self.PLAY

            small_premade = utils.dc(self.factory.premade)
            del small_premade['enemies']
            del small_premade['dialog']
            self.onPacket(self,packet.PremadePacket(small_premade))

            self.onPacket(self,packet.ServerTimePacket(self.factory.server_time))
            self.onPacket(self,packet.OkPacket())
            
            #p = packet.ChatPacket(f'{self._actor.name} Logged in')
            #self.broadcast(p,exclude_self=False)

       

    def tick(self):
        if self.factory.server_time % (30*100) == 0:
            self.send_client(packet.ServerTimePacket(self.factory.server_time))
            
        if not self._packet_queue.empty():
            s, p = self._packet_queue.get()
            self._state(s, p)
    
    def broadcast(self, p: packet.Packet, exclude_self: bool = True):
        for client in [self._actor.room.players[player_name].protocol for player_name in self._actor.room.players]:
            if client == self and exclude_self == True:
                continue
            if client._state != client.PLAY:
                continue

            client.onPacket(self,p)
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
            if self._actor != None:
                self.factory.database.save_player(self._actor)
                self._actor.logoff()
                
                #self._actor.room.remove_player(self._actor)

                
                
                


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


