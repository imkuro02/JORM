extends VBoxContainer

@onready var MAIN = get_tree().root.get_node('Main')
@onready var template = get_node('Presets/Panel')
@onready var entities_vbox = get_node('Entities')
@export var GAME: Control
# Called when the node enters the scene tree for the first time.
func _ready():
	template.visible = false

func does_actor_exist_in_entities_vbox(actor_name):
	for entity in entities_vbox.get_children():
		if entity.get_node('Label').text == actor_name:
			return true
	return false
		
func _process(delta):
	var ROOM = MAIN.ROOM
	
	if ROOM == null:
		return
	if MAIN.CHARACTERSHEET == null:
		return
		
		
	var all_actors = ROOM['players'].duplicate(true)
	all_actors.merge(ROOM['enemies'].duplicate(true))
	for actor in all_actors:
		if does_actor_exist_in_entities_vbox(actor):
			continue

		var entity = template.duplicate()
		entity.get_node('Label').text = all_actors[actor]['name']
		entity.button_up.connect(button_pressed.bind(entity))
		
		if actor in ROOM['players']:
			if actor == MAIN.CHARACTERSHEET['name']:
				entity.get_node('Label').self_modulate = Color(GAME.color_to_tags['player_self'])
			else:
				entity.get_node('Label').self_modulate = Color(GAME.color_to_tags['player'])
			entity.get_node('TextureProgressBar').tint_progress = Color('GREEN')
		if actor in ROOM['enemies']:
			entity.get_node('Label').self_modulate = Color(GAME.color_to_tags['enemy'])
			entity.get_node('TextureProgressBar').tint_progress = Color('RED')
			
		entity.visible = true
		entities_vbox.add_child(entity)
		
	for entity in entities_vbox.get_children():
		var name = entity.get_node('Label')
		if name.text not in all_actors:
			#entities_vbox.remove_child(entity)
			entity.get_node('TextureProgressBar').value = 0
			entity.get_node('AnimationPlayer').play('fade')
			#entity.queue_free()
			continue
	
		
		if name.text in all_actors:
			entity.get_node('Control').visible = MAIN.CHARACTERSHEET['target'] == name.text
			entity.get_node('TextureProgressBar').max_value = all_actors[name.text]['stats']['max_hp']
			entity.get_node('TextureProgressBar').value = all_actors[name.text]['stats']['hp']
	
		#create_interaction_meta(tag, object, label)

func button_pressed(entity):
	var ROOM = MAIN.ROOM
	var name = entity.get_node('Label').text
	var tag = null
	
	if name in ROOM['players']:
		tag = 'player'
	if name in ROOM['enemies']:
		tag = 'enemy'
	if name == MAIN.CHARACTERSHEET['target']:
		tag = 'target'
	
	if tag == null:
		print('button_pressed in Others.gd tag is null, why the fuck is it null')
		return
	
	var meta = '%s' % [GAME.create_interaction_meta(tag, name, name)]
	GAME.interaction(meta)
	

	
	#print(entity.get_node('Label').text)
	#print('pressed')
	
func interaction(meta):
	GAME.interaction(meta)
