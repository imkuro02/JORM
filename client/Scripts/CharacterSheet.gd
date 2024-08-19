extends Panel

@onready var ch = $VSplitContainer/CharacterSheet
@onready var inv = $VSplitContainer/Inventory
@onready var inv_text = inv.get_node('Inventory')
@onready var inv_search = inv.get_node('LineEdit')

var MAIN
var hovered_item = null
var GAME

func _ready():
	MAIN = get_tree().root.get_node('Main')

func receive_character_sheet(_sheet):
	var sheet = _sheet
	
	var ITEMS = MAIN.PREMADE['items']
	var SKILLS = MAIN.PREMADE['skills']
	
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
