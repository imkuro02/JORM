extends Control

const Packet = preload("res://Scripts/Packet.gd")

#@onready var chatbox_container = $Chatbox/ChatboxContainer
@onready var chatbox = $Chatbox/ScrollContainer/VBoxContainer/Chatbox
@onready var input = $Chatbox/LineEdit
@onready var commands = $Chatbox/Commands
@onready var settings = $Panel2/VBoxContainer/States/Settings

#@onready var combat_panel = $CombatPanel/Combat
@onready var background_manager = $BackgroundManager

#@onready var character_sheet = $CharacterSheet

var interactions_popup = preload("res://Scenes/Interactions.tscn")

#@onready var tooltip = $CanvasLayer/Tooltip

var sheet
var MAIN 


var color_to_tags = {
		'player_self': 'AQUA',
		'player': 'AQUAMARINE',
		'enemy': 'coral',
		'npc': 'orange',
		'npc_dialog': 'SANDY_BROWN',
		'inventory': 'LIGHT_BLUE',
		'equipment': 'LIGHT_BLUE',
		'target': 'RED',
		'exit': 'green',
		'skill': 'LIGHT_GOLDENROD',
		'status': 'LIGHT_GREEN',
		'loot': 'LIGHT_BLUE',
		'clear_chat': 'yellow',
		'self_target': 'yellow',
		'un_self_target': 'yellow'
	}

func _ready():
	commands.text = '%s | %s | %s' % [
		interactable('self_target',0,'Self Target'),
		interactable('un_self_target',0,'Untarget'),
		interactable('clear_chat',0,'Clear')
		]
		
	MAIN = get_tree().root.get_node('Main')
	#character_sheet.GAME = self
	chatbox_clear()

	
var chat_message_queue = []
var text_appended = false

func chatbox_clear():
	var empty = ''
	chatbox.text = empty
	
var prev_scroll_value = 0
func chatbox_update():
	# autooscroll only if at bottom already
	#var scrollbar = chatbox.get_v_scroll_bar()
	#if scrollbar.visible:
	#	chatbox.scroll_following = scrollbar.value == abs(scrollbar.size.y - scrollbar.max_value)
		
	var scrollbar = $Chatbox/ScrollContainer.get_v_scroll_bar()
	if scrollbar.visible:
		if scrollbar.value == prev_scroll_value or prev_scroll_value == 0:
			scrollbar.value = scrollbar.max_value
			
		prev_scroll_value = abs(scrollbar.size.y - scrollbar.max_value)
	else:
		prev_scroll_value = 0

		
	
	#var scrollbar = chatbox_container.get_v_scroll_bar()
	#if scrollbar.value < scrollbar.max_value:
	#		scrollbar.value = scrollbar.max_value
		
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
	var ROOM = MAIN.ROOM
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

func _process(_delta):
	# print server time delay
	settings.get_node('Delay').text = 'tick: %s' % [int(MAIN.SERVER_TIME)]
	
	chatbox_trim_update()
	chatbox_update()

	# currently borked, not sure if worth fixing
	# it crashes when sheet['target'] is null, cuz then u cant look up if its in the content or not
	#interactive_chatbox_update()
	
	

func interaction(data):
	var w = interactions_popup.instantiate()
	add_child(w)
	w.create_interaction(data, Input.is_key_pressed(KEY_CTRL))

func receive_npc_dialog(npc_name, text, responses):
	receive_flavoured_message('%s says: %s' % [npc_name,text])
	if responses == null:
		return
		
	chatbox.text += '[table=2]'

	for r in len(responses):
		var response = npc_interactable(npc_name, responses[r]['next'],responses[r]['text'])
		print(response)
		if r == 0:
			chatbox.text += '[cell]%s[/cell][cell]%s[/cell]' % [' ', str(r+1) + ').' + response]
		else:
			chatbox.text += '[cell]%s[/cell][cell]%s[/cell]' % [' ', str(r+1) + ').' + response]
	chatbox.text += '[/table]\n'

