extends RichTextLabel

var MAIN
@export var GAME: Control

var _show_description = true
# Called when the node enters the scene tree for the first time.
func _ready():
	MAIN = get_tree().root.get_node('Main')
	meta_clicked.connect(metaclicked)
	pass # Replace with function body.

func metaclicked(meta):
	if meta == 'description':
		_show_description = !_show_description
		return
	GAME.interaction(meta)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):

	var room = MAIN.ROOM

	if room == null:
		return

	
	text = ''
	text += '[url="description"][center][color="GOLD"]%s[/color][/center][/url]\n' % [room['name']]
	if _show_description:
		text += '%s\n' % [room['description']]
	for exit in room['exits']:
		text += '%s\n' % [GAME.interactable('exit',exit,exit)]
	

