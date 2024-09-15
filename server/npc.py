from utils import dc
class NPC:
    def __init__ (self, name, room, dialog_tree):
        self.name = name
        self.room = room
        self.room.npcs[name] = self
        self.dialog_tree = self.room.map.factory.premade['dialog'][dialog_tree]

    def dialog(self, player, response):
        if response in self.dialog_tree:
            custom_response = dc(self.dialog_tree[response])

            if 'trade' in custom_response:
                check_failed = False
                for item in custom_response['trade']:
                    if item['quantity'] == 0 and item['item'] in player.inventory:
                        check_failed = True
                        continue

                    if item['quantity'] < 0:
                        if item['item'] in player.inventory:
                            if (item['quantity']*-1) > player.inventory[item['item']]:
                                check_failed = True
                                continue
                        else:
                            check_failed = True
                            continue

                if check_failed:
                    custom_response = custom_response['fail']
                else:
                    
                    for item in custom_response['trade']:
                        if item['quantity'] > 0: player.add_item(item['item'],item['quantity'])
                        if item['quantity'] < 0: player.remove_item(item['item'],-1*item['quantity'])

                    custom_response = custom_response['success']

            custom_response['text'] = custom_response['text'].replace('PLAYER', player.name)
            custom_response['text'] = custom_response['text'].replace('NPC', self.name)

            
            if 'responses' in custom_response:
                if custom_response['responses'] != None:
                    player_responses = []
                    for r in custom_response['responses']:
                        r['text'] = r['text'].replace('PLAYER', player.name)
                        r['text'] = r['text'].replace('NPC', self.name)
                        player_responses.append(r)
                    
                    custom_response['responses'] = player_responses

            return custom_response
            
