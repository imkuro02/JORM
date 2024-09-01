extends RichTextLabel

var MAIN
var hovered_item = null

@export var chatbox: RichTextLabel
@export var inventory: RichTextLabel

# Called when the node enters the scene tree for the first time.
func _ready():
	MAIN = get_tree().root.get_node('Main')
	
	inventory.meta_hover_started.connect(set_hovered_item)
	inventory.meta_hover_ended.connect(unset_hovered_item)
	chatbox.meta_hover_started.connect(set_hovered_item)
	chatbox.meta_hover_ended.connect(unset_hovered_item)
	pass # Replace with function body.
	
func _process(_delta):
	visible = hovered_item != null
	
func _input(event):
	if event is InputEventMouseMotion:
		position.y = 15+event.position.y
		position.x = 15+event.position.x
	if event is InputEventMouseButton:
		hovered_item = null
		
			
func set_hovered_item(meta):

	var json = JSON.new()
	var data = json.parse_string(meta)
	
	if data['tag'] not in ' equipment inventory loot ':
		return
		
	hovered_item = data['object']
	
	var sheet = MAIN.CHARACTERSHEET
	var ITEMS = MAIN.PREMADE['items']
	
	if sheet == null:
		return
		
	size.x = 5
	size.y = 5
	text = ''
	text += ITEMS[hovered_item]['name']
	
	if 'slot' in ITEMS[hovered_item]:
		text += ' (%s)\n' % [ITEMS[hovered_item]['slot']]
	else:
		text += '\n'
		
	text += ITEMS[hovered_item]['description'] + '\n'

	if 'stats' not in ITEMS[hovered_item]:
		return
	
	text += '[table=2]'
	for trans in MAIN.PREMADE['translations']:
		#if trans in ['hp','mp','max_hp','max_mp']:
		if trans in ['hp','mp', 'exp', 'points']:
			continue


		var translated_name = MAIN.PREMADE['translations'][trans]
		var stat_number = sheet['stats'][trans]
		var hovered_item_stat_number = ITEMS[hovered_item]['stats'][trans]
		
		if hovered_item_stat_number == 0:
			continue
			
		text += '[cell]%s: [/cell][cell]%s[/cell]' % [translated_name, hovered_item_stat_number]	


	text += '[/table]'
	
	
	
func unset_hovered_item(meta):
	hovered_item = null
