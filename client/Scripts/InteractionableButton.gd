extends Button

var meta
@onready var MAIN = get_tree().root.get_node('Main')
@onready var GAME = get_tree().root.get_node('Main/Game')

# Called when the node enters the scene tree for the first time.
func _ready():
	#GAME = get_tree().root.get_node('Main/Game')
	print(GAME)
	meta = null
	mouse_default_cursor_shape=Control.CURSOR_POINTING_HAND
	size_flags_horizontal=Control.SIZE_FILL

	#button_up.connect(button_pressed.bind(meta_tag))
	pass # Replace with function body.
	
func json_to_data():
	if meta == null:
		return null
		
	var json = JSON.new()
	var data = json.parse_string(meta)
	return data
	
func meta_set(tag, object, label):
	meta = '%s' % [GAME.create_interaction_meta(tag, object, label)]


func _process(delta):
	pass

func data_get():
	return json_to_data()
	
func _pressed():
	if meta != null:
		GAME.interaction(meta)
