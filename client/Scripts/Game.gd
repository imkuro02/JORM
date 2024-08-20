extends Control

const Packet = preload("res://Scripts/Packet.gd")

@onready var chatbox = $Chatbox/Chatbox
@onready var input = $Chatbox/LineEdit
@onready var commands = $Chatbox/Commands
@onready var settings = $Settings
@onready var others = $RightPanel/VBoxContainer/Others

@onready var skills = $RightPanel/VBoxContainer/Skills
@onready var combat_panel = $CombatPanel/Combat
@onready var background_manager = $BackgroundManager

@onready var character_sheet = $CharacterSheet

var interactions_popup = preload("res://Scenes/Interactions.tscn")

#@onready var tooltip = $CanvasLayer/Tooltip

var sheet
var MAIN 
var ROOM = {}

var autouse_skills = []
var prev_autouse = 0

func _ready():
	commands.text = '%s | %s | %s | %s' % [
		interactable('look',0,'Look'),
		interactable('self_target',0,'Self Target'),
		interactable('un_self_target',0,'Untarget'),
		interactable('clear_chat',0,'Clear')
		]
		
	MAIN = get_tree().root.get_node('Main')
	character_sheet.GAME = self

	
var chat_message_queue = []
var text_appended = false
func chatbox_update():
	if int(MAIN.SERVER_TIME) % 5 == 0:
		if not text_appended:
			if len(chat_message_queue) >= 1:
				chatbox.text += chat_message_queue[0]
				chat_message_queue.pop_at(0)
				text_appended = true
				MAIN.audio.play('message')
	else:
		text_appended = false

func interactive_chatbox_update():
	''' REPLACE ENTITY WITH TARGET AND VICE VERSA CODE'''
	if sheet != null:
		var time = Time.get_ticks_usec()
		var meta_contents = []
		var regex = RegEx.new()
		regex.compile(r"\[url(.*?)\[/url\]")
		var result = regex.search_all(chatbox.text)
		for _match in result:
			var str = '[url' + _match.get_string(1)+ '[/url]'
			meta_contents.append(str) # Get the content between [meta] and [/meta]

		for content in meta_contents:
			if sheet['target'] != null:
				if sheet['target'] in content:
					chatbox.text = chatbox.text.replace(content,interactable('target',sheet['target'],sheet['target']))
				else:
					for enemy in ROOM['enemies']:
						if enemy in content: 
							chatbox.text = chatbox.text.replace(content,interactable('enemy',enemy,enemy))
					for player in ROOM['players']:
						if player in content: 
							chatbox.text = chatbox.text.replace(content,interactable('player',player,player))
							
			if ('"tag":"target"' in content) and (sheet['target'] not in content):
				regex.compile(r"\"label\":\"(.*?)\"")
				var label_result = regex.search_all(content)
				label_result = label_result[0].get_string(1)
				chatbox.text = chatbox.text.replace(content,interactable('enemy',label_result,label_result))
					
		#print(Time.get_ticks_usec() - time)
		
	''' REPLACE ENTITY WITH TARGET AND VICE VERSA CODE'''

func chatbox_trim_update():
	if len(chatbox.text) >= 30_000:
		chatbox.text = chatbox.text.substr(1_000, chatbox.text.length() - 1_000)

func refresh_players():
	others.text = ''
	
	if ROOM == null:
		return
		
	if sheet == null:
		return
		
	#others.text += 'Players:\n'
	for player in ROOM['players']:
		var character = ROOM['players'][player]
		var id = player
		var name = player
		var hp = character['stats']['hp']
		var max_hp = character['stats']['max_hp']
		if sheet['target'] == id:
			others.text += interactable('target',id,name)
		else:
			others.text += interactable('player',id,name)
		others.text += '\n'
		#others.text += ''' [color=red] %s%%[/color]\n''' % [int((hp/max_hp)*100)]
	
	#others.text += 'Enemies:\n'
	for enemy in ROOM['enemies']:
		var character = ROOM['enemies'][enemy]
		var id = enemy
		var name = enemy
		var hp = character['stats']['hp']
		var max_hp = character['stats']['max_hp']
		if sheet['target'] == id:
			others.text += interactable('target',id,name)
		else:
			others.text += interactable('enemy',id,name)
		others.text += '\n'
		#others.text += ''' [color=red] %s%%[/color]\n''' % [int((hp/max_hp)*100)]
		
	

