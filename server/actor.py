import random
import packet

class Actor:

    def character_stats(self):
        return {
            'name': self.name,
            'stats': self.stats
        }

    def use_skill(self,skill_id):
        if skill_id not in self.room.map.factory.premade['skills']:
            return 'skill does not exist'
        
        skill = self.room.map.factory.premade['skills'][skill_id]

        if self.target.room != self.room:
            return 'Target is not here'

        if skill_id == 'slash':
            roll = random.randrange(1,self.stats['physic_damage'])
            damage_dealt = self.target.take_physic_damage(roll,skill)
            damage_dealt = self.target.take_physic_damage(roll,skill)
            damage_dealt = self.target.take_physic_damage(roll,skill)
            
        return f'{self.name} Used {skill["name"]}.'
            

    def regen(self, hp = 0, mp = 0):
        if hp < 0: hp = 0
        if mp < 0: mp = 0
        
        self.stats['hp'] += hp
        if self.stats['hp'] > self.stats['max_hp']:
            self.stats['hp'] = self.stats['max_hp']

        self.stats['mp'] += mp
        if self.stats['mp'] > self.stats['max_mp']:
            self.stats['mp'] = self.stats['max_mp']

    def take_physic_damage(self, roll, skill = None):

        roll -= self.stats['physic_block']
        self.stats['hp'] -= roll

        if skill == None:
            text = f'{self.name} Takes {roll} Damage.'
        else:
            if roll <= 0:
                text = f'{self.name} Blocked {skill["name"]}.'
            else:
                text = f'{self.name} Takes {roll} Damage from {skill["name"]}.'

        p: packet = packet.ChatPacket(text,None)
        for player in self.room.players:
            self.room.players[player].protocol.onPacket(None,p)

        
        
        