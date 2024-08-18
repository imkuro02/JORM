extends Control


func _ready():
	if false:
		await _fade_out()
		await _fade_in()
		await _fade_out()

	




func _fade_in():
	var tween = get_tree().create_tween()
	await tween.tween_property($ColorRect, "color:a", 1, 1).finished
	print('faded in')
	
func _fade_out():
	var tween = get_tree().create_tween()
	await tween.tween_property($ColorRect, "color:a", 0.0, 1).finished
	print('faded out')
	queue_free()
