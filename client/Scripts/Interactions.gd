extends Control
const Packet = preload("res://Scripts/Packet.gd")
@onready var text = $RichTextLabel
@onready var panel = $Panel

func create_interaction(data):
	position = get_local_mouse_position() - Vector2(5,5)
	var MAIN = get_tree().root.get_node('Main')
	var ITEMS = MAIN.PREMADE['items']
	text.text = ''
	
	var interactions
	var json = JSON.new()
	data = json.parse_string(data)

	if 'player' in data['tag']:
		interactions = ['Target','Trade','Party invite']
		
	if 'enemy' in data['tag']:
		interactions = ['Target']
		
	if 'exit' in data['tag']:
		interactions = ['Go']

	if 'inventory' in data['tag']:
		if 'slot' in ITEMS[data['object']]:
			interactions = ['Equip','Inspect','Drop','Drop all']
		elif 'use_script' in ITEMS[data['object']]:
			interactions = ['Use','inspect','drop', 'Drop all']
		else:
			interactions = ['Inspect','Drop', 'Drop all']
		
	if 'equipment' in data['tag']:
		interactions = ['Unequip','Inspect']
		
	if 'loot' in data['tag']:
		interactions = ['Grab','Inspect']
		
	if 'target' in data['tag']:
		interactions = []
		
	for interaction in interactions:
			text.text += '[url={"%s":"%s"}][color=yellow]>  %s[/color][/url]\n' % [interaction, data['object'], interaction]

func _process(_delta):
	panel.size = text.size

func _on_rich_text_label_meta_clicked(meta):
	var MAIN = get_tree().root.get_node('Main')
	var ITEMS = MAIN.PREMADE['items']
	
	var json = JSON.new()
	var data = json.parse_string(meta)
	var action = null
	var object = null
	
	for d in data:
		object = data[d]
		action = d
		
	var p = null
	match action:
		'Go':
			p = Packet.new('Go',[object])
		'Equip':
			p = Packet.new('Equip',[object])
		'Unequip':
			p = Packet.new('Unequip',[object])
		'Drop':
			p = Packet.new('Drop', [object,1])
		'Drop all':
			p = Packet.new('Drop', [object,0])
		'Target':
			p = Packet.new('Target',[object])
		'Inspect':
			var text = ''
			text += '%s\n%s' % [ITEMS[object]['name'],ITEMS[object]['description']]
			MAIN.chat_window.receive_simple_message(text)
			
	if p != null:
		MAIN.send_packet(p)
		
	self.queue_free()
		
func _on_rich_text_label_mouse_exited():
	self.queue_free()
