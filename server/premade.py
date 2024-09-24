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

def create_all_dialog():
    with open('premade/dialog.yaml', 'r') as file:
        dialog = yaml.safe_load(file)

    return dialog

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
    skills = {}
    with open('premade/skills.yaml', 'r') as file:
        skills = yaml.safe_load(file)

    for skill in skills:
        skills[skill]['index'] = skill

    return skills

def create_all_skill_sets():
    skills = {}
    with open('premade/skills.yaml', 'r') as file:
        skills = yaml.safe_load(file)
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
        'enemies': create_all_enemies(),
        'dialog': create_all_dialog()
    }

if __name__ == '__main__':
    
    p = get_premade()
    for i in p['skills']:
        print(p['skills'][i])
