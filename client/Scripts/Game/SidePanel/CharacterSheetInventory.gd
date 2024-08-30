extends VBoxContainer

var MAIN
@export var GAME: Control
@onready var inventory = get_node('RichTextLabel')
@onready var search = get_node('LineEdit')
# Called when the node enters the scene tree for the first time.
func _ready():
	MAIN = get_tree().root.get_node('Main')
	inventory.meta_clicked.connect(meta_clicked)
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	var sheet = MAIN.CHARACTERSHEET
	var ITEMS = MAIN.PREMADE['items']
	
	if sheet == null:
		return
	if ITEMS == null:
		return
	inventory.text = ''
	inventory.text += '[center]Equipment[/center]\n'
	
	sheet['equipment'].sort()
	sheet['skills'].sort()
	
	

	for i in sheet['equipment']:
		if i.to_lower() not in ITEMS[i]['name'].to_lower() and not search.text.to_lower() == '':
			continue
		#inv_text.text += '[cell]%s:   [/cell][cell]%s[/cell]\n' % [ITEMS[i]['slot'].capitalize(), interactable('equipment',i,ITEMS[i]['name'])]
		inventory.text += '%s\n' % [GAME.interactable('equipment',i,ITEMS[i]['name'])]

	inventory.text += '[center]Inventory[/center]\n'

	inventory.text += '[table=2]' 
	var inventory_items_to_sort = []
	var inventory_items_unsorted = {}
	for i in sheet['inventory']:
		if i.to_lower() not in ITEMS[i]['name'].to_lower() and not search.text.to_lower() == '':
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
			inventory.text += '[cell]%s[/cell][cell]%s[/cell]\n' % [
				GAME.interactable('inventory',
					inventory_items_unsorted[item]['id'],
					inventory_items_unsorted[item]['name']),
					inventory_items_unsorted[item]['quantity']]
	for item in inventory_items_to_sort:
		if item in inventory_items_unsorted:
			if not inventory_items_unsorted[item]['consumable']: continue
			#print(item,_un['id'])
			inventory.text += '[cell]%s[/cell][cell]%s[/cell]\n' % [
				GAME.interactable('inventory',
					inventory_items_unsorted[item]['id'],
					inventory_items_unsorted[item]['name']),
					inventory_items_unsorted[item]['quantity']]
	for item in inventory_items_to_sort:
		if item in inventory_items_unsorted:
			if inventory_items_unsorted[item]['equipable'] or inventory_items_unsorted[item]['consumable']: continue
			#print(item,_un['id'])
			inventory.text += '[cell]%s[/cell][cell]%s[/cell]\n' % [
				GAME.interactable('inventory',
					inventory_items_unsorted[item]['id'],
					inventory_items_unsorted[item]['name']),
					inventory_items_unsorted[item]['quantity']]
		
	inventory.text += '[/table]'


func meta_clicked(meta):
	GAME.interaction(meta)
