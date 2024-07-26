extends Node

@onready var equip = $Equip
@onready var message = $Message
@onready var item = $Item

# Called when the node enters the scene tree for the first time.
func _ready():
	#equip.play()
	set_volume(0)
	pass # Replace with function body.

func set_volume(vol):
	equip.volume_db = vol
	message.volume_db = vol - 20
	item.volume_db = vol
	
func play(sound):
	match sound:
		'message':
			message.pitch_scale = randf_range(0.8,1.2)
			message.play()
		'equip':
			equip.pitch_scale = randf_range(0.8,1.2)
			equip.play()
		'item':
			item.pitch_scale = randf_range(0.8,1.2)
			item.play()
			
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	pass
