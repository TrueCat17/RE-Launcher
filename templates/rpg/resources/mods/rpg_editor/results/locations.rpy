init python:
	
	register_location("enter", "images/locations/enter/", False, 960, 992)
	register_place(   "enter", "gate_left_pos", 449, 279, 2, 2)
	register_place(   "enter", "gate_right_pos", 509, 279, 2, 2)
	register_place(   "enter", "ikarus_out", 400, 610, 40, 20)
	register_place(   "enter", "ikarus_pos", 293, 590, 2, 2)
	register_place(   "enter", "left_exit", 20, 570, 20, 140)
	register_place(   "enter", "right_exit", 920, 565, 20, 145)
	register_exit("enter", "enter", "right_exit", 0, 570, 20, 140)
	register_exit("enter", "enter", "left_exit", 940, 565, 20, 145)
	
	
	
	locations["enter"].x, locations["enter"].y = 419, 349

