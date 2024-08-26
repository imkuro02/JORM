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

        if self.target != None:
            if self.target.room != self.room:
                if self.target.name in self.room.players:
                    self.target = self.room.players[self.target.name]
                if self.target.name in self.room.enemies:
                    self.target = self.room.enemies[self.target.name]

        statuses_to_remove = []
        for status in self.status_effects:
            self.status_effects[status] -= 1
            if self.status_effects[status] <= 0:
                statuses_to_remove.append(status)

        for status in statuses_to_remove:
            del self.status_effects[status]

    def set_cooldown(self,skill_id,cooldown):
        cooldown = cooldown * self.room.map.factory.tickrate
        self.skill_cooldowns[skill_id] = self.room.map.factory.server_time + cooldown

    def has_status_effect(self, status_effect_id):
        status = self.room.map.factory.premade['statuses'][status_effect_id]
        if 'potion_sickness' in self.status_effects:
            self.broadcast(f'You have {status["name"]} for {int(self.status_effects[status_effect_id]/30)} seconds.',self)
            return True
        return False

    def use_item(self,item_id):
        if item_id not in self.room.map.factory.premade['items']:
            self.broadcast('That item does not exist', self)
            return

        item = self.room.map.factory.premade['items'][item_id]

        if item_id not in self.inventory:
            self.broadcast(f'You don\'t have {item["name"]}')

        
       

        match item['use_script']:
            case 'restore_hp_10':
                if self.has_status_effect('potion_sickness'): 
                    return
                self.regen(hp=10)
                self.status_effects['potion_sickness'] = 60*10
            case 'restore_mp_10':
                if self.has_status_effect('potion_sickness'): 
                    return
                self.regen(mp=10)
                self.status_effects['potion_sickness'] = 60*10


        self.broadcast(f'{self.name} used {item["name"]}')
        self.remove_item(item_id,1)

    def use_skill(self,skill_id):
        # CONDITIONS AND EARLY RETURNS
        if skill_id not in self.skills:
            self.broadcast('You do not know that skill', self)
            return

        if skill_id not in self.room.map.factory.premade['skills']:
            self.broadcast('Skill does not exist', self)
            return 
        
        skill = self.room.map.factory.premade['skills'][skill_id]

        # check if skill needs a target
        if skill['target'] != 'none':
            if self.target == None:
                self.broadcast(f'You are not targetting anyone', self)
                return 

            
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
       
        # add cooldown of 6 seconds for every skill unless skill is on cooldown
        for i in self.skills:
            if i in self.skill_cooldowns:
                continue
            self.set_cooldown(i,6)


        match skill_id:
            case 'stab':
                self.set_cooldown(skill_id,9)
                roll = self.stats['agi'] 
                if crit: 
                    roll = roll * 3
                else:
                    roll = int(roll/2)
                self.target.take_damage(roll,'agi',self,skill['name'])
            case 'slash':
                self.set_cooldown(skill_id,9)
                roll = self.stats['str'] 
                if crit: 
                    roll = roll * 2
                self.target.take_damage(roll,'str',self,skill['name'])
            case 'spit':
                self.set_cooldown(skill_id,9)
                roll = self.stats['str'] 
                if crit: 
                    roll = roll * 2
                self.target.take_damage(roll,'agi',self,skill['name'])
            case 'firebolt':
                self.set_cooldown(skill_id,9)
                roll = self.stats['str'] 
                if crit: 
                    roll = roll * 2
                    self.target.take_damage(roll,'int',self,skill['name'])
                self.target.take_damage(roll,'int',self,skill['name'])
            case 'push':
                self.set_cooldown(skill_id,9)
                roll = self.stats['str'] 
                if roll <= 0: roll = 1
                if crit: 
                    roll = roll * 2
                self.broadcast(f'{self.target.name} lost {int(roll)} MP!')
                self.target.drain_mp(mp = roll)
            case 'guard':
                self.set_cooldown(skill_id,20)
                self.regen(hp=10+self.stats['str'],mp=0)
                self.broadcast(f'GRRRR!')
        return

    def regen(self, hp = 0, mp = 0):
        if hp < 0: hp = 0
        if mp < 0: mp = 0
        
        self.stats['hp'] += hp
        if self.stats['hp'] > self.stats['max_hp']:
            self.stats['hp'] = self.stats['max_hp']

        self.stats['mp'] += mp
        if self.stats['mp'] > self.stats['max_mp']:
            self.stats['mp'] = self.stats['max_mp']

    def dodge_check(self):
        roll = random.randrange(1,100)
        return bool(roll <= self.stats['dodge_chance'])



    def take_damage(self, damage, stat, source, skill = None):
        if self.dodge_check():
            self.broadcast(f'{self.name} dodged {skill}')
            return

        match stat:
            case 'str': damage += ( -self.stats['agi'] + self.stats['int'])
        match stat:
            case 'agi': damage += ( -self.stats['int'] + self.stats['str'])
        match stat:
            case 'int': damage += ( -self.stats['str'] + self.stats['agi'])

        damage = int(damage)

        if damage <= 0:
            if skill != None:
                self.broadcast(f'{self.name} blocked damage from {skill}')
            else:
                self.broadcast(f'{self.name} blocked damage')
            return

        if skill != None:
            self.broadcast(f'{self.name} took damage {damage} from {skill}')
        else:
            self.broadcast(f'{self.name} took damage {damage} ')

        self.stats['hp'] -= damage
        if self.stats['hp'] <= 0:
            self.die()

    def drain_mp(self, mp):
        self.stats['mp'] -= mp
        if self.stats['mp'] < 0: self.stats['mp'] = 0

        
        
        