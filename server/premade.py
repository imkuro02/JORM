from utils import dc
import ezodf

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
    'int':'Intelligence',
    'wis':'Wisdom',
    'cha':'Charisma',
    
    'crit_chance':'Crit Chance',
    'dodge_chance':'Dodge Chance',
    'physic_block':'Physic Block',
    'magic_block':'Magic Block',

    'physic_damage': 'Physic Damage',
    'magic_damage': 'Magic Damage'
}

def create_all_skills():
    ods_file = ezodf.opendoc('skills.ods')
    sheet = ods_file.sheets[0]
    rows = list(sheet.rows())
    labels = [cell.value for cell in rows[0]]
    skill_dict = {}

    _skills = {}

    for row in rows[1:]:
        row_values = [cell.value for cell in row]
        skill_id = row_values[0]
        if skill_id == None:
            continue
        skill_dict = dict(zip(labels, row_values))
        skill_dict[skill_id] = skill_dict
        _skills[skill_id] = {}
        _skills[skill_id]['name'] = skill_dict['name']
        _skills[skill_id]['script'] = skill_dict['script']
        _skills[skill_id]['target'] = skill_dict['target']
        _skills[skill_id]['mp_cost'] = int(skill_dict['mp_cost'])
        _skills[skill_id]['hp_cost'] = int(skill_dict['hp_cost'])
        _skills[skill_id]['description'] = skill_dict['description']

    return _skills

def create_all_skill_sets():
    ods_file = ezodf.opendoc('skill_sets.ods')
    sheet = ods_file.sheets[0]
    rows = list(sheet.rows())
    labels = [cell.value for cell in rows[0]]
    skill_dict = {}

    _skills = {}

    for row in rows[1:]:
        row_values = [cell.value for cell in row]
        skill_id = row_values[0]
        skill_dict = dict(zip(labels, row_values))
        skill_dict[skill_id] = skill_dict
        _skills[skill_id] = skill_dict

    
    skills = {}
    for s in _skills:
        _id = _skills[s]['id']
        skills[_id] = []
        for i in range(0,5):
            if _skills[_id]['skill'+str(i)] != None:
                skills[_id].append(_skills[_id]['skill'+str(i)]) 
        
        

    return skills

def create_all_items():
    all_skills = create_all_skill_sets()

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
        #print(item)
        level_req = int(item['level_req'])
        skills = item['skills']

        if skills != None:
            skills = all_skills[skills]
        else:
            skills = []

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
            'skills': skills,
            'level_req': level_req,
            'stats': stats,
            'use_script': use_script
        }

        if use_script == None: 
            del new_item['use_script']
        if slot == None: 
            del new_item['skills']
            del new_item['slot']
            del new_item['stats']
            del new_item['level_req']

        items[item_id] = new_item
        
    return items

def get_premade():
    return {
        'items': create_all_items(),
        'translations': translations,
        'skills': create_all_skills()
    }

if __name__ == '__main__':
    p = get_premade()
    print(p['skills'])
