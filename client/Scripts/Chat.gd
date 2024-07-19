extends Control

const Packet = preload("res://Scripts/Packet.gd")

@onready var chatbox = $CanvasLayer/Chatbox/Chatbox
@onready var input = $CanvasLayer/Chatbox/LineEdit

@onready var ch = $CanvasLayer/CharacterSheet
@onready var inv = $CanvasLayer/Inventory

@onready var logout = $Logout
var draggable_ui_chat = preload("res://Scenes/DraggableUI.tscn")

var MAIN 
var ROOM = {}

func _ready():
	var w
	w = draggable_ui_chat.instantiate()
	add_child(w)
	$CanvasLayer/Chatbox.reparent(w.get_node('Panel/Item/PanelContainer'))
	
	w = draggable_ui_chat.instantiate()
	add_child(w)
	ch.reparent(w.get_node('Panel/Item/PanelContainer'))
	
	w = draggable_ui_chat.instantiate()
	inv.reparent(w.get_node('Panel/Item/PanelContainer'))
	add_child(w)
	
	MAIN = get_tree().root.get_node('Main')
	
func interaction(data):
	var interactions
	var json = JSON.new()
	data = json.parse_string(data)
	#if error == OK:
	#	print(json.data)

	if 'player' in data:
		interactions = ['inspect','trade','party invite']
		
	if 'exit' in data:
		interactions = ['inspect','go']
		var p: Packet = Packet.new('Go',[data['exit']])
		MAIN.send_packet(p)
		
	if 'inventory' in data:
		for d in data:
			if 'slot' in MAIN.PREMADE[data[d]]:
				interactions = ['equip','inspect','drop']
			elif 'use_script' in MAIN.PREMADE[data[d]]:
				interactions = ['use','inspect','drop']
			else:
				interactions = ['inspect','drop']
				
			var p: Packet = Packet.new('Equip',[data[d]])
			MAIN.send_packet(p)
		
	if 'equipment' in data:
		interactions = ['unequip','inspect']
		for d in data:
			var p: Packet = Packet.new('Unequip',[data[d]])
			MAIN.send_packet(p)
		
	if 'loot' in data:
		interactions = ['grab','inspect']
		
	for d in data:
		print('%s: %s interactions: %s' % [data,data[d],interactions])
		
func receive_simple_message(text: String):
	chatbox.text += '%s\n' % [text]
	
func receive_chat(sender: String, text: String):
	chatbox.text += '[url={"player":"%s"}][color="#4287f5"]%s[/color][/url]: %s\n' % [sender,sender,text]
	
func receive_room(room):
	if 'name' not in ROOM:
		chatbox.text = ''
		ROOM = room
		show_room()

		return
		
	if ROOM['name'] != room['name']:
		chatbox.text = ''
		ROOM = room
		show_room()
		
		return
		
	return
		
func receive_character_sheet(sheet):
	
	
	ch.text = ''
	ch.text += '[center] %s\'s Character Sheet[/center]\n\n' % [sheet['name']]
	ch.text += '''
	[table=4]
	[cell]HP [/cell][cell]%s/%s[/cell]
	[cell]MP [/cell][cell]%s/%s[/cell]
	
	[cell]EXP[/cell][cell]%s[/cell]
	[cell]SP[/cell][cell]%s[/cell]

	[cell]CRT [/cell][cell]%s[/cell]
	[cell]AVD [/cell][cell]%s[/cell]
	[cell]PAC [/cell][cell]%s[/cell]
	[cell]MAC [/cell][cell]%s[/cell]

	[cell]STR [/cell][cell]%s[/cell]
	[cell]DEX [/cell][cell]%s[/cell]
	[cell]CON [/cell][cell]%s[/cell]
	[cell]INT [/cell][cell]%s[/cell]
	[cell]WIS [/cell][cell]%s[/cell]
	[cell]CHA [/cell][cell]%s[/cell]
	[/table]
	''' % [
		sheet['stats']['hp'],
		sheet['stats']['max_hp'],
		sheet['stats']['mp'],
		sheet['stats']['max_mp'],
		
		sheet['stats']['exp'],
		sheet['stats']['points'],
		
		sheet['stats']['crt'],
		sheet['stats']['avd'],
		sheet['stats']['pac'],
		sheet['stats']['mac'],
		
		sheet['stats']['str'],
		sheet['stats']['dex'],
		sheet['stats']['con'],
		sheet['stats']['int'],
		sheet['stats']['wis'],
		sheet['stats']['cha']
	]
	inv.text = ''
	inv.text += '[center]Equipment[/center]\n'
	inv.text += '[table=1]'
	for i in sheet['equipment']:
		#ch.text += '[cell]%s:[/cell][cell][url={"equipment":"%s"}]%s[/url][/cell]\n' % [MAIN.PREMADE[i]['slot'],i,MAIN.PREMADE[i]['name']]
		inv.text += '[cell][url={"equipment":"%s"}]%s[/url][/cell]\n' % [i,MAIN.PREMADE[i]['name']]
	inv.text += '[/table]'
	
	inv.text += '[center]Inventory[/center]\n'
	inv.text += '[table=2]'
	for i in sheet['inventory']:
		inv.text += '[cell][url={"inventory":"%s"}]%s    [/url][/cell][cell]x%s[/cell]\n' % [i,MAIN.PREMADE[i]['name'],sheet['inventory'][i]]
	inv.text += '[/table]'
	pass
	
func show_room():
	var exits = ROOM['exits']
	chatbox.text += '[center]~~~ %s ~~~[/center]\n\n' % [ROOM['name']]
	chatbox.text += '%s\n\n' % [ROOM['description']]
	chatbox.text += 'Exits:\n'
	for e in exits:
		chatbox.text += '          [url={"exit":"%s"}]%s[/url]\n' % [e,e]
	chatbox.text += '\n\n'
	
func send(text: String):
	if text.split(' ')[0] == 'look':
		show_room()
		return
		
	if len(text) > 0:
		var p: Packet = Packet.new('Chat',[text])
		MAIN.send_packet(p)
		input.text = ""
		
func _input(event: InputEvent):
	if event is InputEventKey and event.pressed:
		match event.keycode:
			KEY_ENTER:
				send(input.text)
				input.text = ""
				input.grab_focus()
			KEY_ESCAPE:
				input.release_focus()

func _on_logout_pressed():
	var p: Packet = Packet.new('Disconnect')
	MAIN.send_packet(p)




func _on_character_sheet_meta_clicked(meta):
	interaction(meta)

func _on_inventory_meta_clicked(meta):
	interaction(meta)

func _on_chatbox_meta_clicked(meta):
	interaction(meta)