func _process(_delta):
	# print server time delay
	settings.get_node('Delay').text = 'tick: %s' % [int(MAIN.SERVER_TIME)]
	
	refresh_players()
	chatbox_trim_update()
	chatbox_update()
	# currently borked, not sure if worth fixing
	# it crashes when sheet['target'] is null, cuz then u cant look up if its in the content or not
	#interactive_chatbox_update()
	
	

func interaction(data):
	var w = interactions_popup.instantiate()
	add_child(w)
	w.create_interaction(data, Input.is_key_pressed(KEY_CTRL))

func receive_simple_message(text: String):
	MAIN.audio.play('message')
	chatbox.text += '%s\n' % [text]
	

func receive_chat(sender: String, text: String):
	MAIN.audio.play('message')
	var msg = '%s Says %s\n' % [interactable('player',sender,sender),text]
	chatbox.text += msg

func receive_flavoured_message(text):
	var time = Time.get_ticks_usec()
	var _players = ROOM['players']
	var _enemies = ROOM['enemies']
	var _skills  = MAIN.PREMADE['skills']
	var _items   = MAIN.PREMADE['items']
	var _exits   = ROOM['exits']
	
	# Define the pattern types
	text = ' '+text+' '
	var patterns = [
		{'type': 'loot', 'data': _items},
		{'type': 'enemy', 'data': _enemies},
		{'type': 'player', 'data': _players},
		{'type': 'skill', 'data': _skills}
	]
	var acceptable_fixes = [',','.','\n',' ','?','!']
	for pattern in patterns:
		for key in pattern['data']:
			for fix in acceptable_fixes:
				text = text.replace(
					''+pattern['data'][key]['name']+fix,
					''+interactable(pattern['type'],key,pattern['data'][key]['name'])+fix)
			
	# exits dont have a names field
	for i in _exits:
		for fix in acceptable_fixes:
			text = text.replace(''+i+fix, ''+interactable('exit', i, i )+fix)
	
	text = text.strip_edges(true, false)
	text = text + '\n'
	text = text.strip_edges(true, false)
	chat_message_queue.append(text)
	#print(Time.get_ticks_usec() - time)

	
	
func interactable(tag, object, label):
	var col = 'white'

	var color_to_tags = {
		'player': 'aqua',
		'enemy': 'coral',
		'inventory': 'LIGHT_STEEL_BLUE',
		'equipment': 'LIGHT_STEEL_BLUE',
		'target': 'RED',
		'exit': 'green',
		'skill': 'LIGHT_GOLDENROD',
		'loot': 'GOLDENROD',
		'clear_chat': 'yellow',
		'look': 'yellow',
		'self_target': 'yellow',
		'un_self_target': 'yellow'
	}
	if tag in color_to_tags:
		col = color_to_tags[tag]
		
	var x = '[url={"tag":"%s","object":"%s","label":"%s"}][color="%s"]%s[/color][/url]' % [tag, object, label, col, label]
	return x
	

		
func receive_room(room):
		
	if 'name' not in ROOM:
		#chatbox.text = ''
		ROOM = room
		show_room(true)
		return
		
	if ROOM['name'] != room['name']:
		#chatbox.text = ''
		ROOM = room
		show_room(true)
		return
		
	ROOM = room
		
	return