func flavour_text(text):
	var ROOM = MAIN.ROOM
	var time = Time.get_ticks_usec()
	var _players = ROOM['players']
	var _enemies = ROOM['enemies']
	var _skills  = MAIN.PREMADE['skills']
	var _items   = MAIN.PREMADE['items']
	var _statuses   = MAIN.PREMADE['statuses']
	var _exits   = ROOM['exits']
	var _npcs = ROOM['npcs']
	
	# Define the pattern types
	text = ' '+text+' '
	var patterns = [
		{'type': 'player', 'data': _players},
		{'type': 'loot', 'data': _items},
		{'type': 'enemy', 'data': _enemies},
		{'type': 'skill', 'data': _skills},
		{'type': 'status', 'data': _statuses},
		{'type': 'npc', 'data': _npcs}
	]
	var acceptable_fixes = [',','.','\n',' ','?','!','s']
	for pattern in patterns:
		for key in pattern['data']:
			for fix in acceptable_fixes:
				text = text.replace(
					''+pattern['data'][key]['name']+fix,
					''+interactable(pattern['type'],key,pattern['data'][key]['name'])+fix)
			
	# exits dont have a names field
	#for i in _exits:
	#	for fix in acceptable_fixes:
	#		text = text.replace(''+i+fix, ''+interactable('exit', i, i )+fix)
	
	text = text.strip_edges(true, false)
	
	text = text.strip_edges(true, false)
	
	return text
	
func receive_flavoured_message(text,anim = null):
	var ROOM = MAIN.ROOM
	print(anim)
	if anim != null:
		match anim:
			'death': 
				#$CanvasLayer/OverlayShader.material.set_shader_parameter("intensity", 1)
				MAIN.audio.play('church_bell')
				$CanvasLayer/OverlayShader/AnimationPlayer.play("death")
			'drink':
				MAIN.audio.play('consume_drink')
			'new_room':
				if not $CanvasLayer/OverlayShader/AnimationPlayer.is_playing():
					#text = '[color="silver"]%s[/color]' % [text]
					$AnimationPlayer.play('fade')
					MAIN.audio.play('go')
	else:
		MAIN.audio.play('message')
			
	text = '> ' + flavour_text(text) 
	text = text + '\n'
	chatbox.text += text
	
	#print(Time.get_ticks_usec() - time)

	
func create_interaction_meta(tag, object, label):
	return {"tag": tag, "object": object, "label": label}

func color_interactable(tag):
	var col = 'PINK'
	if tag in color_to_tags:
		col = color_to_tags[tag]
	return col
func npc_interactable(npc_name, next, player_says):
	var npc_meta = {'tag': 'npc_dialog', 'npc': npc_name, 'next': next, 'player_says': player_says}
	var col = color_interactable(npc_meta['tag'])
	var url = '[url=%s][color="%s"] %s [/color][/url]' % [npc_meta, col, flavour_text(player_says)]
	return url
		
func interactable(tag, object, label):

	var col = color_interactable(tag)
		
	if MAIN != null:
		if MAIN.CHARACTERSHEET != null:
			if object == MAIN.CHARACTERSHEET['name'] and tag in ' player ':
				col = color_to_tags['player_self']
		
	
	var interaction_meta = create_interaction_meta(tag, object, label) 
	var url = '[url=%s][color="%s"]%s[/color][/url]' % [interaction_meta, col, label]
	return url
	
func send(text: String):
	if len(text) > 0:
		var p: Packet = Packet.new('Chat',[text])
		MAIN.send_packet(p)
		if text == 'ROOM': print(MAIN.ROOM)
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

func _on_chatbox_meta_clicked(meta):
	interaction(meta)

func _on_font_size_value_changed(value):
	MAIN.theme.default_font_size = int(value)

func _on_audio_volume_value_changed(value):
	MAIN.audio.set_volume(value)

func _on_room_meta_clicked(meta):
	interaction(meta)

