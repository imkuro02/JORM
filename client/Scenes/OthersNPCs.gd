extends VBoxContainer

@onready var MAIN = get_tree().root.get_node('Main')
@onready var template = get_node('Presets/NPC')
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

	var all_actors = ROOM['npcs'].duplicate(true)
			
	for actor in all_actors:
		if does_actor_exist_in_entities_vbox(actor):
			continue
			
		var entity = template.duplicate()

		entity.get_node('Label').self_modulate = Color(GAME.color_to_tags['enemy'])
		entity.get_node('TextureProgressBar').tint_progress = Color('ORANGE')
		entity.get_node('Label').text = actor
			
		entity.visible = true
		entities_vbox.add_child(entity)
		
	for entity in entities_vbox.get_children():
		var name = entity.get_node('Label')
			
		var _name = entity.get_node('Label').text
		var tag = null
		if _name in ROOM['npcs']:
			tag = 'npc'
		if tag != null:
			entity.meta_set(tag,_name,_name)
			
		if name.text not in all_actors:
			entity.get_node('TextureProgressBar').value = 0
			entity.get_node('AnimationPlayer').play('fade')
			continue
	
		
		
