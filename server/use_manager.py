import random
import player
import useable

class UseManager:
    def __init__(self, factory):
        self.factory = factory
        useable.premade = self.factory.premade

    def use(self, user, obj, use_script):
        if hasattr(useable, use_script):
            constructed_script = getattr(useable, use_script)
            constructed_script(user, obj, user.target)
        else:
            user.broadcast(f'{use_script} does not exist.')
       

    def use_item(self, user, item_id):
        item  = self.factory.premade['items'][item_id]
        use_script = 'item_use_' + item['use_script']
        self.use(user, item, use_script)
        
    def use_skill(self, user, skill_id):
        skill = self.factory.premade['skills'][skill_id]
        use_script = 'skill_use_' + skill_id 
        self.use(user, skill, use_script)
        

    