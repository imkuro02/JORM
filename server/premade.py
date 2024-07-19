from utils import dc

ENTITY_STATS = {
    'hp':       10,
    'mp':       10,
    'max_hp':   10,
    'max_mp':   10,
    'exp':      0,
    'points':   0,

    'crt':      1,
    'avd':      1,
    'pac':      1,
    'mac':      1,

    'str':      1,
    'dex':      1,
    'con':      1,
    'int':      1,
    'wis':      1,
    'cha':      1
}

STATS = {
    'max_hp':   0,
    'max_mp':   0,

    'crt':      0,
    'avd':      0,
    'pac':      0,
    'mac':      0,

    'str':      0,
    'dex':      0,
    'con':      0,
    'int':      0,
    'wis':      0,
    'cha':      0
}

DAMAGE = {
    'scaling': 'str',
    'def_type': 'pac',
    'min': 1,
    'max': 10    
}

items_equipable = {
    'sword0': {
        'name':'Basic Sword', 
        'stats': {'str': 1, 'dex': -1}, 
        'damage': {'scaling': 'str', 'min': 10, 'max': 21}, 
        'description': 'A cool looking sword', 
        'slot': 'weapon'
        },

    'helmet0': {
        'name':'Basic Helmet', 
        'stats': {'max_hp':5,'str': 4, 'dex': 1, 'pac': 10}, 
        'description': 'A hat', 
        'slot': 'helmet'
        },

    'katana': {
        'name':'Super Katana', 
        'stats': {'dex': 68}, 
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

def create_all_items():
    items = {}

    # Create equipable items
    for item_id, item_data in items_equipable.items():
        item = dc(item_data)
        item['stats'] = {**STATS, **item['stats']}
        if 'damage' in item:
            item['damage'] = {**DAMAGE, **item['damage']}
        items[item_id] = item

    # Create miscellaneous items
    for item_id, item_data in items_misc.items():
        items[item_id] = dc(item_data)

    # Create miscellaneous items
    for item_id, item_data in items_consumable.items():
        items[item_id] = dc(item_data)

    return items

if __name__ == '__main__':
    all_items = create_all_items()
    print(all_items)


