extends RichTextLabel

var MAIN
@export var GAME: Control

# Called when the node enters the scene tree for the first time.
func _ready():
	MAIN = get_tree().root.get_node('Main')
	var tags = GAME.color_to_tags
	text = 'Color Codes:\n[table=2]'
	var interactables = ['player','enemy','target','exit','inventory','skill','status']
	text += '[cell][color=%s]%s        [/color][/cell]\n' % [tags['player'],'PLAYER']
	text += '[cell][color=%s]%s[/color][/cell]\n' % [tags['enemy'],'ENEMY']
	text += '[cell][color=%s]%s[/color][/cell]\n' % [tags['target'],'TARGET']
	text += '[cell][color=%s]%s[/color][/cell]\n' % [tags['exit'],'EXIT']
	text += '[cell][color=%s]%s[/color][/cell]\n' % [tags['inventory'],'ITEM']
	text += '[cell][color=%s]%s[/color][/cell]\n' % [tags['skill'],'SKILL']
	text += '[cell][color=%s]%s[/color][/cell]' % [tags['status'],'STATUS']
	text += '[cell][color=%s]%s[/color][/cell]' % ['YELLOW','ACTION']

