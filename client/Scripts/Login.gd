extends Control

@onready var username = $VBoxContainer/Username/TextEdit
@onready var password = $VBoxContainer/Password/TextEdit
@onready var login = $VBoxContainer/Buttons/Login
@onready var register = $VBoxContainer/Buttons/Register
@onready var bgpanel = $BGPanel

const Packet = preload("res://Scripts/Packet.gd")

var MAIN 

# Called when the node enters the scene tree for the first time.
func _ready():
	MAIN = get_tree().root.get_node('Main')
	login.pressed.connect(self._login)
	register.pressed.connect(self._register)
	bgpanel.size = $VBoxContainer.size + Vector2(20,20)
	bgpanel.position = $VBoxContainer.position - Vector2(10,10)
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


