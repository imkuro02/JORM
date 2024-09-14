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
            
