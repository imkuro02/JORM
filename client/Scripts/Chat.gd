extends Control

const Packet = preload("res://Scripts/Packet.gd")

@onready var chatbox = $CanvasLayer/Chatbox/Chatbox
@onready var input = $CanvasLayer/Chatbox/LineEdit

@onready var settings = $CanvasLayer/Settings
@onready var others = $CanvasLayer/Others
@onready var ch = $CanvasLayer/CharacterSheet
@onready var inv = $CanvasLayer/Inventory
@onready var inv_text = $CanvasLayer/Inventory/Inventory
@onready var inv_search = $CanvasLayer/Inventory/LineEdit
@onready var skills = $CanvasLayer/Skills

var interactions_popup = preload("res://Scenes/Interactions.tscn")

#@onready var tooltip = $CanvasLayer/Tooltip

var sheet



var MAIN 

var ROOM = {}

func _ready():
	MAIN = get_tree().root.get_node('Main')
	MAIN.create_draggable_ui(self,'Chat',$CanvasLayer/Chatbox)
	MAIN.create_draggable_ui(self,'Character Sheet',ch)
	MAIN.create_draggable_ui(self,'Settings',settings)
	MAIN.create_draggable_ui(self,'Inventory',inv)
	MAIN.create_draggable_ui(self,'Others',others)
	MAIN.create_draggable_ui(self,'Skills',skills)
	
	
	
	
func _process(_delta):
	# print server time delay
	settings.get_node('Delay').text = 'tick: %s' % [int(MAIN.SERVER_TIME)]
	refresh_players()
	

func interaction(data):
	hovered_item = null # just reset hovered item real quick
	var w = interactions_popup.instantiate()
	add_child(w)
	w.create_interaction(data, Input.is_key_pressed(KEY_CTRL))

		
	
func receive_simple_message(text: String):
	MAIN.audio.play('message')
	chatbox.text += '%s\n' % [text]
	
func receive_chat(sender: String, text: String):
	MAIN.audio.play('message')
	chatbox.text += '%s Says %s\n' % [interactable('player',sender,sender),text]

func receive_flavoured_message(text):
	#var time = Time.get_ticks_usec()
	var _players = ROOM['players']
	var _enemies = ROOM['enemies']
	var _skills  = MAIN.PREMADE['skills']
	var _items   = MAIN.PREMADE['items']
	var _exits   = ROOM['exits']
	text = ' '+text+' '
	for i in _items:
		text = text.replace(' '+_items[i]['name']+' ', ' '+interactable('loot',i,_items[i]['name'])+' ')
	for i in _enemies:
		text = text.replace(' '+_enemies[i]['name']+' ', ' '+interactable('enemy',i,_enemies[i]['name'])+' ')
	for i in _players:
		text = text.replace(' '+_players[i]['name']+' ', ' '+interactable('player',i,_players[i]['name'])+' ')
	for i in _skills:
		
		text = text.replace(' '+_skills[i]['name']+' ', ' '+interactable('skill',i,_skills[i]['name'])+' ')
	for i in _exits:
		text = text.replace(' '+i+' ', ' '+interactable('exit', i, i )+' ')
	#print(Time.get_ticks_usec() - time)
	
	text = text.strip_edges(true, false)
	chatbox.text += text + '\n'
	MAIN.audio.play('message')
	
func interactable(tag, object, label):
	var x = '[url={"tag":"%s","object":"%s","label":"%s"}]%s[/url]' % [tag, object, label, label]
	var col
	match tag:
		'player':
			col = 'aqua'
		'enemy': 
			col = 'coral'
		'inventory':
			col = 'LIGHT_STEEL_BLUE'
		'equipment':
			col = 'LIGHT_STEEL_BLUE'
		'target':
			col = 'yellow'
		'exit':
			col = 'green'
		'skill':
			col = 'LIGHT_GOLDENROD'
		'loot':
			col = 'yellow'
		_:
			return x
	x = '[color="%s"]' % [col] + x + '[/color]' 
	#print(x)
	return x
	
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
			others.text += interactable('target',id,'> '+name)
		else:
			others.text += interactable('player',id,name)
		others.text += ''' [color=red] %s%%[/color]\n''' % [int((hp/max_hp)*100)]
	
	#others.text += 'Enemies:\n'
	for enemy in ROOM['enemies']:
		var character = ROOM['enemies'][enemy]
		var id = enemy
		var name = enemy
		var hp = character['stats']['hp']
		var max_hp = character['stats']['max_hp']
		if sheet['target'] == id:
			others.text += interactable('target',id,'> '+name)
		else:
			others.text += interactable('enemy',id,name)
		others.text += ''' [color=red] %s%%[/color]\n''' % [int((hp/max_hp)*100)]
		
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
		
	ROOM = room
		
	return
		
