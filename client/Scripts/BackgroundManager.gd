extends Control

@export var bg_basic: Texture
@export var bg_city: Texture
@export var bg_city1: Texture
@export var bg_forest: Texture
@export var bg_forest1: Texture
@export var bg_ruins: Texture

var bg 
func new_room(room_name):
	bg = bg_basic
	var backgrounds = {
		'Small Town': bg_city,
		'Small Town Ruins': bg_ruins,
		'Small Town Gate': bg_ruins,
		'Forest West Of Small Town': bg_forest1,
		'Forest East Of Big Town': bg_forest,
		'Big Town Gate' : bg_city1
	}
	if room_name in backgrounds:
		bg = backgrounds[room_name]
	$Background.texture = bg
		
