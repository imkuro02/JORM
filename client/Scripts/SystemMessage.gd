extends Control
	
func message(title,message):
	$Title.text = title
	$Message.text = message

func _on_button_pressed():
	queue_free()
