extends Node

@onready var equip = $Equip
@onready var message = $Message
@onready var go = $Go
@onready var church_bell = $ChurchBell
@onready var consume_drink = $ConsumeDrink

# Called when the node enters the scene tree for the first time.
func _ready():
	#equip.play()
	set_volume(0)
	pass # Replace with function body.

func set_volume(vol):
	equip.volume_db = vol
	message.volume_db = vol - 20
	go.volume_db = vol
	church_bell.volume_db = vol
	consume_drink.volume_db = vol
	
func play(sound):
	match sound:
		'message':
			message.pitch_scale = randf_range(0.5,1)
			message.play()
		'equip':
			equip.pitch_scale = randf_range(0.8,1.2)
			equip.play()
		'go':
			go.pitch_scale = randf_range(0.8,1.2)
			go.play()
		'church_bell':
			church_bell.pitch_scale = randf_range(0.8,1.2)
			church_bell.play()
		'consume_drink':
			consume_drink.pitch_scale = randf_range(0.8,1.2)
			consume_drink.play()
			
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	pass
