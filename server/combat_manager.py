import random
import player

class CombatManager:
    def __init__(self, factory):
        self.factory = factory

    def use_item(self,user,item_id):
        if not isinstance(user, player.Player):
            print(user, user.name, 'tried to use ', item_id, 'but this is a class ', type(user))
            return 

        if user.dead:
            user.broadcast('You are Dead', user)
            return

        if item_id not in user.room.map.factory.premade['items']:
            user.broadcast('That item does not exist', user)
            return

        item = user.room.map.factory.premade['items'][item_id]

        if item_id not in user.inventory:
            user.broadcast(f'You don\'t have {item["name"]}')
            return

        match item['use_script']:
            case 'restore_hp_10':
                if user.has_status_effect('potion_sickness'): 
                    return
                user.regen(hp=10)
                user.broadcast(f'{user.name} used {item["name"]}', anim = 'drink')
                user.set_status_effect(status_effect = 'potion_sickness', amount = 20, broadcast_to = user)
                user.remove_item(item_id,1)

            case 'restore_mp_10':
                if user.has_status_effect('potion_sickness'): 
                    return
                user.regen(mp=10)
                user.broadcast(f'{user.name} used {item["name"]}', anim = 'drink')
                user.set_status_effect(status_effect = 'potion_sickness', amount = 20, broadcast_to = user)
                user.remove_item(item_id,1)


        
        
        

    def use_skill(self,user,skill_id):

        if user.dead:
            user.broadcast('You are Dead', user)
            return

        # CONDITIONS AND EARLY RETURNS
        if skill_id not in user.skills:
            user.broadcast('You do not know that skill', user)
            return

        if skill_id not in self.factory.premade['skills']:
            user.broadcast('Skill does not exist', user)
            return 
        
        skill = self.factory.premade['skills'][skill_id]

        if skill['target'] != 'none':
            if user.target == None:
                user.broadcast(f'You are not targetting anyone', user)
                return 

            if user.target.room != user.room:
                user.broadcast(f'{user.target.name} is not here', user)
                return 
                
            if user.target.dead:
                user.broadcast(f'This target is already dead', user)
                return 

            targetting_ally = (user in user.room.players.values() and user.target in user.room.players.values()) or (user in user.room.enemies.values() and user.target in user.room.enemies.values())
            

            if skill['target'] == 'ally' and not targetting_ally:
                user.broadcast(f'Target must be an ally', user)
                return 
            
            if skill['target'] == 'enemy' and targetting_ally:
                user.broadcast(f'Target Can\'t be an ally', user)
                return 

            if (skill['target'] == 'any') and (targetting_ally == True) and (user.room.pvp == False) == True:
                user.broadcast(f'Not in PVP zone.',user)
                return
        
        
        if skill_id in user.skill_cooldowns:
            user.broadcast(f'{skill["name"]} is on cooldown', user)
            return

        if skill['mp_cost'] > user.stats['mp']:
            user.broadcast(f'Not enough MP to use {skill["name"]}', user)
            return

        if skill['hp_cost'] > user.stats['hp']:
            user.broadcast(f'Not enough HP to use {skill["name"]}', user)
            return

        user.stats['mp'] -= skill['mp_cost']
        user.stats['hp'] -= skill['hp_cost']

        # CHECK FOR CRIT
        crit = random.randrange(0,100)
        crit = crit <= user.stats['crit_chance']

        # Print crit or not :p
        if crit:
            user.broadcast(f'{user.name} used {skill["name"]}, its Critical!')
        else:
            user.broadcast(f'{user.name} used {skill["name"]}')
       
        # add cooldown of 6 seconds for every skill unless skill is on cooldown
        for i in user.skills:
            if i in user.skill_cooldowns:
                continue
            user.set_cooldown(i,2)

        user.set_cooldown(skill_id,skill['cooldown'])

        match skill_id:
            case 'heal_light_wounds':
                roll = user.stats['int'] + 6
                user.target.regen(hp=roll)
                user.broadcast(f'{user.name} heals {user.target.name} for {roll}')
            case 'first_aid':
                roll = 6
                user.target.regen(hp=roll)
                user.broadcast(f'{user.name} heals {user.target.name} for {roll}')
            case 'stab':
                roll = user.stats['agi'] 
                if crit: 
                    roll = roll * 3
                user.target.take_damage(damage = roll, damage_type = 'agi', actor_source = user, damage_source = skill['name'])
            case 'slash':
                roll = user.stats['str'] 
                if crit: 
                    roll = roll * 2
                user.target.take_damage(damage = roll, damage_type = 'str', actor_source = user, damage_source = skill['name'])
            case 'spit':
                roll = user.stats['int'] 
                if crit: 
                    roll = roll * 2
                user.target.take_damage(damage = roll, damage_type = 'int', actor_source = user, damage_source = skill['name'])
            case 'ignite':
                #roll = user.stats['int'] 
                #damage_taken = user.target.take_damage(damage = roll, damage_type = 'int', actor_source = user, damage_source = skill['name'])
                user.target.set_status_effect('burning',4)

            case 'firebolt':
                roll = user.stats['int'] 
                damage_taken = user.target.take_damage(damage = roll, damage_type = 'int', actor_source = user, damage_source = skill['name'])
                if crit and damage_taken >= 1:
                    user.target.set_status_effect('burning',9)

            case 'dance_hypnosis':
                user.target.set_status_effect('dancing',10)
                
            case 'push':
                roll = user.stats['str'] 
                if roll <= 0: roll = 1
                if crit: 
                    roll = roll * 2
                user.broadcast(f'{user.target.name} lost {int(roll)} MP!')
                user.target.drain_mp(mp = roll)
            case 'guard':
                user.regen(hp=10+user.stats['str'],mp=0)
                user.broadcast(f'GRRRR!')
        return