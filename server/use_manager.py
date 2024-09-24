import random
import player
import skills

class UseManager:
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

        skill = self.factory.premade['skills'][skill_id]
        use_script = 'skill_use_' + skill_id 
        try:
            constructed_script = getattr(skills, use_script)
            constructed_script(user, skill, user.target)
        except KeyError as e:
            #print(f"{use_script} is not a valid use script name. Stacktrace: {e}")
            user.broadcast(f'Skill: {skill["index"]} / {skill["name"]} does not exist')
        except TypeError:
            #print(f"{use_script} can't handle arguments.")
            pass

    