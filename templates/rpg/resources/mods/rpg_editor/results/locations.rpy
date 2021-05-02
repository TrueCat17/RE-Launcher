init python:
	
	register_location("enter", "images/locations/enter/", False, 960, 992)
	register_place(   "enter", "gate_left_pos", 449, 279, 2, 2)
	register_place(   "enter", "gate_right_pos", 509, 279, 2, 2)
	register_place(   "enter", "ikarus_out", 400, 590, 40, 40)
	register_place(   "enter", "ikarus_pos", 293, 590, 2, 2)
	register_place(   "enter", "left", 0, 570, 40, 140, to=["left", "enter", "right"])
	register_place(   "enter", "right", 920, 565, 40, 145, to=["right", "enter", "left"])
	
	
	
	rpg_locations["enter"].x, rpg_locations["enter"].y = 420, 350

