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
			interactions = ['Consume','Inspect','Drop', 'Drop all']
		else:
			interactions = ['Inspect','Drop', 'Drop all']
		
	if 'equipment' == data['tag']:
		interactions = ['Unequip','Inspect']
		
	if 'loot' == data['tag']:
		interactions = ['Inspect']
		
	if 'target' == data['tag']:
		interactions = ['Untarget']
		
	if 'skill' == data['tag']:
		interactions = ['Use Skill','Skill Description']
		
	if 'clear_chat' == data['tag']:
		activate_now = true
		interactions = ['Clear']
	
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
		'Clear':
			#MAIN.chat_window.chatbox.text = ''
			MAIN.chat_window.chatbox_clear()
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
		'Consume':
			p = Packet.new('UseItem',[object])
		'Skill Description':
			var text = ''
			text += '%s\n%s\n' % [SKILLS[object]['name'],SKILLS[object]['description']]
			MAIN.chat_window.receive_flavoured_message(text)
		'Inspect':
			print('fdsafsda')
			var text = ''
			text += '%s\n%s\n' % [ITEMS[object]['name'],ITEMS[object]['description']]

			var _sheet = MAIN.chat_window.sheet
			var _equipment = _sheet['equipment']
			
			if 'slot' in ITEMS[object]:
				var TRANS = MAIN.PREMADE['translations']
				#text += '[table=3]'
				text += '[table=5]'

				for stat_name in ITEMS[object]['stats']:
					var self_compare = false
					var _current_stat = _sheet['stats'][stat_name] 
					var _item_stat = ITEMS[object]['stats'][stat_name]
					var _equiped_stat = 0
				
					var _original_stat = _current_stat - _equiped_stat
					var _new_stat = _original_stat + _item_stat
					for e in _sheet['equipment']:
						if ITEMS[e]['slot'] == ITEMS[object]['slot']:
							_equiped_stat = ITEMS[e]['stats'][stat_name]
							_original_stat = _current_stat - _equiped_stat
							_new_stat = _original_stat + _item_stat
							if e == object:
								_new_stat = _original_stat 
								


					
					
					
					if (_original_stat + _item_stat == _original_stat + _equiped_stat) and _item_stat == 0:
						continue

					if _new_stat > _original_stat + _equiped_stat:
						_new_stat = '[color=green]%s[/color]'%[_new_stat]
					else:
						_new_stat = '[color=red]%s[/color]'%[_new_stat]
					text += '[cell]%s [/cell][cell]%s [/cell][cell]-> [/cell][cell]%s [/cell][cell](%s)[/cell]' %[
						TRANS[stat_name],
						_original_stat + _equiped_stat,
						_new_stat,
						_item_stat
					]


						
				text += '[/table]'
				
					
				
		
			MAIN.chat_window.receive_flavoured_message(text)
			
	if p != null:
		MAIN.send_packet(p)
		
	self.queue_free()
		
func _on_rich_text_label_mouse_exited():
	#self.queue_free()
	pass
