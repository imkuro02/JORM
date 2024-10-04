from utils import dc
class NPC:
    def __init__ (self, dialog_tree, room):
        
        self.room = room
        self.name = self.room.map.factory.premade['dialog'][dialog_tree]['name']
        self.room.npcs[self.name] = self
        self.dialog_tree = self.room.map.factory.premade['dialog'][dialog_tree]

    def dialog(self, player, response):
        if response in self.dialog_tree:

            if response == 'trade':
                return
                
            custom_response = dc(self.dialog_tree[response]) 
            cr = custom_response

            condition_passed = True

            if 'player_equipment' in cr['try']:

                for i in cr['try']['player_equipment']:
                    if i['quantity'] >= 1 and i['item'] not in player.equipment:
                        condition_passed = False
                    if i['quantity'] <= 0 and i['item'] in player.equipment:
                        condition_passed = False
                        
            if 'player_inventory' in cr['try']:
                for i in cr['try']['player_inventory']:
                    if i['quantity'] <= -1:
                        if i['item'] in player.inventory: 
                            if player.inventory[i['item']] < i['quantity']*-1:
                                condition_passed = False
                        else:
                            condition_passed = False
                    if i['quantity'] == 0 and i['item'] in player.inventory:
                        condition_passed = False

                if condition_passed:
                    for i in cr['try']['player_inventory']:
                        if i['quantity'] <= -1: player.remove_item(i['item'],i['quantity']*-1)
                        if i['quantity'] > 0: player.add_item(i['item'],i['quantity'])

                     


            if condition_passed:
                cr = cr['try']
            else:
                cr = cr['fail']

            cr['text'] = cr['text'].replace('PLAYER', player.name)
            cr['text'] = cr['text'].replace('NPC', self.name)

            player_responses = []
            
            if 'responses' in cr:

                #cr['responses'] = dc(self.dialog_tree[1]['try']['responses'])+cr['responses']
                if cr['responses'] != None:
                    
                    for r in cr['responses']:
                        r['text'] = r['text'].replace('PLAYER', player.name)
                        r['text'] = r['text'].replace('NPC', self.name)
                        player_responses.append(r)
                    
                    cr['responses'] = player_responses

            return cr
            
