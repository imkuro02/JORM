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

    def set_cooldown(self,skill_id,cooldown):
        self.skill_cooldowns[skill_id] = self.room.map.factory.server_time + cooldown

    def use_skill(self,skill_id):
        # CONDITIONS AND EARLY RETURNS
        if skill_id not in self.skills:
            self.broadcast('You do not know that skill', self)
            return

        if skill_id not in self.room.map.factory.premade['skills']:
            self.broadcast('Skill does not exist', self)
            return 
        
        skill = self.room.map.factory.premade['skills'][skill_id]

        if self.target.room != self.room:
            self.broadcast(f'{self.target.name} is not here', self)
            return 
        
        if skill_id in self.skill_cooldowns:
            self.broadcast(f'{skill["name"]} is on cooldown', self)
            return

        if skill['mp_cost'] > self.stats['mp']:
            self.broadcast(f'Not enough MP to use {skill["name"]}', self)
            return

        if skill['hp_cost'] > self.stats['mp']:
            self.broadcast(f'Not enough HP to use {skill["name"]}', self)
            return

        self.stats['mp'] -= skill['mp_cost']
        self.stats['hp'] -= skill['hp_cost']

        # CHECK FOR CRIT
        crit = random.randrange(0,100)
        crit = crit <= self.stats['crit_chance']
        # Print crit or not :p
        if crit:
            self.broadcast(f'{self.name} used {skill["name"]}, its Critical!')
        else:
            self.broadcast(f'{self.name} used {skill["name"]}')
       
        # add cooldown of 3 seconds for every skill unless skill is on cooldown
        for i in self.skills:
            if i in self.skill_cooldowns:
                continue
            self.skill_cooldowns[i] = self.room.map.factory.server_time + 3
        
        # bleh
        targetting_oppesite = self.target.tag != self.tag

        # use skill by id
        match skill_id:
            case 'slash':
                self.set_cooldown(skill_id,6)
                roll = random.randrange(1,self.stats['physic_damage'])
                if crit: 
                    roll = roll * 2
                self.target.take_physic_damage(roll,skill['name'])
                
            case 'stab':
                self.set_cooldown(skill_id,6)
                roll = random.randrange(1,self.stats['physic_damage'])
                if crit: 
                    roll = roll * 3
                self.target.take_physic_damage(roll,skill['name'])
    
            case 'firebolt':
                self.set_cooldown(skill_id,6)
                roll = random.randrange(1,self.stats['magic_damage'])
                if crit: 
                    roll = roll * 2
                self.target.take_magic_damage(roll,skill['name'])

            case 'spit':
                self.set_cooldown(skill_id,6)
                roll = random.randrange(1,self.stats['physic_damage'])
                if crit: 
                    roll = roll * 2
                self.target.take_magic_damage(roll,skill['name'])

            case 'scratch':
                self.set_cooldown(skill_id,6)
                roll = random.randrange(1,self.stats['physic_damage'])
                if crit: 
                    roll = roll * 3
                self.target.take_physic_damage(roll,skill['name'])

            case 'push':
                self.set_cooldown(skill_id,6)
                roll = random.randrange(1,self.stats['physic_damage'])
                if crit: 
                    roll = roll * 3
                self.broadcast(f'{self.target.name} lost {roll} MP!')
                self.target.drain_mp(mp = roll)


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

    def drain_mp(self, mp):
        self.stats['mp'] -= mp
        if self.stats['mp'] < 0: self.stats['mp'] = 0

        
        
        