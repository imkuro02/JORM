extends Control

@onready var panel = $Panel
@onready var item = $Panel/Item
@onready var resize_button = $Panel/Item/Resize
@onready var item_container = $Panel/Item/PanelContainer

var min_size = Vector2()

var pressed = false
var resize_pressed = false

var can_resize = true

func _ready():
	min_size = Vector2(panel.size.x, item.size.y)
	
func set_item(_item: Node, can_resize = true):
	panel.position = _item.position
	resize_button.visible = can_resize
	#min_size = item.size
	panel.size.x = _item.size.x
	item.size.y = _item.size.y
	_item.reparent(item_container)


	
		
func _process(_delta):
	var size = get_window().size
	if panel.position.x < 0:
		panel.position.x = 0
		
	if panel.position.x + panel.size.x > size.x:
		panel.position.x = size.x - panel.size.x
		
	if panel.position.y < 0:
		panel.position.y = 0
		
	if item.visible:
		if panel.position.y + panel.size.y + item.size.y > size.y:
			panel.position.y = size.y - (panel.size.y + item.size.y)
	else:
		if panel.position.y + panel.size.y > size.y:
			panel.position.y = size.y - panel.size.y
			

	if panel.size.x <= min_size.x:
		panel.size.x = min_size.x 

	if item.size.y  <= min_size.y:
		item.size.y =  min_size.y
		
func _on_panel_gui_input(event):
	if event is InputEventMouseButton:
		if event.button_index == 1:
			pressed = event.pressed
			get_parent().move_child(self,-1)
			
	if event is InputEventMouseMotion and pressed:
		var pos = panel.position + event.relative
		#var size = get_window().size
		#print(size)
		panel.position = pos
		
		

func _on_resize_gui_input(event):
	
	if event is InputEventMouseButton:
		if event.button_index == 1:
			resize_pressed = event.pressed
			get_parent().move_child(self,-1)
			
	if event is InputEventMouseMotion and resize_pressed:
		var new_size_x = panel.size.x + event.relative.x
		if new_size_x >= min_size.x:
			panel.size.x = new_size_x
		var new_size_y = item.size.y + event.relative.y
		if new_size_y >= min_size.y:
			item.size.y = new_size_y


func _on_hide_toggled(toggled_on):
	item.visible = !toggled_on
