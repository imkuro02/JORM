from utils import dc
import ezodf

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

PLAYER_SKILLS = {
    'basic_attack': {
        'name': 'Reckless Charge',
        'description': 'Recklessly charge the target! dealing dealing between 1 and physic_damage'
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
    # Load the ODS file
    ods_file = ezodf.opendoc('items.ods')

    # Access the first sheet
    sheet = ods_file.sheets[0]

    # Convert rows generator to a list
    rows = list(sheet.rows())

    # Read the first row to get column labels
    labels = [cell.value for cell in rows[0]]

    # Initialize an empty dictionary to store items
    items_dict = {}

    # Iterate over the rows starting from the second row
    for row in rows[1:]:
        # Extract the cell values from the row
        row_values = [cell.value for cell in row]
        
        # Assume the first column is the ID
        item_id = row_values[0]
        
        # Create a dictionary for the current item
        item_dict = dict(zip(labels, row_values))
        
        # Store the item in the items_dict using the item_id as the key
        items_dict[item_id] = item_dict

    # Print the resulting dictionary
    items = {}
    for item_id, item in items_dict.items():
        if item['id'] == None:
            continue
        name = item['name']
        description = item['description']
        stats = {
            'max_hp': int(item['max_hp']),
            'max_mp': int(item['max_mp']),

            
            'crit_chance': int(item['crit_chance']),
            'dodge_chance': int(item['dodge_chance']),
            
            'physic_block': int(item['physic_block']),
            'magic_block': int(item['magic_block']),
            
            'physic_damage': int(item['physic_damage']),
            'magic_damage': int(item['magic_damage']),
            
            

            'str': int(item['str']),
            'dex': int(item['dex']),
            'con': int(item['con']),
            'int': int(item['int']),
            'wis': int(item['wis']),
            'cha': int(item['cha'])
        }

        slot = item['slot']
        use_script = item['use_script']

        new_item = {
            'name': name,
            'description': description,
            'slot': slot,
            'stats': stats,
            'use_script': use_script
        }

        if use_script == None: 
            del new_item['use_script']
        if slot == None: 
            del new_item['slot']
            del new_item['stats']

        items[item_id] = new_item
        
    return {'items': items, 'translations': translations}

if __name__ == '__main__':
    all_items = create_all_items()
    print(all_items)


