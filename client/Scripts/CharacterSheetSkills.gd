extends VBoxContainer

@onready var MAIN = get_tree().root.get_node('Main')
@onready var PRESETS = get_node("Presets")
@onready var OBJECTS = get_node("Objects")
# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if MAIN.ROOM == null:
		return
	if MAIN.CHARACTERSHEET == null:
		return
		
	var skills = MAIN.CHARACTERSHEET['skills']
	var cooldowns = MAIN.CHARACTERSHEET['skill_cooldowns']

	var existing_skills = []
	
	for o in OBJECTS.get_children():
		
		var meta = o.data_get()
		existing_skills.append(meta['object'])
		

		if meta['object'] in cooldowns:
			o.get_node('V/Top/Label2').text = '(%ss)' % [int(abs(MAIN.SERVER_TIME - cooldowns[meta['object']])/30)+1]
		else:
			o.get_node('V/Top/Label2').text = 'READY'
			
		o.get_node('V/Top/Label').text = meta['label']
		o.get_node('V/Bot/Label').text = str(MAIN.PREMADE['skills'][meta['object']]['mp_cost'])
		
		if meta['object'] not in skills:
			o.queue_free()
		
		
	for skill in skills:
		if skill in existing_skills:
			continue
		var object = PRESETS.get_node('Button').duplicate()
		OBJECTS.add_child(object)
		
		var name = MAIN.PREMADE['skills'][skill]['name']
		
		object.meta_set('skill',skill,name)
		object.visible = true
		
	
	
		

		
	
	pass
