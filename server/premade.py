from utils import dc

PLAYER_STATS = {
    'hp':       10,
    'mp':       10,
    'max_hp':   10,
    'max_mp':   10,
    'exp':      0,
    'points':   0,

    'crit_chance':  0,
    'dodge_chance': 0,
    'physic_block': 0,
    'magic_block':  0,

    'physic_damage': 2,
    'magic_damage': 2,

    'str':      1,
    'dex':      1,
    'con':      1,
    'int':      1,
    'wis':      1,
    'cha':      1
}


ENEMY_STATS = {
    'hp':       10,
    'mp':       10,
    'max_hp':   10,
    'max_mp':   10,

    'crit_chance':  0,
    'dodge_chance': 0,
    'physic_block': 0,
    'magic_block':  0,

    'physic_damage': 4,
    'magic_damage': 4,

    'str':      1,
    'dex':      1,
    'con':      1,
    'int':      1,
    'wis':      1,
    'cha':      1
}


ITEM_STATS = {
    'max_hp':   0,
    'max_mp':   0,

    'crit_chance':  0,
    'dodge_chance': 0,
    'physic_block': 0,
    'magic_block':  0,

    'physic_damage': 0,
    'magic_damage': 0,

    'str':      0,
    'dex':      0,
    'con':      0,
    'int':      0,
    'wis':      0,
    'cha':      0
}

PLAYER_SKILLS = {
    'basic_attack': {
        'name': 'Reckless Charge',
        'description': 'Recklessly charge the target! dealing dealing between 1 and physic_damage'
    }


}
items_equipable = {
    'sword0': {
        'name':'Basic Sword', 
        'stats': {'str': 1, 'dex': -1, 'physic_damage':10}, 
        'description': 'A cool looking sword', 
        'slot': 'weapon'
        },

    'helmet0': {
        'name':'Basic Helmet', 
        'stats': {'max_hp':5,'str': 4, 'dex': 1, 'physic_block': 10, 'magic_damage': 2}, 
        'description': 'A hat', 
        'slot': 'helmet'
        },

    'katana': {
        'name':'Super Katana', 
        'stats': {'dex': 68, 'magic_damage': 10, 'max_mp':10}, 
        'description': 'A cool looking katana', 
        'slot': 'weapon'
        }
}

items_consumable = {
    'potion0': {
        'name': 'Health Potion',
        'description': 'A health potion that heals 10% of your max HP!',
        'use_script': 'potion0'
    }
}
items_misc = {
    'coins': {
        'name': 'Coins',
        'description': 'Shiny!'
        },

    'rock': {
        'name':'Gray Rock', 
        'description': 'Just a gray boring rock...'
        }
}

translations = {
    'exp':'EXP',
    'points': 'Points',

    'max_hp':'Max Health',
    'hp':'Health',
    'max_mp':'Max Mana',
    'mp':'Mana',

    'str':'Strength',
    'dex':'Dexterity',
    'con':'Constitution',
    'int':'Inteligence',
    'wis':'Wisdom',
    'cha':'Charisma',
    
    'crit_chance':'Critical Chance',
    'dodge_chance':'Dodge Chance',
    'physic_block':'Physic Block',
    'magic_block':'Magic Block',

    'physic_damage': 'Physic Damage',
    'magic_damage': 'Magic Damage'
}


def create_all_items():
    items = {}

    # Create equipable items
    for item_id, item_data in items_equipable.items():
        item = dc(item_data)
        item['stats'] = {**ITEM_STATS, **item['stats']}
        #if 'damage' in item:
        #    item['damage'] = {**DAMAGE, **item['damage']}
        items[item_id] = item

    # Create miscellaneous items
    for item_id, item_data in items_misc.items():
        items[item_id] = dc(item_data)

    # Create miscellaneous items
    for item_id, item_data in items_consumable.items():
        items[item_id] = dc(item_data)

    everything = {'items':items,'translations':translations}
    return everything

if __name__ == '__main__':
    all_items = create_all_items()
    print(all_items)


