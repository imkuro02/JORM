extends Node

var socket = WebSocketPeer.new()
const Packet = preload("res://Scripts/Packet.gd")
var state: Callable
var LOGIN_WINDOW = preload("res://Scenes/Login.tscn")
var CHAT_WINDOW = preload("res://Scenes/Chat.tscn")
var login_window
var chat_window

var PREMADE: Dictionary

func _ready():
	state = Callable(self, 'LOGIN')
	
	login_window = add_window(LOGIN_WINDOW)

	connect_to_server()

func connect_to_server():
	socket = WebSocketPeer.new()
	# Connect to the WebSocket server with SSL enabled and the custom TLS options.
	var err = socket.connect_to_url("wss://127.0.0.1:8081", TLSOptions.client_unsafe())
	if err != OK:
		print("Error connecting to WebSocket:", err)
	else:
		print("WebSocket connection initiated")
		
func add_window(window):
	var w = window.instantiate()
	add_child(w)
	return w
	
func remove_window(window):
	var w = window
	remove_child(w)
	w.queue_free()
		
func LOGIN(p):
	var _payloads = p.payloads
	match p.action:
		"Ok":
			state = Callable(self, 'PLAY')
			remove_window(login_window)
			chat_window = add_window(CHAT_WINDOW)
		"Deny":
			pass
			
func PLAY(p):
	var _payloads = p.payloads
	match p.action:
		"Premade":
			PREMADE = _payloads[0]
		"Chat":
			var message = "Something went wrong with receiving Chat message"
			if _payloads[1] == null:
				chat_window.receive_simple_message(_payloads[0])
			else:
				chat_window.receive_chat(_payloads[1], _payloads[0])
			
		"CharacterSheet":
			chat_window.receive_character_sheet(_payloads[0])
			
		"Room":
			var room = {'name':_payloads[0],'description':_payloads[1],'exits':_payloads[2]}
			chat_window.receive_room(room)
			
		"Disconnect":
			socket.close()
			state = Callable(self, 'LOGIN')
			remove_window(chat_window)
			login_window = add_window(LOGIN_WINDOW)
			
			connect_to_server()
			
			


func _process(delta):
	socket.poll()
	var socket_state = socket.get_ready_state()
	if socket_state == WebSocketPeer.STATE_OPEN:
		while socket.get_available_packet_count():
			var packet = socket.get_packet()
			var json_string: String = packet.get_string_from_utf8()
			var packet_obj = Packet.json_to_action_payloads(json_string)
			var p: Packet = Packet.new(packet_obj['action'],packet_obj['payloads'])
			state.call(p)
			var _payloads = p.payloads
			#print(p.tostring())

	elif socket_state == WebSocketPeer.STATE_CLOSING:
		# Keep polling to achieve proper close.
		pass
		
	elif socket_state == WebSocketPeer.STATE_CLOSED:
		var code = socket.get_close_code()
		var reason = socket.get_close_reason()
		print("WebSocket closed with code: %d, reason %s. Clean: %s" % [code, reason, code != -1])
		set_process(false)  # Stop processing.

func send_packet(packet: Packet) -> void:
	# Sends a packet to the server
	
	_send_string(packet.tostring())

func _send_string(string: String) -> void:
	socket.put_packet(string.to_utf8_buffer())
	#_client.get_peer(1).put_packet(string.to_utf8())
	#print("Sent string ", string)
	
func _exit_tree():
	if socket.get_ready_state() == WebSocketPeer.STATE_OPEN:
		socket.close()
		print("WebSocket connection closed gracefully.")
