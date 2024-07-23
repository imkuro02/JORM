class Actor:

    def character_stats(self):
        return {
            'name': self.name,
            'stats': {'hp':self.stats['hp'],'max_hp':self.stats['max_hp'],'mp':self.stats['mp'],'max_mp':self.stats['max_mp']}
        }
        
    def use_skill(self,skill_name):
        if self.target.room != self.room:
            return 'Target is not here'

        if skill_name == 'basic_attack':
            roll = random.randrange(1,self.stats['physic_damage'])
            self.target.take_physic_damage(hp = roll)

    def regen(self, hp = 0, mp = 0):
        self.stats['hp'] += hp
        if self.stats['hp'] > self.stats['max_hp']:
            self.stats['hp'] = self.stats['max_hp']

        self.stats['mp'] += mp
        if self.stats['mp'] > self.stats['max_mp']:
            self.stats['mp'] = self.stats['max_mp']

    def take_physic_damage(roll, skill_name):
        roll -= self.stats['physic_block']
        if roll <= 0:
            return f'{self.name} Blocked all damage from {skill_name}'
        
        self.stats['hp'] -= roll
        return f'{self.name} took {roll} damage from {skill_name}'