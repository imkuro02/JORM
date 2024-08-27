extends RichTextLabel

var MAIN
var sheet 

var hovered_item = null

@export var inventory: RichTextLabel
# Called when the node enters the scene tree for the first time.
func _ready():
	MAIN = get_tree().root.get_node('Main')
	inventory.meta_hover_started.connect(set_hovered_item)
	inventory.meta_hover_ended.connect(unset_hovered_item)
	pass # Replace with function body.


func set_hovered_item(meta):
	var json = JSON.new()
	var data = json.parse_string(meta)
	hovered_item = data['object']
	
func unset_hovered_item(meta):
	hovered_item = null
# Called every frame. 'delta' is the elapsed time since the previous frame.



func _process(_delta):
	var sheet = MAIN.CHARACTERSHEET
	var ITEMS = MAIN.PREMADE['items']
	if sheet == null:
		return

	text = ''
	text += '[table=3]'
	for trans in MAIN.PREMADE['translations']:
		#if trans in ['hp','mp','max_hp','max_mp']:
		if trans in ['hp','mp']:
			continue

		''' HORRIBLE TERRIBLE ITEM COMPARE CODE'''
		var hovered_item_stat_number = ''
		if hovered_item != null:
			var _i = ITEMS[hovered_item]
			if 'slot' in _i:
				if trans in _i['stats']:
					hovered_item_stat_number = int(_i['stats'][trans])
					for e in sheet['equipment']:
						if ITEMS[e]['slot'] == _i['slot']:
							hovered_item_stat_number = int(_i['stats'][trans] - ITEMS[e]['stats'][trans])
					if hovered_item_stat_number == 0:
						hovered_item_stat_number = '[color=gray]%s[/color]' % _i['stats'][trans]
					elif hovered_item_stat_number >= 1:
						hovered_item_stat_number = '[color=green]+%s[/color]' % hovered_item_stat_number
					else:
						hovered_item_stat_number = '[color=red]%s[/color]' % hovered_item_stat_number
		'''OH GOD'''

		var translated_name = MAIN.PREMADE['translations'][trans]
		var stat_number = sheet['stats'][trans]
		text += '[cell]%s: [/cell][cell]%s [/cell][cell]%s[/cell]' % [translated_name, stat_number, hovered_item_stat_number]	


	text += '[/table]'
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
