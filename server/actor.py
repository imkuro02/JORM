import random
import packet

class Actor:

    def character_stats(self):
        return {
            'name': self.name,
            'stats': self.stats
        }

    def broadcast(self,p):
        #p: packet = packet.ChatPacket(text,None)
        for player in self.room.players:
            self.room.players[player].protocol.onPacket(None,p)

    def use_skill(self,skill_id):
        if skill_id not in self.skills:
            return
        if skill_id not in self.room.map.factory.premade['skills']:
            #self.broadcast('skill does not exist')
            return 
        
        skill = self.room.map.factory.premade['skills'][skill_id]

        if self.target.room != self.room:
            #self.broadcast('Target is not here')
            return 
        
        #self.broadcast(f'{self.name} Used {skill["name"]}.')

        p: packet = packet.FlavouredMessagePacket(f'{self.name} used {skill["name"]}')
        self.broadcast(p)

        targetting_oppesite = self.target.tag != self.tag
        if skill_id == 'slash':
            roll = random.randrange(1,self.stats['physic_damage'])
            self.target.take_physic_damage(roll,skill['name'])
            
        if skill_id == 'stab':
            roll = random.randrange(1,round(self.stats['physic_damage']/2)) + self.target.stats['physic_block']
            self.target.take_physic_damage(roll,skill['name'])
           
    def regen(self, hp = 0, mp = 0):
        if hp < 0: hp = 0
        if mp < 0: mp = 0
        
        self.stats['hp'] += hp
        if self.stats['hp'] > self.stats['max_hp']:
            self.stats['hp'] = self.stats['max_hp']

        self.stats['mp'] += mp
        if self.stats['mp'] > self.stats['max_mp']:
            self.stats['mp'] = self.stats['max_mp']

    def take_physic_damage(self, dmg, skill = None):

        dmg -= self.stats['physic_block']

        if dmg <= 0:
            dmg = 0    

        self.stats['hp'] -= dmg

        

        p: packet = packet.FlavouredMessagePacket(f'{self.name} took {dmg} damage from {skill}.')
        for player in self.room.players:
            self.room.players[player].protocol.onPacket(None,p)

        
        
        