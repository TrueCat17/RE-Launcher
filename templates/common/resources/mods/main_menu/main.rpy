init python:
	set_fps(20)
	set_can_mouse_hide(False)
	config.has_autosave = False
	
	pause_screen.disable = True
	start_screens = ['hotkeys', 'main_menu']
	
	back_path = 'images/gui/menu/main/back.png'

screen mods_with_bg:
	key 'ESCAPE' action HideMenu('mods_with_bg')
	
	button:
		ground back_path
		hover  back_path
		corner_sizes 0
		
		mouse False
		size 1.0
		
		action HideMenu('mods_with_bg')
	
	use mods

screen main_menu:
	image back_path:
		size 1.0
	
	vbox:
		align (0.5, 0.5)
		spacing 5
		
		$ btn_params = (
			(_('New game'), Function(start_mod, 'std')),
			(_('Load'), ShowMenu('load')),
			(_('Mods'), ShowMenu('mods_with_bg')),
			(_('Preferences'), ShowMenu('preferences')),
			(_('Exit'), exit_from_game),
		)
		for text, action in btn_params:
			textbutton text:
				style 'menu_button'
				action action
