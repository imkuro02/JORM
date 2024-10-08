import sys
import protocol
from twisted.python import log
from twisted.internet import reactor, task, ssl
from autobahn.twisted.websocket import WebSocketServerFactory
import time
import premade
import world
import database
from use_manager import UseManager

import threading
import time

class Factory(WebSocketServerFactory):
    def __init__(self, hostname: str, port: int):
        self.protocol = protocol.ServerProtocol
        super().__init__(f"wss://{hostname}:{port}")
        self.clients: set[protocol.ServerProtocol] = set()
        self._last_delta_time_checked = time.time()
        self.tickrate: int = 30
        self.server_time = 0
        self.premade = premade.get_premade()
        self.map = world.Map(self)
        self.use_manager = UseManager(self)
        self.database = database.DataBase()

        tickloop = task.LoopingCall(self.tick)
        tickloop.start(1 / self.tickrate)

    def tick(self):
        self.server_time += 1
        #print(self.server_time)
        for r in self.map.rooms:
            self.map.rooms[r].tick()

        
        for p in self.clients:
            p.tick()

    def remove_protocol(self, p: protocol.ServerProtocol):   
        self.clients.remove(p)

    # Override
    def buildProtocol(self,addr):
        p = super().buildProtocol(addr)
        self.clients.add(p)
        return p 

    def handle_user_input(self):
        while True:
            cmd = input('>')
            print(cmd)
            if cmd == 'stop':
                for p in self.clients:
                    p._closeConnection()
                time.sleep(2)
                reactor.stop()
        
if __name__ == '__main__':

    log.startLogging(sys.stdout)

    PORT: int = 8081
    IP: str = '0.0.0.0'
    SSL: bool = True

    # SSL context creation (use your SSL certificate and private key)
    ssl_context = ssl.DefaultOpenSSLContextFactory('./server.key', './server.crt')
    factory = Factory(IP, PORT)

    if SSL:
        reactor.listenSSL(PORT, factory, ssl_context)
    else:
        reactor.listenTCP(PORT, factory)

    input_thread = threading.Thread(target=factory.handle_user_input)
    input_thread.daemon = True  # Daemonize the thread so it exits when the main program exits
    input_thread.start()

    reactor.run()
    



    
        
