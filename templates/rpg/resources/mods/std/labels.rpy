label rpg_start:
	python:
		set_location("enter", "ikarus_out")
		me.set_direction(to_back)
	
	"RPG starts here."
	"Use WASD/arrows + Shift. Action key: E."
	"Quick save/load: Q/L."
	"Hide/Show interface: H, screenshot: P."
	
	window hide
	$ set_rpg_control(True)

