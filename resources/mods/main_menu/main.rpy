init -1000 python:
	btn_ysize = 25
	
	style.textbutton.ysize = btn_ysize
	style.textbutton.text_size = 20
	style.textbutton.font = 'Fregat_bold'
	
	style.textbutton.ground = im.rect('#08F')
	style.textbutton.hover  = im.rect('#F80')

init python:
	set_fps(20)
	set_can_mouse_hide(False)
	config.has_autosave = False
	
	pause_screen.disable = True
	start_screens = ['hotkeys', 'main_menu']
	
	
	input.reverse_btns = True
	style.input_button.ground = im.round_rect('#08F', style.input_button.xsize, style.input_button.ysize, 4)
	style.input_button.hover  = im.round_rect('#F80', style.input_button.xsize, style.input_button.ysize, 4)
	
	console.background_alpha = 0.6
	
	
	def check_updates():
		reus.scan_links()
		reus.check_and_load('')
	
	def show_loading_progress():
		progress = reus.get_loading_progress()
		if not progress:
			return None
		
		loaded, size_to_load = progress
		return '%s: %s/%s %s' % (_('Loaded'), loaded, size_to_load, _('MB'))
	
	signals.add('reus_load', Function(notification.out, show_loading_progress))
	
	
	def open_documentation():
		import webbrowser
		webbrowser.open('https://github.com/TrueCat17/Ren-Engine/wiki')
	
	notification.align = (1.0, 0.0)
	
	
	files_to_open = (
		(
			('std/main.rpy', 'mods/std/main.rpy'),
			('gui.rpy', 'mods/common/gui.rpy'),
			('characters.rpy', 'mods/common/characters.rpy'),
		),
		(
			('config.rpy', 'mods/common/config.rpy'),
			('bg.rpy', 'mods/common/bg.rpy'),
			('sprites.rpy', 'mods/common/sprites.rpy'),
		)
	)
	
	dirs_to_open = (
		('images', 'sound'),
		('mods', 'fonts')
	)
	
	exists_files_and_dirs = []
	def check_exists_files_and_dirs():
		global exists_files_and_dirs
		exists_files_and_dirs = []
		
		if not project.dir:
			return
		
		root = projects_dir + project.dir + '/resources/'
		
		for files in files_to_open:
			for _name, path in files:
				if os.path.exists(root + path):
					exists_files_and_dirs.append(path)
		for directories in dirs_to_open:
			for directory in directories:
				if os.path.exists(root + directory):
					exists_files_and_dirs.append(directory)
	
	set_interval(check_exists_files_and_dirs, 1.0)
	
	
	def get_dotted_line(color, one_width, empty_width, count, height):
		cache = get_dotted_line.__dict__
		key = (color, one_width, count, height)
		if key in cache:
			return cache[key]
		
		one = im.rect(color, one_width, height)
		args = [((one_width + empty_width) * count, height)]
		for i in range(count):
			args.append(((one_width + empty_width) * i, 0))
			args.append(one)
		cache[key] = im.composite(*args)
		return cache[key]


