extends VBoxContainer

@onready var MAIN = get_tree().root.get_node('Main')
@onready var template = get_node('Presets/Character')
@onready var entities_vbox = get_node('Entities/VBoxContainer')


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
		
	var npcs = ROOM['npcs'].duplicate(true)
	var all_actors = ROOM['players'].duplicate(true)
	all_actors.merge(ROOM['enemies'].duplicate(true))
			
	for actor in all_actors:
		if does_actor_exist_in_entities_vbox(actor):
			continue

		var entity
		if actor in ROOM['players']:
			entity = template.duplicate()
		if actor in ROOM['enemies']:
			entity = template.duplicate()

		entity.get_node('Label').text = all_actors[actor]['name']
		#entity.button_up.connect(button_pressed.bind(entity))		
		
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
		if name.text == MAIN.CHARACTERSHEET['name']:
			entities_vbox.move_child(entity, 0)
			
		var _name = entity.get_node('Label').text
		var tag = null
		if _name in ROOM['players']:
			tag = 'player'
		if _name in ROOM['enemies']:
			tag = 'enemy'
		if _name == MAIN.CHARACTERSHEET['target']:
			tag = 'target'
		if tag != null:
			entity.meta_set(tag,_name,_name)
			
		if name.text not in all_actors and name.text:
			#entities_vbox.remove_child(entity)
			entity.get_node('TextureProgressBar').value = 0
			entity.get_node('AnimationPlayer').play('fade')
			#entity.queue_free()
			continue
	
		
		if name.text in all_actors and name.text:
			var hp_diff = all_actors[name.text]['stats']['hp'] - entity.get_node('TextureProgressBar').value
			
			if hp_diff != 0:
				var stat_tick = entity.get_node('StatTickAnim')
				var s = stat_tick.duplicate()
				s.visible = true
				if hp_diff <= -1:
					s.set("theme_override_colors/font_color",'red')
					s.text = '%s' % [hp_diff]
				if hp_diff >= 1:
					s.set("theme_override_colors/font_color",'green')
					s.text = '+%s' % [hp_diff]
				entity.add_child(s)
				s.get_node('AnimationPlayer').play('fade')
				
				
				
			entity.get_node('Control').visible = MAIN.CHARACTERSHEET['target'] == name.text
			entity.get_node('TextureProgressBar').max_value = all_actors[name.text]['stats']['max_hp']
			entity.get_node('TextureProgressBar').value = all_actors[name.text]['stats']['hp']
			
			entity.get_node('HP').text = '%s/%s' % [all_actors[name.text]['stats']['hp'],all_actors[name.text]['stats']['max_hp']]
			entity.get_node('MP').text = '%s/%s' % [all_actors[name.text]['stats']['mp'],all_actors[name.text]['stats']['max_mp']]
			
	
