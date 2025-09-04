init 1 python:
	register_location_object('ikarus', 'images/locations/enter/objects/', 'ikarus_main', 'ikarus_free')
	
	register_location_object('gate_left', 'images/locations/enter/objects/', 'gate_left_main', 'gate_free')
	register_location_object('gate_right', 'images/locations/enter/objects/', 'gate_right_main', 'gate_free')
	
	add_location_object("enter", "gate_left_pos", "gate_left")
	add_location_object("enter", "gate_right_pos", "gate_right")
	add_location_object("enter", "ikarus_pos", "ikarus")
