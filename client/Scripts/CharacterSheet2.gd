extends Panel

const Packet = preload("res://Scripts/Packet.gd")

@onready var ch = $VSplitContainer/CharacterSheet
@onready var inv = $VSplitContainer/Inventory

@onready var inv_text = inv.get_node('Inventory')
@onready var inv_search = inv.get_node('LineEdit')

@onready var combat = $VSplitContainer/Combat
@onready var skills = $VSplitContainer/Combat/Skills
@onready var others = $VSplitContainer/Combat/Others

var autouse_skills = []
var prev_autouse = 0

var MAIN
var hovered_item = null
var GAME

var state = 'sheet'


func _ready():
	MAIN = get_tree().root.get_node('Main')

func _process(_delta):
	ch.visible = state == 'sheet'
	inv.visible = state == 'inventory'
	combat.visible = state == 'combat'
	
func receive_others(target, players, enemies):
	
	others.text = ''
		
	#others.text += 'Players:\n'
	for player in players:
		var character = players[player]
		var id = player
		var name = player
		var hp = character['stats']['hp']
		var max_hp = character['stats']['max_hp']
		if target == id:
			others.text += GAME.interactable('target',id,name)
		else:
			others.text += GAME.interactable('player',id,name)
		others.text += '\n'
		#others.text += ''' [color=red] %s%%[/color]\n''' % [int((hp/max_hp)*100)]
	
	#others.text += 'Enemies:\n'
	for enemy in enemies:
		var character = enemies[enemy]
		var id = enemy
		var name = enemy
		var hp = character['stats']['hp']
		var max_hp = character['stats']['max_hp']
		if target == id:
			others.text += GAME.interactable('target',id,name)
		else:
			others.text += GAME.interactable('enemy',id,name)
		others.text += '\n'
		#others.text += ''' [color=red] %s%%[/color]\n''' % [int((hp/max_hp)*100)]
	pass
	
func receive_skills(_skills,_cooldowns):
	var SKILLS = MAIN.PREMADE['skills']
	''' SKILLS '''
	skills.text = '[table=4]'
	for skill in _skills:
		var cooldown = ''
		var autouse = ''

		if skill in _cooldowns:
			cooldown = '(%ss)' % [int(abs(MAIN.SERVER_TIME - _cooldowns[skill])/30)+1]
			
		if skill in autouse_skills:
			autouse = '(A)'
		skills.text += '[cell]%s [/cell][cell][color="aqua"]%s [/color][/cell][cell] %s[/cell][cell]%s[/cell] \n' % [
			GAME.interactable('skill',skill,SKILLS[skill]['name']),
			SKILLS[skill]['mp_cost'],
			cooldown,
			autouse
		]
	skills.text += '[/table]'
	
	''' AutoUse '''
	for skill in autouse_skills:
		if skill not in _skills:
			#print(autouse_skills)
			autouse_skills.erase(skill)
			
	
	if $VSplitContainer/Combat/AutoUse.button_pressed == true:
		for skill in autouse_skills:
			if prev_autouse < MAIN.SERVER_TIME - 30:
				if skill not in _cooldowns:
					var p = Packet.new('UseSkill',[skill])
					MAIN.send_packet(p)
				
	if prev_autouse < MAIN.SERVER_TIME - 30:
		prev_autouse = MAIN.SERVER_TIME
	''' AutoUse '''
	''' SKILLS '''
	
