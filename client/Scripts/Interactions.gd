extends Control
const Packet = preload("res://Scripts/Packet.gd")
@onready var text = $RichTextLabel
@onready var panel = $Panel

func create_interaction(data, activate_now = false):

	position = get_local_mouse_position() - Vector2(5,5)
	
	var MAIN = get_tree().root.get_node('Main')
	var ITEMS = MAIN.PREMADE['items']
	text.text = ''
	
	var interactions
	var json = JSON.new()
	data = json.parse_string(data)

	if 'player' == data['tag']:
		interactions = ['Target','Trade','Party invite']
		
	if 'enemy' == data['tag']:
		interactions = ['Target']
		
	if 'exit' == data['tag']:
		interactions = ['Go']

	if 'inventory' == data['tag']:
		if 'slot' in ITEMS[data['object']]:
			interactions = ['Equip','Inspect','Drop','Drop all']
		elif 'use_script' in ITEMS[data['object']]:
			interactions = ['Use','Inspect','Drop', 'Drop all']
		else:
			interactions = ['Inspect','Drop', 'Drop all']
		
	if 'equipment' == data['tag']:
		interactions = ['Unequip','Inspect']
		
	if 'loot' == data['tag']:
		interactions = ['Grab','Inspect']
		
	if 'target' == data['tag']:
		interactions = ['Untarget']
		
	if 'skill' == data['tag']:
		interactions = ['Use Skill','Skill Description']
		
	if 'look' == data['tag']:
		activate_now = true
		interactions = ['Look']
	
	if 'self_target' == data['tag']:
		activate_now = true
		interactions = ['Target']
		data['object'] = ''
		
	if 'un_self_target' == data['tag']:
		activate_now = true
		interactions = ['Untarget']
		
	if activate_now:
		var meta = '{"%s":"%s"}' % [interactions[0], data['object']]
		_on_rich_text_label_meta_clicked(meta)

	text.text = ''
	#text.text += '%s\n' % [data['label']]
	for interaction in interactions:
			text.text += '[url={"%s":"%s"}][color=yellow]%s[/color][/url]\n' % [interaction, data['object'], interaction]


func _process(_delta):
	panel.size = text.size + Vector2(16,16)
	panel.position = text.position - Vector2(8,8)

func _input(event):
	if event is InputEventMouseButton:
		await get_tree().create_timer(0.1).timeout
		queue_free()
	
func _on_rich_text_label_meta_clicked(meta):
	var MAIN = get_tree().root.get_node('Main')
	var ITEMS = MAIN.PREMADE['items']
	var SKILLS = MAIN.PREMADE['skills']
	
	var json = JSON.new()
	var data = json.parse_string(meta)
	var action = null
	var object = null
	
	for d in data:
		object = data[d]
		action = d
		
	var p = null
	match action:
		'Look':
			MAIN.chat_window.show_room()
		'Go':
			p = Packet.new('Go',[object])
			MAIN.audio.play('go')
		'Equip':
			p = Packet.new('Equip',[object])
			MAIN.audio.play('equip')
		'Unequip':
			p = Packet.new('Unequip',[object])
			MAIN.audio.play('equip')
		'Drop':
			p = Packet.new('Drop', [object,1])
			MAIN.audio.play('message')
		'Drop all':
			p = Packet.new('Drop', [object,0])
			MAIN.audio.play('message')
		'Target':
			p = Packet.new('Target',[object])
			MAIN.audio.play('message')
		'Self Target':
			p = Packet.new('Target',[object])
			MAIN.audio.play('message')
		'Untarget':
			p = Packet.new('Target',[null])
			MAIN.audio.play('message')
		'Use Skill':
			p = Packet.new('UseSkill',[object])
		'Skill Description':
			var text = ''
			text += '%s\n%s\n' % [SKILLS[object]['name'],SKILLS[object]['description']]
			MAIN.chat_window.receive_simple_message(text)
		'Inspect':
			print('fdsafsda')
			var text = ''
			text += '%s\n%s\n' % [ITEMS[object]['name'],ITEMS[object]['description']]
			'''
			if 'slot' in ITEMS[object]:
				text += '\n.....\n[table=2]'
				var TRANS = MAIN.PREMADE['translations']
				for stat_name in ITEMS[object]['stats']:
					var stat = ITEMS[object]['stats'][stat_name]
					text += '[cell]%s: [/cell][cell]%s [/cell]\n' % [TRANS[stat_name],stat]
				text += '[/table]'
			'''
			MAIN.chat_window.receive_simple_message(text)
			
	if p != null:
		MAIN.send_packet(p)
		
	self.queue_free()
		
func _on_rich_text_label_mouse_exited():
	#self.queue_free()
	pass
