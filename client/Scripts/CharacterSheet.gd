extends RichTextLabel

var MAIN
var sheet 
# Called when the node enters the scene tree for the first time.
func _ready():
	MAIN = get_tree().root.get_node('Main')
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	var sheet = MAIN.CHARACTERSHEET
	if sheet == null:
		return

	
	text = ''
	text += '[table=2]'
	for trans in MAIN.PREMADE['translations']:
		if trans in ['hp','mp']:
			continue

		var translated_name = MAIN.PREMADE['translations'][trans]
		var stat_number = sheet['stats'][trans]
		text += '[cell]%s: [/cell][cell]%s [/cell]' % [translated_name, stat_number]	
	text += '[/table]'
