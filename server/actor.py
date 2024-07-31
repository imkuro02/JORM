import random
import packet

class Actor:

    def character_stats(self):
        return {
            'name': self.name,
            'stats': self.stats
        }

    def broadcast(self, text, specific_player = None):
        p: packet = packet.FlavouredMessagePacket(text)
        for player in self.room.players:
            if specific_player == None:
                self.room.players[player].protocol.onPacket(None,p)
            else:
                if specific_player == self.room.players[player]:
                    self.room.players[player].protocol.onPacket(None,p)


    def tick(self):
        cooldowns_finished = []
        for i in self.skill_cooldowns:
            if self.skill_cooldowns[i] <= self.room.map.factory.server_time:
                cooldowns_finished.append(i)

        for i in cooldowns_finished:
            del self.skill_cooldowns[i]

    def use_skill(self,skill_id):
        if skill_id not in self.skills:
            self.broadcast('You do not know that skill', self)
            return

        if skill_id not in self.room.map.factory.premade['skills']:
            self.broadcast('Skill does not exist', self)
            return 
        
        skill = self.room.map.factory.premade['skills'][skill_id]

        if self.target.room != self.room:
            self.broadcast('Target is not here', self)
            return 
        
        if skill_id in self.skill_cooldowns:
            self.broadcast('Skill is on cooldown', self)
            return

        crit = random.randrange(0,100)
        crit = crit <= self.stats['crit_chance']
        if crit:
            
            self.broadcast(f'{self.name} used {skill["name"]}, its Critical!')
        else:
            self.broadcast(f'{self.name} used {skill["name"]}')
       
        
        for i in self.skills:
            self.skill_cooldowns[i] = self.room.map.factory.server_time + 3
        self.skill_cooldowns[skill_id] = self.room.map.factory.server_time + 6

        targetting_oppesite = self.target.tag != self.tag
        match skill_id:
            case 'slash':
                roll = random.randrange(1,self.stats['physic_damage'])
                if crit: 
                    roll = roll * 2
                self.target.take_physic_damage(roll,skill['name'])
                
            case 'stab':
                roll = random.randrange(1,self.stats['physic_damage'])
                if crit: 
                    roll = roll * 3
                self.target.take_physic_damage(roll,skill['name'])

            case 'firebolt':
                roll = random.randrange(1,self.stats['magic_damage'])
                if crit: 
                    roll = roll * 2
                    self.take_magic_damage(roll,skill['name'])
                self.target.take_magic_damage(roll,skill['name'])


            
            
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

        p: packet = packet.FlavouredMessagePacket(f'{self.name} took {dmg} damage from {skill}')
        for player in self.room.players:
            self.room.players[player].protocol.onPacket(None,p)


        if self.stats['hp'] <= 0:
            self.die()

    def take_magic_damage(self, dmg, skill = None):
        dmg -= self.stats['magic_block']

        if dmg <= 0:
            dmg = 0    

        self.stats['hp'] -= dmg

        p: packet = packet.FlavouredMessagePacket(f'{self.name} took {dmg} magic damage from {skill}')
        for player in self.room.players:
            self.room.players[player].protocol.onPacket(None,p)

        if self.stats['hp'] <= 0:
            self.die()

        
        
        