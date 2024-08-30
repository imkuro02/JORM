extends Control
const Packet = preload("res://Scripts/Packet.gd")
@onready var text = $RichTextLabel
@onready var panel = $Panel

var PREMADE
var MAIN

func _ready():
	MAIN = get_tree().root.get_node('Main')
	PREMADE = MAIN.PREMADE
	
func create_interaction(data, activate_now = false):

	position = get_local_mouse_position() - Vector2(5,5)
	
	var ITEMS = PREMADE['items']
	text.text = ''
	
	var interactions
	
	var json = JSON.new()
	data = json.parse_string(data)

	if 'player' == data['tag']:
		interactions = ['Target','Trade','Party invite','Inspect']
		
	if 'enemy' == data['tag']:
		interactions = ['Target','Inspect']
		
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
		if data['object'] in MAIN.ROOM['enemies']:
			data['tag'] = 'enemy'
			interactions = ['Untarget', 'Inspect']
		if data['object'] in MAIN.ROOM['players']:
			data['tag'] = 'player'
			interactions = ['Untarget','Trade','Party invite','Inspect']
		
	if 'skill' == data['tag']:
		interactions = ['Use Skill','Skill Description']
		
	if 'status' == data['tag']:
		interactions = ['Inspect']
		
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
		data['interaction'] = interactions[0]
		var meta = '%s' % [data]
		_on_rich_text_label_meta_clicked(meta)

	text.text = ''
	#text.text += '%s\n' % [data['label']]
	
	for interaction in interactions:
			data['interaction'] = interaction
			text.text += '[url=%s][color=yellow]%s[/color][/url]\n' % [data, interaction]


func _process(_delta):
	panel.size = text.size + Vector2(16,16)
	panel.position = text.position - Vector2(8,8)

func _input(event):
	if event is InputEventMouseButton:
		await get_tree().create_timer(0.1).timeout
		queue_free()
		print(event)
	
func _on_rich_text_label_meta_clicked(meta):
	var MAIN = get_tree().root.get_node('Main')
	var ITEMS = MAIN.PREMADE['items']
	var SKILLS = MAIN.PREMADE['skills']
	var STATUSES = MAIN.PREMADE['statuses']
	
	var json = JSON.new()
	var data = json.parse_string(meta)
	var action = null
	var object = null
	
	print(data)

		
	var p = null
	match data['interaction']:
		'Clear':
			#MAIN.chat_window.chatbox.text = ''
			MAIN.chat_window.chatbox_clear()
		'Go':
			p = Packet.new('Go',[data['object']])
			
		'Equip':
			p = Packet.new('Equip',[data['object']])
			MAIN.audio.play('equip')
		'Unequip':
			p = Packet.new('Unequip',[data['object']])
			MAIN.audio.play('equip')
		'Drop':
			p = Packet.new('Drop', [data['object'],1])
			MAIN.audio.play('message')
		'Drop all':
			p = Packet.new('Drop', [data['object'],0])
			MAIN.audio.play('message')
		'Target':
			p = Packet.new('Target',[data['object']])
			MAIN.audio.play('message')
		'Self Target':
			p = Packet.new('Target',[data['object']])
			MAIN.audio.play('message')
		'Untarget':
			p = Packet.new('Target',[null])
			MAIN.audio.play('message')
		'Use Skill':
			p = Packet.new('UseSkill',[data['object']])
		'Consume':
			p = Packet.new('UseItem',[data['object']])
		'Inspect':
			var text = ''
			match data['tag']:
				'inventory', 'equipment', 'loot':
					text += '%s\n%s' % [ITEMS[data['object']]['name'],ITEMS[data['object']]['description']]
					var _sheet = MAIN.CHARACTERSHEET
					var _equipment = _sheet['equipment']
					
					if 'slot' in ITEMS[data['object']]:
						text += '\n'
						var TRANS = MAIN.PREMADE['translations']
						#text += '[table=3]'
						text += '[table=5]'

						for stat_name in ITEMS[data['object']]['stats']:
							var self_compare = false
							var _current_stat = _sheet['stats'][stat_name] 
							var _item_stat = ITEMS[data['object']]['stats'][stat_name]
							var _equiped_stat = 0
						
							var _original_stat = _current_stat - _equiped_stat
							var _new_stat = _original_stat + _item_stat
							for e in _sheet['equipment']:
								if ITEMS[e]['slot'] == ITEMS[data['object']]['slot']:
									_equiped_stat = ITEMS[e]['stats'][stat_name]
									_original_stat = _current_stat - _equiped_stat
									_new_stat = _original_stat + _item_stat
									if e == data['object']:
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
				'player':
					var players = MAIN.ROOM['players']
					if data['object'] not in players:
						text = 'This player is not here.'
					else:
						text = 'Another player, they are wearing: '
						var equipment = players[data['object']]['equipment']
						if len(equipment) == 0:
							text += 'Nothing... they are BUCK NAKED!'
						else:

							for item in equipment:
								text += '%s, ' % [ITEMS[item]['name']]

							text = text.substr(0, text.length() - 2) + "."
					#var player_name = object['']
					#var ROOM = MAIN.ROOM['players'][object['name']]
				'enemy':
					var ROOM = MAIN.ROOM
					var enemy_name = data['object']
					var enemy_id = null
					for enemy in ROOM['enemies']:
						if ROOM['enemies'][enemy]['name'] == enemy_name:
							enemy_id = ROOM['enemies'][enemy]['id']
					if enemy_id == null:
						text = 'That enemy is not here.'
					else:
						text = '%s' % [PREMADE['enemies'][enemy_id]['description']]
					
				'status':
					text = '%s' % [PREMADE['statuses'][data['object']]['description']]
				
			if text == '':
				text = 'Something went wrong with action Inspect:\n%s\n' % [data]
				
			MAIN.chat_window.receive_flavoured_message(text)
			
	if p != null:
		MAIN.send_packet(p)
		
	self.queue_free()
		
func _on_rich_text_label_mouse_exited():
	#self.queue_free()
	pass
