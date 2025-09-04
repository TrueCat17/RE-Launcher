label rpg_start:
	python:
		set_location('enter', 'ikarus_out')
		me.set_direction(to_back)
	
	"RPG starts here."
	"Use WASD + Shift. Action key: E, Inventory - I."
	"Quick save/load: Q/L."
	"Hide/Show interface: H, screenshot: P."
	
	window hide
	$ set_rpg_control(True)
