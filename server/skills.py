def skill_check_alive(func):
    def wrapper(user, skill, target):
        if user.dead:
            user.broadcast(f'You are dead.', user)
            return
        return func(user, skill, target)
    return wrapper

def skill_check_user_has_skill(func):
    def wrapper(user, skill, target):
        if skill['index'] not in user.skills:
            user.broadcast(f'You dont have the skill "{skill["name"]}"', user)
            return
        return func(user, skill, target)
    return wrapper
            
def skill_check_use(func):
    def wrapper(user, skill, target):
        if skill['mp_cost'] > user.stats['mp']:
            user.broadcast(f'Not enough MP for {skill["name"]}.', user)
            return
            
        if skill['hp_cost'] > user.stats['hp']:
            user.broadcast(f'Not enough HP for {skill["name"]}.', user)
            return

        
        if skill['index'] in user.skill_cooldowns:
            user.broadcast(f'{skill["name"]} is on cooldown.', user)
            return

        user.stats['mp'] -= skill['mp_cost']
        user.stats['hp'] -= skill['hp_cost']
        user.set_cooldown(skill['index'],skill['cooldown'])

        user.broadcast(f'{user.name} Used {skill["name"]}.')
        return func(user, skill, target)
    return wrapper

def skill_check_cant_pvp(func):
    def wrapper(user, skill, target):
        targetting_ally = (user in user.room.players.values() and user.target in user.room.players.values()) or (user in user.room.enemies.values() and user.target in user.room.enemies.values()) 
        if targetting_ally and not user.room.pvp:
            user.broadcast(f'Not in PVP zone.', user)
            return
        return func(user, skill, target)
    return wrapper

def skill_check_default(func):
    @skill_check_alive
    @skill_check_user_has_skill
    @skill_check_use
    def wrapper(user, skill, target):
        return func(user, skill, target)
    return wrapper

def skill_check_target_self_if_none(func):
    def wrapper(user, skill, target):
        if target == None:
            target = user    
        if target.room != user.room:
            target = user
            return
        if target.dead:
            user.broadcast('Beating a dead horse?', user)
            return
        return func(user, skill, target)
    return wrapper

def skill_check_target_any(func):
    def wrapper(user, skill, target):
        if target == None:
            user.broadcast('You need a target.', user)
            return
        if target.room != user.room:
            user.broadcast('Target is not here.', user)
            return
        if target.dead:
            user.broadcast('Beating a dead horse?', user)
            return
        return func(user, skill, target)
    return wrapper

#######################################################################

@skill_check_target_any
@skill_check_cant_pvp
@skill_check_default
def skill_use_slash(user, skill, target):
    roll = user.stats['str'] 
    if user.crit_check(): 
        roll = roll * 2
    target.take_damage(damage = roll, damage_type = 'str', actor_source = user, damage_source = skill['name']) 

@skill_check_target_any
@skill_check_cant_pvp
@skill_check_default
def skill_use_stab(user, skill, target):
    roll = user.stats['agi'] 
    if user.crit_check(): 
        roll = roll * 3
    target.take_damage(damage = roll, damage_type = 'agi', actor_source = user, damage_source = skill['name']) 

@skill_check_target_any
@skill_check_cant_pvp
@skill_check_default
def skill_use_firebolt(user, skill, target):
    roll = user.stats['int'] 
    damage_taken = target.take_damage(damage = roll, damage_type = 'int', actor_source = user, damage_source = skill['name'])
    if user.crit_check() and damage_taken >= 1:
        target.set_status_effect('burning',9)

@skill_check_target_self_if_none
@skill_check_default
def skill_use_heal_light_wounds(user, skill, target):
    roll = user.stats['int'] + 6 
    target.regen(hp=roll)
    user.broadcast(f'{target.name} heals for {roll}.')
    
@skill_check_target_any
@skill_check_cant_pvp
@skill_check_default
def skill_use_ignite(user, skill, target):
    damage_taken = user.target.take_damage(damage = 0, damage_type = None, actor_source = user, damage_source = None, silent = True)
    target.set_status_effect('burning',4)

@skill_check_target_any
@skill_check_default
def skill_use_dance_hypnosis(user, skill, target):
    target.set_status_effect('dancing',10)