func receive_character_sheet(_sheet):
	character_sheet.receive_character_sheet(_sheet)

	var SKILLS = MAIN.PREMADE['skills']

	sheet = _sheet
	
	combat_panel.get_node("Self").set_sheet(sheet)

	#print(sheet['target'])
	if sheet['target'] == null:
		combat_panel.get_node("Target").set_sheet(null)
	if sheet['target'] in ROOM['players']:
		var target_sheet = ROOM['players'][sheet['target']]
		combat_panel.get_node("Target").set_sheet(target_sheet)
	elif sheet['target'] in ROOM['enemies']:
		var target_sheet = ROOM['enemies'][sheet['target']]
		combat_panel.get_node("Target").set_sheet(target_sheet)

	
	''' SKILLS '''
	skills.text = '[table=4]'
	for skill in sheet['skills']:
		var cooldown = ''
		var autouse = ''

		if skill in sheet['skill_cooldowns']:
			cooldown = '(%ss)' % [int(abs(MAIN.SERVER_TIME - sheet['skill_cooldowns'][skill])/30)+1]
			
		if skill in autouse_skills:
			autouse = '(Auto)'
		skills.text += '[cell]%s [/cell][cell][color="aqua"]%s [/color][/cell][cell] %s[/cell][cell]%s[/cell] \n' % [
			interactable('skill',skill,SKILLS[skill]['name']),
			SKILLS[skill]['mp_cost'],
			cooldown,
			autouse
		]
	skills.text += '[/table]'
	
	''' AutoUse '''
	for skill in autouse_skills:
		if skill not in sheet['skills']:
			autouse_skills.erase(skill)
	
	if $RightPanel/VBoxContainer/AutoUse.button_pressed == true:
		for skill in autouse_skills:
			if prev_autouse < MAIN.SERVER_TIME - 30:
				if skill not in sheet['skill_cooldowns']:
					var p = Packet.new('UseSkill',[skill])
					MAIN.send_packet(p)
				
	if prev_autouse < MAIN.SERVER_TIME - 30:
		prev_autouse = MAIN.SERVER_TIME
	''' AutoUse '''
	''' SKILLS '''
	
func show_room(clear = false):
	if clear: 
		chatbox.text = '[bgcolor="black"]'
		
	background_manager.new_room(ROOM['name'])
	var exits = ROOM['exits']
	var label = '[center][color="GOLD"]%s[/color][/center]\n' % [ROOM['name']]
	var desc = ROOM['description']
	desc = label + desc + '\n'
	#receive_flavoured_message(desc)
	'''
	for exit in exits:
		desc += 'Go to: ' + interactable('exit',exit,exit) + '\n'

	for player in ROOM['players']:
		desc += interactable('player',player,player)+'\n'
		
	for enemy in ROOM['enemies']:
		desc += interactable('enemy',enemy,enemy)+'\n'
		
	desc += 'Is here..\n'
	'''
	for exit in ROOM['exits']:
		desc += '[' + interactable('exit',exit,exit) + '] '
	desc += '\n'
	chatbox.text += desc
	
func send(text: String):
	if len(text) > 0:
		var p: Packet = Packet.new('Chat',[text])
		MAIN.send_packet(p)
		input.text = ""
		
func _input(event: InputEvent):
	if event is InputEventKey and event.pressed:
		match event.keycode:
			KEY_ENTER:
				if input.text == 'ROOM':
					print(ROOM)
					return
				if input.text == 'SELF':
					print(sheet)
					return
				send(input.text)
				input.text = ""
				input.grab_focus()
			KEY_ESCAPE:
				input.release_focus()

func _on_logout_pressed():
	var p: Packet = Packet.new('Disconnect')
	MAIN.send_packet(p)

func _on_chatbox_meta_clicked(meta):
	interaction(meta)

func _on_others_meta_clicked(meta):
	interaction(meta)
	
func _on_font_size_value_changed(value):
	MAIN.theme.default_font_size = int(value)

func _on_audio_volume_value_changed(value):
	MAIN.audio.set_volume(value)


