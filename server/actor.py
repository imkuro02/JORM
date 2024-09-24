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
        for i in self.status_effects:
            self.status_effects[i] = 0


    def cooldown_tick(self):
        cooldowns_finished = []
        for i in self.skill_cooldowns:
            if self.skill_cooldowns[i] <= self.room.map.factory.server_time:
                cooldowns_finished.append(i)

        for i in cooldowns_finished:
            del self.skill_cooldowns[i]
        
    def remove_status_effect(self,status_effect):
        if status_effect not in self.status_effects:
            print(f'ERROR {self.name} tried to remove_stats_effect on status effect: {status_effect} without having it.')
            return

        status_name = self.room.map.factory.premade['statuses'][status_effect]['name']
        if self.dead == False: 
            self.broadcast(f'You are no longer afflicted with {status_name}.', self)

        del self.status_effects[status_effect]

        # when status effect is removed
        match status_effect:
            case 'dancing':
                self.stats['str'] += 10
                self.stats['agi'] -= 10
                self.stats['dodge_chance'] += 100

    def set_status_effect(self, status_effect, amount, broadcast_to = None):
        amount = amount * self.room.map.factory.tickrate

        if status_effect in self.status_effects:
            self.status_effects[status_effect] += amount
        else:
            self.status_effects[status_effect] = amount

            status_name = self.room.map.factory.premade['statuses'][status_effect]['name']
            self.broadcast(f'{self.name} is afflicted with {status_name}.', broadcast_to)
            
            # when status effect is first applied
            match status_effect:
                case 'dancing':
                    self.stats['str'] -= 10
                    self.stats['agi'] += 10
                    self.stats['dodge_chance'] -= 100
                    lines = [f'shuffles their feet.', f'busts it down sexual style.', f'is quirking it up in the club!']
                    line = random.choice(lines)
                    self.broadcast(f'{self.name} {line}')

    def status_effects_tick(self):
        statuses_to_remove = []
        for status in self.status_effects:
            self.status_effects[status] -= 1
            if self.status_effects[status] <= 0:
                statuses_to_remove.append(status)

        for status in statuses_to_remove:
            self.remove_status_effect(status)

        if self.room.map.factory.server_time % 30 == 0:
            for status_effect in self.status_effects:
                status_name = self.room.map.factory.premade['statuses'][status_effect]['name']
                #  when status effect ticks once a second
                match status_effect:
                    case 'burning':
                        #self.broadcast('You are Burning!',self)
                        self.take_damage(damage = 1, damage_type = status_effect, damage_source = status_name, silent = True, can_dodge = False)
                    
                        


    def tick(self):

        if self.room == None:
            return

        if self.dead and self.room.map.factory.server_time >= self.respawn_at:
            self.respawn()

        self.cooldown_tick()
        self.status_effects_tick()

        if self.target != None:
            if self.target.room != self.room:
                if self.target.name in self.room.players:
                    self.target = self.room.players[self.target.name]
                if self.target.name in self.room.enemies:
                    self.target = self.room.enemies[self.target.name]

        # clamp
        if self.stats['hp'] > self.stats['max_hp']: self.stats['hp'] = self.stats['max_hp'] 
        if self.stats['mp'] > self.stats['max_mp']: self.stats['mp'] = self.stats['max_mp'] 

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
        self.room.map.factory.use_manager.use_item(self,item_id)

    def use_skill(self,skill_id):
        self.room.map.factory.use_manager.use_skill(self,skill_id)

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

    def crit_check(self):
        roll = random.randrange(1,100)
        return bool(roll <= self.stats['crit_chance'])

    def take_damage(self, damage = 0, damage_type = None, actor_source = None, damage_source = None, silent = False, can_dodge = True):
        if can_dodge:
            if self.dodge_check():
                if silent == False:
                    self.broadcast(f'{self.name} dodged {damage_source}.')
                return 0

        match damage_type:
            case 'str': 
                damage -= int(self.stats['int']/2) 
            case 'agi': 
                damage -= int(self.stats['str']/2) 
            case 'int': 
                damage -= int(self.stats['agi']/2) 

        damage = int(damage)

        if silent == False:
            if damage <= 0:
                if damage_source != None:
                    self.broadcast(f'{self.name} blocked damage from {damage_source}.')
                else:
                    self.broadcast(f'{self.name} blocked damage.')

            else:
                if damage_source != None:
                    self.broadcast(f'{self.name} took {damage} damage from {damage_source}.')
                else:
                    self.broadcast(f'{self.name} took {damage} damage.')

        self.stats['hp'] -= damage
        if self.stats['hp'] <= 0:
            self.die()

        return damage
       

    def drain_mp(self, mp):
        self.stats['mp'] -= mp
        if self.stats['mp'] < 0: self.stats['mp'] = 0

        
        
        