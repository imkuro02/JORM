extends Panel

var states
var state 
var nodes
# Called when the node enters the scene tree for the first time.
func _ready():
	
	states = []
	nodes = []
	for i in get_node('VBoxContainer/Buttons').get_children():
		states.append(i.name)
	for i in get_node('VBoxContainer/States').get_children():
		nodes.append(i.name)
	pass # Replace with function body.
	
	state = states[0]


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	for i in get_node('VBoxContainer/Buttons').get_children():
		if i.button_pressed == true: 
			state = i.name
	for i in get_node('VBoxContainer/States').get_children():
		i.visible = i.name == state

