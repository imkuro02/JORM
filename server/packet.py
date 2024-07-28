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
    Drop = enum.auto()
    UseSkill = enum.auto()

    FlavouredMessage = enum.auto()

    Room = enum.auto()
    Go = enum.auto()
    Target = enum.auto()

    PartyRequest = enum.auto()
    PartyAnswer = enum.auto()
    PartyLeave = enum.auto()
    PartyKick = enum.auto()

    

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

class DropPacket(Packet):
    def __init__(self, item_id: str, quantity: int):
        super().__init__(Action.Drop, item_id, quantity)

class UseSkillPacket(Packet):
    def __init__(self, skill_id: str):
        super().__init__(Action.UseSkill, skill_id)

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

class FlavouredMessagePacket(Packet):
    def __init__(self,message):
        super().__init__(Action.FlavouredMessage, message)

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

