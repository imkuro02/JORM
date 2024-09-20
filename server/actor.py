import random
import packet

class Actor:
    def character_stats(self):
        return {
            'name': self.name,
            'stats': self.stats
        }

    def broadcast(self, text, specific_player = None, exclude_self = False, anim = None):
        p: packet = packet.FlavouredMessagePacket(text,anim)
        for player in self.room.players:
            if exclude_self and self.room.players[player] == self:
                continue
            if specific_player == None:
                self.room.players[player].protocol.onPacket(None,p)
            else:
                if specific_player == self.room.players[player]:
                    self.room.players[player].protocol.onPacket(None,p)

    def die(self):
        self.respawn_at = self.room.map.factory.server_time + (30*10) 
        self.dead = True

    def tick(self):

        if self.room == None:
            return

        if self.dead and self.room.map.factory.server_time >= self.respawn_at:
            self.respawn()

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
        self.room.map.factory.combat_manager.use_item(self,item_id)

    def use_skill(self,skill_id):
        self.room.map.factory.combat_manager.use_skill(self,skill_id)

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
            case 'str': 
                damage -= int(self.stats['int']/2) 
            case 'agi': 
                damage -= int(self.stats['str']/2) 
            case 'int': 
                damage -= int(self.stats['agi']/2) 

        damage = int(damage)

        if damage <= 0:
            if skill != None:
                self.broadcast(f'{self.name} blocked damage from {skill}')
            else:
                self.broadcast(f'{self.name} blocked damage')
            return

        if skill != None:
            self.broadcast(f'{self.name} took {damage} damage from {skill}')
        else:
            self.broadcast(f'{self.name} took {damage} damage')

        self.stats['hp'] -= damage
        if self.stats['hp'] <= 0:
            self.die()

    def drain_mp(self, mp):
        self.stats['mp'] -= mp
        if self.stats['mp'] < 0: self.stats['mp'] = 0

        
        
        