func receive_character_sheet(_sheet):
	var ITEMS = MAIN.PREMADE['items']
	var SKILLS = MAIN.PREMADE['skills']
	sheet = _sheet
	
	ch.get_node("Label").text = sheet['name']
	ch.get_node("GridContainer/HP_BAR").value = sheet['stats']['hp']
	ch.get_node("GridContainer/HP_BAR").max_value = sheet['stats']['max_hp']
	ch.get_node("GridContainer/MP_BAR").value = sheet['stats']['mp']
	ch.get_node("GridContainer/MP_BAR").max_value = sheet['stats']['max_mp']
	ch.get_node("GridContainer/HP_BAR/Label").text = 'HP: %s/%s' % [sheet['stats']['hp'],sheet['stats']['max_hp']]
	ch.get_node("GridContainer/MP_BAR/Label").text = 'MP: %s/%s' % [sheet['stats']['mp'],sheet['stats']['max_mp']]

	
	var stats = ch.get_node('RichTextLabel')
	stats.text = ''
	stats.text += '[table=3]'
	for trans in MAIN.PREMADE['translations']:
		#if trans in ['hp','mp','max_hp','max_mp']:
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
	inv_text.text += 'Equipment:\n'
	inv_text.text += '[table=2]'
	for i in sheet['equipment']:
		if inv_search.text.to_lower() not in ITEMS[i]['name'].to_lower() and not inv_search.text.to_lower()=='':
			continue
		inv_text.text += '[cell]%s:   [/cell][cell]%s[/cell]\n' % [ITEMS[i]['slot'].capitalize(), interactable('equipment',i,ITEMS[i]['name'])]

	inv_text.text += '[/table]'
	inv_text.text += '\n\nInventory:\n'

	inv_text.text += '[table=2]' 
	for i in sheet['inventory']:
		if inv_search.text.to_lower() not in ITEMS[i]['name'].to_lower() and not inv_search.text.to_lower()=='':
			continue
	
		var quantity = sheet['inventory'][i]
		if quantity > 1:
			quantity = ' x %s' % [quantity]
		else:
			quantity = ''
		inv_text.text += '[cell]%s[/cell][cell]%s[/cell]\n' % [interactable('inventory',i,ITEMS[i]['name']),quantity]


	inv_text.text += '[/table]'
	
	''' SKILLS '''
	skills.text = '[table=3]'
	#print(MAIN.SERVER_TIME)
	for skill in sheet['skills']:
		
		var cooldown = ''
		if skill in sheet['skill_cooldowns']:
			cooldown = '(%ss)' % [int(abs(MAIN.SERVER_TIME - sheet['skill_cooldowns'][skill])/30)+1]
		skills.text += '[cell]%s[/cell][cell] [color="aqua"]%s[/color][/cell][cell]%s[/cell]\n' % [interactable('skill',skill,SKILLS[skill]['name']),SKILLS[skill]['mp_cost'],cooldown]
		
	skills.text += '[/table]'
	
func show_room():
	var exits = ROOM['exits']
	chatbox.text += '[center]~~~ %s ~~~[/center]\n' % [ROOM['name']]
	#chatbox.text += '[center][img=420]Images/fields.png[/img][/center]\n'
	var desc = ROOM['description']
	for e in ROOM['exits']:
		#print(e)
		desc = desc.replace(e,interactable('exit',e,e))
	chatbox.text += desc + '\n\n'
	#chatbox.text += 'Exits:\n'
	#for e in exits:
	#	chatbox.text += '          %s\n' % interactable('exit',e,e)
	#chatbox.text += '\n\n'
	
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

func _on_inventory_meta_clicked(meta):
	interaction(meta)

func _on_chatbox_meta_clicked(meta):
	interaction(meta)

func _on_others_meta_clicked(meta):
	interaction(meta)
	
func _on_font_size_value_changed(value):
	MAIN.theme.default_font_size = int(value)

func _on_audio_volume_value_changed(value):
	MAIN.audio.set_volume(value)

var hovered_item = null
func _on_inventory_meta_hover_started(meta):
	var json = JSON.new()
	var data = json.parse_string(meta)
	hovered_item = data['object']
	pass # Replace with function body.

func _on_inventory_meta_hover_ended(meta):
	hovered_item = null
	pass # Replace with function body.
