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
	var SHEET = MAIN.CHARACTERSHEET
	var ROOM = MAIN.ROOM
	
	
	if SHEET == null:
		return
	if ROOM == null:
		return

	var target = SHEET['target']
	
	text = ''
		
	#others.text += 'Players:\n'
	var all_actors = ROOM['players'].duplicate(true)
	all_actors.merge(ROOM['enemies'].duplicate(true))
	for actor in all_actors:
		var character = all_actors[actor]
		var name = all_actors[actor]['name']
		
		var hp = character['stats']['hp']
		var max_hp = character['stats']['max_hp']
		var mp = character['stats']['mp']
		var max_mp = character['stats']['max_mp']

		if target == name:
			text += GAME.interactable('target',name,name)
		else:
			if name in ROOM['players']:
				text += GAME.interactable('player',name,name)
			else:
				text += GAME.interactable('enemy',name,name)
			
		text += '\n'
		text += '[color=CRIMSON]HP:%s/%s[/color]\n' % [hp,max_hp]
		text += '[color=CORNFLOWER_BLUE]MP:%s/%s[/color]\n' % [mp,max_mp]
		
