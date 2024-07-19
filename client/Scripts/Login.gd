extends Control

@onready var username = get_node("CanvasLayer/Container/Username/TextEdit")
@onready var password = get_node("CanvasLayer/Container/Username/TextEdit")
@onready var login = get_node("CanvasLayer/Container/Buttons/Login")
@onready var register = get_node("CanvasLayer/Container/Buttons/Register")

const Packet = preload("res://Scripts/Packet.gd")

var MAIN 

# Called when the node enters the scene tree for the first time.
func _ready():
	MAIN = get_tree().root.get_node('Main')
	login.pressed.connect(self._login)
	register.pressed.connect(self._register)
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	pass
	
func _login():
	var _username = username.text
	var _password = password.text
	var p: Packet = Packet.new('Login',[_username,_password])
	MAIN.send_packet(p)
	
func _register():
	var _username = username.text
	var _password = password.text
	var p: Packet = Packet.new('Register',[_username,_password])
	MAIN.send_packet(p)


