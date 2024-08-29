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
    'agi':'Agility',
    'int':'Intelligence',
    
    'crit_chance':'Crit Chance',
    'dodge_chance':'Dodge Chance',
    
}

def create_all_enemies():
    with open('premade/enemies.yaml', 'r') as file:
        enemies = yaml.safe_load(file)

    template = enemies['template']

    for enemy in enemies:
        for attribute in template:
            if attribute not in enemies[enemy]: enemies[enemy][attribute] = template[attribute]

        for stat in template['stats']:
            if stat not in enemies[enemy]['stats']: enemies[enemy]['stats'][stat] = template['stats'][stat]
                



    return enemies
        
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
        #_skills[skill_id]['script'] = skill_dict['script']
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

import yaml
def create_all_items():
    items = {}
    with open('premade/items.yaml', 'r') as file:
        items = yaml.safe_load(file)

    for item in items:
        if 'parent' in items[item]:
            template = dc(items['template'])
            to_copy = items[item]

            #if 'skills' in to_copy:
            #    to_copy['skills'] = template['skills']

            if 'description' not in to_copy:
                to_copy['description'] = template['description']
            
            if 'equipable' == to_copy['parent']:
                if 'stats' in to_copy:
                    template['stats'].update(to_copy['stats'])
                to_copy['stats'] = template['stats']
                
            items[item] = to_copy

    return items


def create_all_statuses():
    statuses = {}
    with open('premade/statuses.yaml', 'r') as file:
        statuses = yaml.safe_load(file)

    return statuses

def get_premade():
    return {
        'items': create_all_items(),
        'translations': translations,
        'skills': create_all_skills(),
        'statuses': create_all_statuses(),
        'enemies': create_all_enemies()
    }

if __name__ == '__main__':
    p = get_premade()
    for i in p['enemies']:
        print(p['enemies'][i])
