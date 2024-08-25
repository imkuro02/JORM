extends VBoxContainer

const Packet = preload("res://Scripts/Packet.gd")

var MAIN
@export var GAME: Control
var AUTOUSE
var LABEL 

var prev_autouse = 0

# Called when the node enters the scene tree for the first time.
func _ready():
	MAIN = get_tree().root.get_node('Main')
	AUTOUSE = get_node('CheckBox')
	LABEL = get_node('RichTextLabel')
	LABEL.meta_clicked.connect(meta_clicked)
	pass # Replace with function body.

func meta_clicked(meta):
	GAME.interaction(meta)
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	var sheet = MAIN.CHARACTERSHEET
	
	if sheet == null:
		return
		
	var skills = sheet['skills']
	var cooldowns = sheet['skill_cooldowns']
	var SKILLS = MAIN.PREMADE['skills']
	
	''' SKILLS '''
	LABEL.text = '[table=4]'
	for skill in skills:
		var cooldown = ''
		var autouse = ''

		if skill in cooldowns:
			cooldown = '(%ss)' % [int(abs(MAIN.SERVER_TIME - cooldowns[skill])/30)+1]
			

			
		LABEL.text += '[cell]%s [/cell][cell][color="aqua"]%s [/color][/cell][cell] %s[/cell][cell]%s[/cell] \n' % [
			GAME.interactable('skill',skill,SKILLS[skill]['name']),
			SKILLS[skill]['mp_cost'],
			cooldown,
			autouse
		]
	LABEL.text += '[/table]'
	
