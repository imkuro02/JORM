
def check(premade: dict):
    errors: list = []

    def add_error(err):
        errors.append(err)

    _items =    premade['items']
    _skills =   premade['skills']
    _statuses = premade['statuses']
    _enemies =  premade['enemies']

    # print(_enemies)

    for key, item in _enemies.items():
        for i in item:
            if i not in _enemies['template']:
                add_error(f'"{key}" has value "{i}" while Template Enemy does not have this value')

        for i in _enemies['template']:
            if i not in item:
                add_error(f'"{key}" is lacking value "{i}" which Template Enemy has')

        child_stats = item['stats'].keys()
        parent_stats =  _enemies['template']['stats'].keys()

        if child_stats != parent_stats:
            add_error(f'"{key}" and Template Enemy do not share same stats child vs parent:\n{child_stats}\n{parent_stats}')
            
        for stat in child_stats:
            s = item['stats'][stat]
            if type(s) != int:
                add_error(f'"{key}" has a non intiger stat "{stat}"="{s}"')   


    for key, item in _skills.items():
        if 'name' not in item: add_error(f'{key} has no "name"') 
        if 'description' not in item: add_error(f'{key} has no "description"') 

    for key, item in _items.items():
        
        #print(key)
        #print(item)

        if 'name' not in item:
            add_error(f'{key} has no name')
            continue

        if 'description' not in item:
            add_error(f'{key} has no description')
            continue

        if 'parent' not in item:
            add_error(f'{key} has no parent')
            continue

        for i in item:
            if i not in _items[item['parent']]:
                if i == 'parent': continue
                add_error(f'"{key}" has value "{i}" while their parent "{item["parent"]}" does not have this value')

        for i in _items[item['parent']]:
            if i not in item:
                if i == 'level_req': continue
                if i == 'skills': continue
                add_error(f'"{key}" is lacking value "{i}" which their parent "{item["parent"]}" has')
        
        if 'equipable' == item['parent']:
            child_stats = item['stats'].keys()
            parent_stats = _items[item['parent']]['stats'].keys()

            if child_stats != parent_stats:
                add_error(f'"{key}" and their parent "{item["parent"]}" do not share same stats child vs parent:\n{child_stats}\n{parent_stats}')
                
            for stat in child_stats:
                s = item['stats'][stat]
                if type(s) != int:
                    add_error(f'"{key}" has a non intiger stat "{stat}"="{s}"')       

        #print(f'processed: {key}:\n{item}')
    for _e in errors:
        print(_e)

    
if __name__ == '__main__':
    import premade
    _premade = premade.get_premade()
    check(_premade)