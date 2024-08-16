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
	match room_name:
		'Small Town':
			bg = bg_city
		'Small Town Ruins':
			bg = bg_ruins
		'Small Town Gate':
			bg = bg_ruins
		'Forest West Of Small Town':
			bg = bg_forest1
		'Forest East Of Big Town':
			bg = bg_forest
		'Big Town Gate':
			bg = bg_city1
	$Background.texture = bg
		