func receive_character_sheet(_sheet):
	var sheet = _sheet
	
	var ITEMS = MAIN.PREMADE['items']
	
	receive_skills(sheet['skills'],sheet['skill_cooldowns'])
	
	var stats = ch.get_node('RichTextLabel')
	stats.text = ''
	stats.text += '[table=3]'
	for trans in MAIN.PREMADE['translations']:
		if trans in ['hp','mp']:
			continue
		''' HORRIBLE TERRIBLE ITEM COMPARE CODE'''
		var hovered_item_stat_number = 0
		var hovered_item_stat_number_display = ''
		if hovered_item != null:
			var _i = ITEMS[hovered_item]
			if 'slot' in _i:
				if trans in _i['stats']:
					hovered_item_stat_number = int(_i['stats'][trans])
					for e in sheet['equipment']:
						if ITEMS[e]['slot'] == _i['slot']:
							if ITEMS[e] == _i:
								hovered_item_stat_number = int(_i['stats'][trans]) * -1
							else:
								hovered_item_stat_number = int(_i['stats'][trans] - ITEMS[e]['stats'][trans]) 
								
					if hovered_item_stat_number == 0:
						hovered_item_stat_number_display = '[color=gray][/color]' 
					if hovered_item_stat_number > 0:
						hovered_item_stat_number_display = '[color=green]+%s[/color]' % hovered_item_stat_number
					if hovered_item_stat_number < 0:
						hovered_item_stat_number_display = '[color=red]%s[/color]' % hovered_item_stat_number

		var translated_name = MAIN.PREMADE['translations'][trans]
		var stat_number = sheet['stats'][trans]
		stats.text += '[cell]%s: [/cell][cell]%s [/cell][cell]%s[/cell]' % [translated_name, stat_number, hovered_item_stat_number_display]	
		'''OH GOD'''
	stats.text += '[/table]'
	
	inv_text.text = ''
	inv_text.text += '[center]Equipment[/center]\n'
	
	sheet['equipment'].sort()
	sheet['skills'].sort()
	
	

	for i in sheet['equipment']:
		if inv_search.text.to_lower() not in ITEMS[i]['name'].to_lower() and not inv_search.text.to_lower()=='':
			continue
		#inv_text.text += '[cell]%s:   [/cell][cell]%s[/cell]\n' % [ITEMS[i]['slot'].capitalize(), interactable('equipment',i,ITEMS[i]['name'])]
		inv_text.text += '%s\n' % [GAME.interactable('equipment',i,ITEMS[i]['name'])]

	inv_text.text += '[center]Inventory[/center]\n'

	inv_text.text += '[table=2]' 
	var inventory_items_to_sort = []
	var inventory_items_unsorted = {}
	for i in sheet['inventory']:
		if inv_search.text.to_lower() not in ITEMS[i]['name'].to_lower() and not inv_search.text.to_lower()=='':
			continue
	
		var quantity = sheet['inventory'][i]
		if quantity > 1:
			quantity = ' (%s)' % [quantity]
		else:
			quantity = ''
		
		inventory_items_to_sort.append(ITEMS[i]['name'])
		inventory_items_unsorted[ITEMS[i]['name']] = {'id':i,'name':ITEMS[i]['name'],'quantity':quantity,'equipable': 'stats' in ITEMS[i], 'consumable': 'use_script' in ITEMS[i]}
	inventory_items_to_sort.sort()
	
	for item in inventory_items_to_sort:
		if item in inventory_items_unsorted:
			if not inventory_items_unsorted[item]['equipable']: continue
			#print(item,_un['id'])
			inv_text.text += '[cell]%s[/cell][cell]%s[/cell]\n' % [
				GAME.interactable('inventory',
					inventory_items_unsorted[item]['id'],
					inventory_items_unsorted[item]['name']),
					inventory_items_unsorted[item]['quantity']]
	for item in inventory_items_to_sort:
		if item in inventory_items_unsorted:
			if not inventory_items_unsorted[item]['consumable']: continue
			#print(item,_un['id'])
			inv_text.text += '[cell]%s[/cell][cell]%s[/cell]\n' % [
				GAME.interactable('inventory',
					inventory_items_unsorted[item]['id'],
					inventory_items_unsorted[item]['name']),
					inventory_items_unsorted[item]['quantity']]
	for item in inventory_items_to_sort:
		if item in inventory_items_unsorted:
			if inventory_items_unsorted[item]['equipable'] or inventory_items_unsorted[item]['consumable']: continue
			#print(item,_un['id'])
			inv_text.text += '[cell]%s[/cell][cell]%s[/cell]\n' % [
				GAME.interactable('inventory',
					inventory_items_unsorted[item]['id'],
					inventory_items_unsorted[item]['name']),
					inventory_items_unsorted[item]['quantity']]
		
	inv_text.text += '[/table]'
	
func _on_inventory_meta_hover_started(meta):
	var json = JSON.new()
	var data = json.parse_string(meta)
	hovered_item = data['object']
	pass # Replace with function body.

func _on_inventory_meta_hover_ended(meta):
	hovered_item = null
	pass # Replace with function body.
	
func _on_inventory_meta_clicked(meta):
	GAME.interaction(meta)


func _on_button_sheet_button_down():
	state = 'sheet'

func _on_button_inventory_button_down():
	state = 'inventory'


func _on_button_combat_button_down():
	state = 'combat'

func _on_skills_meta_clicked(meta):
	GAME.interaction(meta)


func _on_others_meta_clicked(meta):
	GAME.interaction(meta)


