init python:
	set_fps(20)
	set_can_mouse_hide(False)
	config.has_autosave = False
	
	pause_screen.disable = True
	start_screens = ['hotkeys', 'main_menu']
	
	back_path = 'images/gui/menu/main/back.png'
	mods = get_mods()

screen mods:
	key 'ESCAPE' action HideMenu('mods')
	
	button:
		ground back_path
		hover  back_path
		
		mouse False
		size 1.0
		
		action HideMenu('mods')
	
	vbox:
		align (0.5, 0.5)
		spacing 5
		
		for name, dir_name in mods:
			textbutton name action start_mod(dir_name)

screen main_menu:
	image back_path:
		size 1.0
	
	vbox:
		align (0.5, 0.5)
		spacing 5
		
		textbutton _('New game')    xalign 0.5 action start_mod('std')
		textbutton _('Load')        xalign 0.5 action ShowMenu('load')
		textbutton _('Mods')        xalign 0.5 action ShowMenu('mods')
		textbutton _('Preferences') xalign 0.5 action ShowMenu('preferences')
		textbutton _('Exit')        xalign 0.5 action exit_from_game
