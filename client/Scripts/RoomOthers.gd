extends RichTextLabel

var MAIN
@export var GAME: Control

# Called when the node enters the scene tree for the first time.
func _ready():
	MAIN = get_tree().root.get_node('Main')
	meta_clicked.connect(metaclicked)
	pass # Replace with function body.

func metaclicked(meta):
	GAME.interaction(meta)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	var sheet = MAIN.CHARACTERSHEET
	var room = MAIN.ROOM
	if sheet == null:
		return
	if room == null:
		return
	var players = room['players']
	var enemies = room['enemies']
	var target = sheet['target']
	
	text = ''
		
	#others.text += 'Players:\n'
	for player in players:
		var character = players[player]
		var id = player
		var name = player
		var hp = character['stats']['hp']
		var max_hp = character['stats']['max_hp']
		if target == id:
			text += GAME.interactable('target',id,name)
		else:
			text += GAME.interactable('player',id,name)
		text += '\n'

	for enemy in enemies:
		var character = enemies[enemy]
		var id = enemy
		var name = enemy
		var hp = character['stats']['hp']
		var max_hp = character['stats']['max_hp']
		if target == id:
			text += GAME.interactable('target',id,name)
		else:
			text += GAME.interactable('enemy',id,name)
		text += '\n'

