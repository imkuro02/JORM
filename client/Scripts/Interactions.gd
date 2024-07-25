extends Control
const Packet = preload("res://Scripts/Packet.gd")
@onready var text = $RichTextLabel
@onready var panel = $Panel

func create_interactionsss(data):
	position = get_local_mouse_position() - Vector2(30,10)
	var MAIN = get_tree().root.get_node('Main')
	var ITEMS = MAIN.PREMADE['items']
	text.text = ''
	
	var interactions
	var json = JSON.new()
	data = json.parse_string(data)

	if 'player' in data:
		interactions = ['target','trade','party invite']
		var p: Packet = Packet.new('Target',[data['player']])
		#sheet['target'] = data['player']
		MAIN.send_packet(p)
		
	if 'enemy' in data:
		interactions = ['target']
		var p: Packet = Packet.new('Target',[data['enemy']])
		MAIN.send_packet(p)
		
	if 'exit' in data:
		interactions = ['inspect','go']
		var p: Packet = Packet.new('Go',[data['exit']])
		MAIN.send_packet(p)
		
	if 'inventory' in data:
		for d in data:
			if 'slot' in ITEMS[data[d]]:
				interactions = ['equip','inspect','drop']
			elif 'use_script' in ITEMS[data[d]]:
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
			
func create_interaction(data):
	position = get_local_mouse_position() - Vector2(5,5)
	var MAIN = get_tree().root.get_node('Main')
	var ITEMS = MAIN.PREMADE['items']
	text.text = ''
	
	var interactions
	var json = JSON.new()
	data = json.parse_string(data)

	if 'player' in data:
		interactions = ['target','trade','party invite']
		
	if 'enemy' in data:
		interactions = ['target']
		
	if 'exit' in data:
		interactions = ['go']

	if 'inventory' in data:
		for d in data:
			if 'slot' in ITEMS[data[d]]:
				interactions = ['equip','inspect','drop']
			elif 'use_script' in ITEMS[data[d]]:
				interactions = ['use','inspect','drop']
			else:
				interactions = ['inspect','drop']
		
	if 'equipment' in data:
		interactions = ['unequip','inspect']
		
	if 'loot' in data:
		interactions = ['grab','inspect']
		
	for interaction in interactions:
		for d in data:
			text.text += '[url={"%s":"%s"}][color=yellow]>  %s[/color][/url]\n' % [interaction, data[d], interaction]

func _process(_delta):
	panel.size = text.size

func _on_rich_text_label_meta_clicked(meta):
	var MAIN = get_tree().root.get_node('Main')
	var json = JSON.new()
	var data = json.parse_string(meta)
	var action = null
	var object = null
	
	for d in data:
		object = data[d]
		action = d
		
	var p = null
	match action:
		'go':
			p = Packet.new('Go',[object])
		'equip':
			p = Packet.new('Equip',[object])
		'unequip':
			p = Packet.new('Unequip',[object])
		'target':
			p = Packet.new('Target',[object])
			
	if p != null:
		MAIN.send_packet(p)
		self.queue_free()
	
	
func _on_rich_text_label_mouse_exited():
	self.queue_free()
