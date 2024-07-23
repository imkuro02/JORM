import json
import enum

class Action(enum.Enum):
    Chat = enum.auto()
    Login = enum.auto()
    Register = enum.auto()
    Ok = enum.auto()
    Deny = enum.auto()
    Disconnect = enum.auto()
    
    Premade = enum.auto()
    CharacterSheet = enum.auto()
    Equip = enum.auto()
    Unequip = enum.auto()

    Room = enum.auto()
    Go = enum.auto()
    Target = enum.auto()

    PartyRequest = enum.auto()
    PartyAnswer = enum.auto()
    PartyLeave = enum.auto()
    PartyKick = enum.auto()

    CombatStart = enum.auto()
    CombatAction = enum.auto()
    CombatReaction = enum.auto()
    CombatTurn = enum.auto()
    CombatStatusEffect = enum.auto()

class Packet:
    def __init__(self, action: Action,  *payloads):
        self.action: Action = action
        self.payloads: tuple = payloads

    def __str__(self) -> str:
        serialize_dict = {'a': self.action.name}
        for i in range(len(self.payloads)):
            serialize_dict[f'p{i}'] = self.payloads[i]
        data = json.dumps(serialize_dict, separators=(',',':'))
        return data

    def __bytes__(self) -> bytes:
        return str(self).encode('utf-8')

class ChatPacket(Packet):
    def __init__(self, message: str, sender = None):
        super().__init__(Action.Chat, message, sender)

class LoginPacket(Packet):
    def __init__(self, username: str, password: str):
        super().__init__(Action.Login, username, password)

class RegisterPacket(Packet):
    def __init__(self, username: str, password: str):
        super().__init__(Action.Register, username, password)

class OkPacket(Packet):
    def __init__(self):
        super().__init__(Action.Ok)

class DenyPacket(Packet):
    def __init__(self, reason: str):
        super().__init__(Action.Deny, reason)
    
class DisconnectPacket(Packet):
    def __init__(self, reason: str = None):
        super().__init__(Action.Disconnect, reason)

#
class PremadePacket(Packet):
    def __init__(self, premade: dict):
        super().__init__(Action.Premade, premade)

class CharacterSheetPacket(Packet):
    def __init__(self, character_sheet: dict):
        super().__init__(Action.CharacterSheet, character_sheet)

class EquipPacket(Packet):
    def __init__(self, item_id: str):
        super().__init__(Action.Equip, item_id)

class UnequipPacket(Packet):
    def __init__(self, item_id: str):
        super().__init__(Action.Unequip, item_id)
#
class RoomPacket(Packet):
    def __init__(self, name: str, description: str, exits: list, players: dict, enemies: dict):
        super().__init__(Action.Room, name, description, exits, players, enemies)

class GoPacket(Packet):
    def __init__(self, room_name: str):
        super().__init__(Action.Go, room_name)

class TargetPacket(Packet):
    def __init__(self, target: str):
        super().__init__(Action.Target, target)

#
class PartyRequestPacket(Packet):
    def __init__(self, actorID: int):
        super().__init__(Action.PartyRequestPacket, actorID)

class PartyAnswerPacket(Packet):
    def __init__(self, actorID: int, accept: bool):
        super().__init__(Action.PartyAnswer, actorID, accept)

class PartyLeavePacket(Packet):
    def __init__(self):
        super().__init__(Action.PartyLeave)

class PartyKickPacket(Packet):
    def __init__(self, actorID: int):
        super().__init__(Action.PartyKick, actorID)

# send a dict of every character in the combat, enemies and players
class CombatStartPacket(Packet):
    def __init__(self, combat: dict):
        super().__init__(Action.CombatStart, combat)

# send the id of which characters turn it is, player or enemy
class CombatTurnPacket(Packet):
    def __init__(self, actorID: int):
        super().__init__(Action.CombatTurn, actorID)

# player sends their combat action and their target
class CombatActionPacket(Packet):
    def __init__(self, target_actorID: int, action: str):
        super().__init__(Action.CombatAction, target_actorID, action)

class CombatReactionPacket(Packet):
    def __init__(self, actorID: int, reaction: dict):
        super().__init__(Action.CombatReaction, actorID, reaction)
'''
#reaction dict

{
'source':'bleed',
'stats':{
    'hp':-10
    'mp':-2
    }
}

# source is the source of the stat changes
# stats is the stats affected, so the client would see

Enemy0 loses 10 hp from bleed
Enemy0 loses 2 mp from bleed

and could therefore animate them properly

or possibly send each stat change as individual packet would be cleaner

{
'source':'bleed',
'hp': -10
}

{
'source':'bleed',
'mp': -2
}

this would work well with both skills and status effects

{
'source':'cleave',
'hp': -20
}

Enemy0 takes 20 damage from Cleave
'''
class CombatStatusEffectPacket(Packet):
    def __init__(self, actorID: int, status_effect: str, status_effect_amount: int):
        super().__init__(Action.CombatStatusEffect, actorID, status_effect, status_effect_amount)

'''
send the actorID of the affected actor, if the actor did not have that effect beforehand clientside print
Actor is now Blessed! / Bleeding! / Etc!

if a packet gets sent with amount of 0, then remove that status effect clientside, as it no longer exists on the server

Actor is no longer Bleeding / Blessed / Cursed / Etc

otherwise just keep track of the "amount variable" so the clients always know how much an actor is affected

status amount can both be a number of turns something lasts, and how much there is in a stack, for example bleeding wont go away on its own and only incriments
so amount means how much damage a character takes each turn

while blessed is a status that gives some bonus regardless of the amount, so amount 2 means for 2 more turns

'''

def from_json(json_str: str) -> Packet:
    obj_dict = json.loads(json_str)
    action = None
    payloads = []
    for key, value in obj_dict.items():
        if key == 'a':
            action = value

        if key[0] == 'p':
            index = int(key[1:])
            payloads.insert(index, value)

    # Use reflection to construct the specific packet type we're looking for
    class_name = action + "Packet"
    try:
        constructor: type = globals()[class_name]
        return constructor(*payloads)
    except KeyError as e:
        print(
            f"{class_name} is not a valid packet name. Stacktrace: {e}")
    except TypeError:
        print(
            f"{class_name} can't handle arguments {tuple(payloads)}.")