screen main_menu:
	zorder -1
	
	image theme.back_bg:
		size 1.0
	
	image theme.front_bg:
		clipping True
		pos  (0.02, 0.02)
		size (0.47, 0.65)
		
		vbox:
			ypos 10
			xsize 0.47
			xalign 0.5
			spacing 10
			
			null:
				xsize 0.4
				xalign 0.5
				
				text (_('Projects') + ':\n'):
					font  theme.text_font
					color theme.text_color
					text_size 30
					ysize 30
				
				hbox:
					xalign 1.0
					size  (150, 30)
					spacing 7
					
					button:
						yalign 0.5
						size (40, 36)
						ground theme.refresh_btn_ground
						hover  theme.refresh_btn_hover
						action update_project_list()
					text _('Refresh'):
						yalign 0.5
						font  theme.version_text_font
						color theme.text_color
						text_size 20
						ysize 20
			
			image get_dotted_line(theme.text_color, 10, 4, 100, 3):
				size (1400, 3)
			
			vbox:
				xalign 0.5
				spacing 10
				alpha (1 if get_game_time() - last_update_project_list > 0.1 else 0)
				
				for project_dir in projects_list[pl_page_index * pl_page_size : (pl_page_index + 1) * pl_page_size]:
					textbutton project_dir:
						xsize 280
						ground im.round_rect(theme.btn_ground_color, 280, btn_ysize, 4)
						hover  im.round_rect(theme.btn_hover_color,  280, btn_ysize, 4)
						font  theme.btn_text_font
						color theme.btn_text_color
						text_align 'center'
						action project.select(project_dir)
		
		vbox:
			xalign 0.5
			yalign 1.0
			
			null ysize 10
			
			hbox:
				spacing 10
				
				textbutton '<-':
					xsize 50
					yalign 0.5
					ground im.round_rect(theme.btn_ground_color, 50, btn_ysize, 4)
					hover  im.round_rect(theme.btn_hover_color,  50, btn_ysize, 4)
					font  theme.btn_text_font
					color theme.btn_text_color
					action SetVariable('pl_page_index', max(0, pl_page_index - 1))
					alpha 0 if pl_page_index == 0 else 1
				
				text (str(pl_page_index + 1) + '/' + str(pl_page_count)):
					yalign 0.5
					font  theme.text_font
					color theme.text_color
					alpha 0 if pl_page_count <= 1 else 1
				
				textbutton '->':
					xsize 50
					yalign 0.5
					ground im.round_rect(theme.btn_ground_color, 50, btn_ysize, 4)
					hover  im.round_rect(theme.btn_hover_color,  50, btn_ysize, 4)
					font  theme.btn_text_font
					color theme.btn_text_color
					action SetVariable('pl_page_index', min(pl_page_count - 1, pl_page_index + 1))
					alpha 0 if pl_page_count == 0 or pl_page_index == pl_page_count - 1 else 1
			
			null ysize 10
	
	vbox:
		xpos 0.02
		ypos int(get_stage_height() * 0.67 + get_stage_width() * 0.02)
		xsize 0.47
		spacing 10
		
		$ btn_params = (
			(_('New Project'),   Show('new'),        theme.btn_ground_color_active, theme.btn_hover_color_active),
			(_('Check updates'), check_updates,      theme.doc_btn_ground_color,    theme.doc_btn_hover_color),
			(_('Documentation'), open_documentation, theme.doc_btn_ground_color,    theme.doc_btn_hover_color),
		)
		for text, action, ground_color, hover_color in btn_params:
			textbutton text:
				xalign 0.5
				xsize 0.4
				ground im.round_rect(ground_color, int(get_stage_width() * 0.4), btn_ysize, 4)
				hover  im.round_rect(hover_color,  int(get_stage_width() * 0.4), btn_ysize, 4)
				font  theme.btn_text_font
				color theme.btn_text_color
				action action
	
	hbox:
		xpos 16
		ypos get_stage_height() - 16
		yanchor 1.0
		spacing 5
		
		image 'images/misc/icon.png':
			size 64
			yalign 0.5
		text ('Ren-Engine\nver. ' + get_engine_version()):
			font  theme.version_text_font
			color theme.version_text_color
			text_size 18
			yalign 0.5
	
	image theme.front_bg:
		clipping True
		pos  (0.51, 0.02)
		size (0.47, 0.85)
		
		vbox:
			ypos 10
			xalign 0.5
			spacing 10
			
			text (project.dir or '-'):
				xalign 0.5
				font  theme.text_font
				color theme.text_color
				text_size 30
				ysize 30
			
			image get_dotted_line(theme.text_color, 10, 4, 100, 3):
				size (1400, 3)
			
			if project.dir:
				$ btn_params = (
					(_('Start') + ' (F5)',   project.start,         theme.btn_ground_color_active, theme.btn_hover_color_active),
					(_('Open directory'),    project.open,          theme.btn_ground_color, theme.btn_hover_color),
					(_('Update Ren-Engine'), project.update_engine, theme.btn_ground_color, theme.btn_hover_color),
					(_('Build/Zip'),         project.build,         theme.btn_ground_color, theme.btn_hover_color),
					(_('Extra...'),          Show('extra'),         theme.btn_ground_color, theme.btn_hover_color),
				)
				for text, action, ground_color, hover_color in btn_params:
					textbutton text:
						xsize 280
						xalign 0.5
						ground im.round_rect(ground_color, 280, btn_ysize, 4)
						hover  im.round_rect(hover_color,  280, btn_ysize, 4)
						font  theme.btn_text_font
						color theme.btn_text_color
						action action
				
				key 'F5' action project.start
				key 'F6' action Show('stdout_viewer')
		
		image theme.open_bg:
			clipping True
			size (0.47, 0.2)
			yalign 1.0
			
			$ text_size = get_stage_height() // 33
			$ file_btn_xsize = get_stage_width() // 8
			$ dir_btn_xsize = get_stage_width() // 11
			
			image get_dotted_line(theme.open_text_color, 6, 4, 200, 2):
				size (2000, 2)
				ypos text_size + 12
			
			vbox:
				xpos 10
				ypos 5
				spacing get_stage_height() // 45
				
				text (_('Open file') + ':'):
					size (0.235, text_size + 2)
					text_size text_size
					text_align 'center'
					font  theme.open_text_font
					color theme.open_text_color
				
				hbox:
					xalign 0.5
					
					for files in files_to_open:
						vbox:
							for name, path in files:
								python:
									exists = path in exists_files_and_dirs
									ground = im.round_rect(theme.open_btn_ground_color, file_btn_xsize, text_size + 2, 4)
									if exists:
										hover = im.round_rect(theme.open_btn_hover_color, file_btn_xsize, text_size + 2, 4)
									else:
										hover = ground
								textbutton name:
									size (file_btn_xsize, text_size + 2)
									ground ground
									hover  hover
									font  theme.open_btn_text_font
									color theme.open_btn_text_color if exists else theme.open_text_color_inactive
									text_size text_size
									mouse exists
									action project.open('resources/' + path) if exists else None
			
			vbox:
				xalign 1.0
				ypos 5
				spacing get_stage_height() // 45
				
				text (_('Open directory') + ':'):
					size (0.235, text_size + 2)
					text_size text_size
					text_align 'center'
					font  theme.open_text_font
					color theme.open_text_color
				
				hbox:
					xalign 0.5
					
					for directories in dirs_to_open:
						vbox:
							for directory in directories:
								python:
									exists = directory in exists_files_and_dirs
									ground = im.round_rect(theme.open_btn_ground_color, dir_btn_xsize, text_size + 2, 4)
									if exists:
										hover = im.round_rect(theme.open_btn_hover_color, dir_btn_xsize, text_size + 2, 4)
									else:
										hover = ground
								
								textbutton directory:
									size (dir_btn_xsize, text_size + 2)
									ground ground
									hover  hover
									font  theme.open_btn_text_font
									color theme.open_btn_text_color if exists else theme.open_text_color_inactive
									text_size text_size
									mouse exists
									action project.open('resources/' + directory) if exists else None
	
	hbox:
		align (0.95, 0.95)
		spacing 5
		
		$ btn_params = (
			(_('Console'),  console.show),
			(_('Settings'), Show('settings')),
			(_('Exit'),     exit_from_game),
		)
		for text, action in btn_params:
			textbutton text:
				xsize 120
				ground im.round_rect(theme.btn_ground_color, 120, btn_ysize, 4)
				hover  im.round_rect(theme.btn_hover_color,  120, btn_ysize, 4)
				font  theme.btn_text_font
				color theme.btn_text_color
				action action

