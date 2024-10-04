# get the factory.premade so it will be easier to print names etc
premade = {}

# checks
def check_alive(func):
    def wrapper(user, obj, target):
        if user.dead:
            user.broadcast(f'You are dead.', user)
            return
        return func(user, obj, target)
    return wrapper

def check_user_has_skill(func):
    def wrapper(user, skill, target):
        if skill['index'] not in user.skills:
            user.broadcast(f'You dont have the skill "{skill["name"]}."', user)
            return
        return func(user, skill, target)
    return wrapper

def check_user_has_item(func):
    def wrapper(user, obj, target):
        if obj['index'] not in user.skills:
            user.broadcast(f'You dont have a "{obj["name"]}."', user)
            return
        return func(user, skill, target)
    return wrapper

def check_item_consume(amount):
    def decorator(func):
        def wrapper(user, obj, target):
            if user.inventory[obj['index']] < amount:
                user.broadcast(f'You need {amount} x "{obj["name"]}."', user)
                return
            user.remove_item(obj['index'], amount)
            return func(user, obj, target)
        return wrapper
    return decorator
            
def check_skill_use(func):
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

        user.broadcast(f'{user.name} used {skill["name"]}.')
        return func(user, skill, target)
    return wrapper

def check_cant_pvp(func):
    def wrapper(user, obj, target):
        targetting_ally = (user in user.room.players.values() and user.target in user.room.players.values()) or (user in user.room.enemies.values() and user.target in user.room.enemies.values()) 
        if targetting_ally and not user.room.pvp:
            user.broadcast(f'Not in PVP zone.', user)
            return
        return func(user, obj, target)
    return wrapper

def check_skill_default(func):
    @check_alive
    @check_user_has_skill
    @check_skill_use
    def wrapper(user, skill, target):
        return func(user, skill, target)
    return wrapper

def check_target_self_if_none(func):
    def wrapper(user, obj, target):
        if target == None:
            target = user    
        if target.room != user.room:
            target = user
            return
        if target.dead:
            user.broadcast('Beating a dead horse?', user)
            return
        return func(user, obj, target)
    return wrapper

def check_target_self_always(func):
    def wrapper(user, obj, target):
        target = user
        return func(user, obj, target)
    return wrapper


def check_has_valid_target(func):
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

def check_status(status, need_status):
    def decorator(func):
        def wrapper(user, obj, target):
            
            if not need_status and status in target.status_effects:
                user.broadcast(f'Can\'t use {obj["name"]} while under the effect of {premade["statuses"][status]["name"]}', user)
                return

            if need_status and status not in target.status_effects:
                user.broadcast(f'Can\'t use {obj["name"]} while not under the effect of {premade["statuses"][status]["name"]}', user)
                return

            return func(user, obj, target)
        return wrapper
    return decorator

# skill_use

@check_has_valid_target
@check_cant_pvp
@check_skill_default
def skill_use_slash(user, skill, target):
    roll = user.stats['str'] 
    if user.crit_check(): 
        roll = roll * 2
    target.take_damage(damage = roll, damage_type = 'str', actor_source = user, damage_source = skill['name']) 

@check_has_valid_target
@check_cant_pvp
@check_skill_default
def skill_use_stab(user, skill, target):
    roll = user.stats['agi'] 
    if user.crit_check(): 
        roll = roll * 3
    target.take_damage(damage = roll, damage_type = 'agi', actor_source = user, damage_source = skill['name']) 

@check_has_valid_target
@check_cant_pvp
@check_skill_default
def skill_use_firebolt(user, skill, target):
    roll = user.stats['int'] 
    damage_taken = target.take_damage(damage = roll, damage_type = 'int', actor_source = user, damage_source = skill['name'])
    if user.crit_check() and damage_taken >= 1:
        target.set_status_effect('burning',9)

@check_target_self_if_none
@check_skill_default
def skill_use_heal_light_wounds(user, skill, target):
    roll = user.stats['int'] + 6 
    target.regen(hp=roll)
    user.broadcast(f'{target.name} heals for {roll}.')
    
@check_has_valid_target
@check_cant_pvp
@check_skill_default
def skill_use_ignite(user, skill, target):
    damage_taken = user.target.take_damage(damage = 0, damage_type = None, actor_source = user, damage_source = None, silent = True)
    target.set_status_effect('burning',4)


@check_has_valid_target
@check_skill_default
def skill_use_dance_hypnosis(user, skill, target):
    target.set_status_effect('dancing',10)

# item_use
@check_alive
@check_target_self_always
@check_status('potion_sickness', False)
@check_item_consume(1)
def item_use_regen_hp(user, item, target):
    user.regen(hp=10)
    user.broadcast(f'{user.name} used {item["name"]}', anim = 'drink')
    user.set_status_effect(status_effect = 'potion_sickness', amount = 20, broadcast_to = user)

@check_alive
@check_target_self_always
@check_status('potion_sickness', False)
@check_item_consume(1)
def item_use_regen_mp(user, item, target):
    user.regen(mp=10)
    user.broadcast(f'{user.name} used {item["name"]}', anim = 'drink')
    user.set_status_effect(status_effect = 'potion_sickness', amount = 20, broadcast_to = user)

@check_alive
@check_target_self_always
@check_status('potion_sickness', False)
@check_item_consume(1)
def item_use_regen_hp_and_mp(user, item, target):
    user.regen(hp=10, mp=10)
    user.broadcast(f'{user.name} used {item["name"]}', anim = 'drink')
    user.set_status_effect(status_effect = 'potion_sickness', amount = 20, broadcast_to = user)

@check_alive
@check_target_self_always
@check_status('motion_sickness', False)
def item_use_tp_spawn(user, item, target):
    user.broadcast(f'{user.name} used {item["name"]}')
    user.room.move_player(player = user, new_room = 'spawn', forced = True)
    user.set_status_effect(status_effect = 'motion_sickness', amount = 20, broadcast_to = user)