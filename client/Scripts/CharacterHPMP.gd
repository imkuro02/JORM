extends GridContainer

@onready var hp = $HP_BAR/Label
@onready var hp_bar = $HP_BAR

@onready var mp = $MP_BAR/Label
@onready var mp_bar = $MP_BAR

var sheet = null

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func set_sheet(_sheet):
	sheet = _sheet
	return
	if sheet == null:
		get_node("Name").text = 'None'
		
		get_node("HP_BAR").max_value = 100
		get_node("MP_BAR").max_value = 100
		
		get_node("HP_BAR").value = 0
		get_node("MP_BAR").value = 0  

		get_node("HP_BAR/Label").text = '-' 
		get_node("MP_BAR/Label").text = '-' 
		return
		
	#get_node("Name").text = 'None'
	
	get_node("HP_BAR").max_value = sheet['stats']['max_hp']
	get_node("MP_BAR").max_value = sheet['stats']['max_mp']
	
	get_node("HP_BAR").value = sheet['stats']['hp']
	get_node("MP_BAR").value = sheet['stats']['mp']

	get_node("HP_BAR/Label").text = 'HP: %s/%s' % [sheet['stats']['hp'],sheet['stats']['max_hp']]
	get_node("MP_BAR/Label").text = 'MP: %s/%s' % [sheet['stats']['mp'],sheet['stats']['max_mp']]
	
func _process(_delta):
	if sheet == null:
		get_node("Name").text = 'None'
		
		get_node("HP_BAR").max_value = 100
		get_node("MP_BAR").max_value = 100
		
		get_node("HP_BAR").value = 0
		get_node("MP_BAR").value = 0  

		get_node("HP_BAR/Label").text = '-' 
		get_node("MP_BAR/Label").text = '-' 
		return
		
	get_node("Name").text = sheet['name']
	
	get_node("HP_BAR").max_value = sheet['stats']['max_hp']
	get_node("MP_BAR").max_value = sheet['stats']['max_mp']
	
	if sheet['stats']['hp'] > get_node("HP_BAR").value:
		get_node("HP_BAR").value += get_node("HP_BAR").max_value/100
	if sheet['stats']['hp'] < get_node("HP_BAR").value:
		get_node("HP_BAR").value -= get_node("HP_BAR").max_value/100
		
	if sheet['stats']['mp'] > get_node("MP_BAR").value:
		get_node("MP_BAR").value += get_node("MP_BAR").max_value/100
	if sheet['stats']['mp'] < get_node("MP_BAR").value:
		get_node("MP_BAR").value -= get_node("MP_BAR").max_value/100
	
	
	get_node("HP_BAR/Label").text = 'HP: %s/%s' % [sheet['stats']['hp'],sheet['stats']['max_hp']]
	get_node("MP_BAR/Label").text = 'MP: %s/%s' % [sheet['stats']['mp'],sheet['stats']['max_mp']]
