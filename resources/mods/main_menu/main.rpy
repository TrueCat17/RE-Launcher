init -1000:
	style textbutton:
		ysize 0.053
		font 'Fregat_bold'
		text_size     0.033
		text_size_min 12
		ground im.rect('#08F')
		hover  im.rect('#F80')

init python:
	set_fps(30)
	set_can_mouse_hide(False)
	config.has_autosave = False
	
	pause_screen.disable = True
	start_screens = ['hotkeys', 'main_menu']
	
	
	def upd_props():
		global text_size, icon_size, btn_ysize
		text_size = style.textbutton.get_current('text_size')
		icon_size = min(text_size, 24)
		btn_ysize = style.textbutton.get_current('ysize')
	signals.add('resized_stage', upd_props, priority = -100)
	upd_props()
	
	
	hovered_gradient_name = ''
	hovered_gradient_effect_time = 0.25
	hovered_gradient_times = defaultdict(int)
	
	def update_hovered_gradient():
		last_tick = get_last_tick()
		for name, time in hovered_gradient_times.items():
			if name == hovered_gradient_name:
				time += last_tick
			else:
				time -= last_tick
			hovered_gradient_times[name] = in_bounds(time, 0, hovered_gradient_effect_time)
	signals.add('exit_frame', update_hovered_gradient)
	
	
	
	def get_rounded_gradients(round_top, round_bottom):
		# top part - not rounded, bottom - rounded
		ground = 'images/btn/gradient.png'
		hover  = 'images/btn/gradient_hover.png'
		
		res = []
		for image in (ground, hover):
			w, h = get_image_size(image)
			h2 = h // 2
			h = h2 * 2
			
			top            = im.crop(image, 0, 0,  w, h2)
			bottom_rounded = im.crop(image, 0, h2, w, h2)
			
			top_rounded = im.flip(bottom_rounded, False, True)
			bottom      = im.flip(top,            False, True)
			
			args = [
				(w, h),
				(0, 0),     top_rounded if round_top    else top,
				(0, h2), bottom_rounded if round_bottom else bottom,
			]
			res.append(im.composite(*args))
		return res
	
	gradient_btns = {
		'new':   get_rounded_gradients(False, False),
		'doc':   get_rounded_gradients(False, True),
		'start': get_rounded_gradients(True,  True),
	}
	
	
	def get_gradient(btn_name):
		k = hovered_gradient_times[btn_name] / hovered_gradient_effect_time
		k = round(k * 20) / 20
		
		colors = theme[btn_name + '_btn_colors']
		if type(colors) is str: # not colors, name of real prop of colors
			colors = theme[colors]
		color1, color2 = colors
		
		cache = get_gradient.__dict__
		key = (btn_name, k, color1, color2)
		if key in cache:
			return cache[key]
		
		ground, hover = gradient_btns[btn_name]
		
		gradient = im.composite(
			get_image_size(ground),
			(0, 0), ground,
			(0, 0), im.recolor(hover, 255, 255, 255, 255 * k)
		)
		
		cache[key] = im.matrix_color(gradient, im.matrix.colorize(color1, color2))
		return cache[key]
	
	def get_icon(name, color):
		cache = get_icon.__dict__
		key = (name, icon_size, color)
		
		if key in cache:
			return cache[key]
		
		path = 'images/btn/%s.png' % name
		w, h = get_image_size(path)
		
		xsize = icon_size * w // h
		ysize = icon_size
		
		image = im.renderer_scale(path, xsize, ysize)
		image = im.color(image, color)
		
		cache[key] = (image, (xsize, ysize))
		return cache[key]
	
	
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
	
	
	notification.align = (1.0, 0.0)
	
	
	files_to_open = (
		(
			('std/main.rpy',   'mods/std/main.rpy'),
			('gui.rpy',        'mods/common/gui.rpy'),
			('characters.rpy', 'mods/common/characters.rpy'),
		),
		(
			('config.rpy',  'mods/common/config.rpy'),
			('bg.rpy',      'mods/common/bg.rpy'),
			('sprites.rpy', 'mods/common/sprites.rpy'),
		)
	)
	
	dirs_to_open = (
		('images', 'sound', None),
		('mods',   'fonts', None),
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
				if directory:
					if os.path.exists(root + directory):
						exists_files_and_dirs.append(directory)
	
	set_interval(check_exists_files_and_dirs, 1.0)
	
	
	def get_dotted_line(color, res_width):
		res_width = int(res_width * get_stage_width())
		
		one_width, empty_width, height = 10, 4, 2
		count = res_width // (one_width + empty_width)
		res_width = (one_width + empty_width) * count
		
		cache = get_dotted_line.__dict__
		key = (color, res_width)
		if key in cache:
			return cache[key]
		
		one = im.rect(color, one_width, height)
		args = [(res_width, height)]
		for i in range(count):
			args.append(((one_width + empty_width) * i, 0))
			args.append(one)
		cache[key] = im.composite(*args), (res_width, height)
		return cache[key]
	
	
	prompts = {
		'refresh':           'Refresh list of projects',
		'update':            'Update Launcher',
		'update ren-engine': 'Update the project engine',
		'console':           'Ren-Engine console, Shift+O',
		'doc':               'Copy link',
	}
	
	showed_prompt = ''
	def show_prompt(name):
		global hovered_gradient_name, showed_prompt
		hovered_gradient_name = name
		showed_prompt = prompts.get(name, '')
	def hide_prompt(name):
		global hovered_gradient_name, showed_prompt
		if hovered_gradient_name == name:
			hovered_gradient_name = ''
			showed_prompt = ''
	
	
	icon_btns = {
		'refresh':  update_project_list,
		'update':   check_updates,
		'console':  console.show,
		'settings': ShowScreen('settings'),
		'exit':     exit_from_game,
		'create':   new_project.create,
	}
	
	selected_btn = ''
	def icon_btn_hovered(name):
		global selected_btn
		selected_btn = name
		show_prompt(name)
	def icon_btn_unhovered(name):
		global selected_btn, showed_prompt
		if selected_btn == name:
			selected_btn = ''
			showed_prompt = ''
	
	def on_hide_screen(_screen_name):
		icon_btn_unhovered(selected_btn)
	signals.add('hide_screen', on_hide_screen)
	
	new_doc_btn_params = (
		('new', 'New Project',    ShowScreen('new')),
		('doc', 'Documentation', 'copy_link("doc")'),
	)

init 10 python:
	panel_btn_params = (
		('Start',             project.start),
		('Open directory',    project.open),
		('Update Ren-Engine', project.update_engine),
		('Build/Zip',         project.build),
		('Extra...',          ShowScreen('extra')),
	)

init:
	$ input.reverse_btns = True
	
	style input_button:
		size (100, 25)
		text_size 20
		ground im.round_rect('#08F', 20, 20, 6)
		hover  im.round_rect('#F80', 20, 20, 6)


screen icon_btn(name, xalign = 1.0, yalign = 0, xsize = None, action = None):
	python:
		text = _(screen.name.capitalize())
		
		action = screen.action or icon_btns[screen.name]
		xsize  = screen.xsize  or (icon_size + 10 + get_text_width(text, text_size))
		
		if screen.name == 'refresh':
			ground = hover = btn_transparent
			hbox_xalign = 1.0
		else:
			ground = btn_ground
			hover  = btn_hover
			hbox_xalign = 0.5
	
	size (xsize, btn_ysize)
	align (screen.xalign, screen.yalign)
	
	button:
		size (xsize, btn_ysize)
		
		ground ground
		hover  hover
		
		hovered   icon_btn_hovered(screen.name)
		unhovered icon_btn_unhovered(screen.name)
		action action
		
		hbox:
			xalign hbox_xalign
			yalign 0.5
			spacing 5
			
			python:
				selected = selected_btn == screen.name
				icon_color = theme['icon_hover_color'     if selected else 'icon_ground_color']
				text_color = theme['btn_text_color_hover' if selected else 'btn_text_color']
			
			$ image, size = get_icon(screen.name, icon_color)
			image image:
				yalign 0.5
				size size
			
			text text:
				yalign 0.5
				font  theme.btn_text_font
				color text_color
				text_size text_size


screen main_menu:
	zorder -1
	
	image back_bg:
		size 1.0
	
	image panel_image_cropped:
		corner_sizes -1
		clipping True
		pos  (0.02, 0.02)
		size (0.37, 0.65)
		
		vbox:
			ypos 8
			xsize 0.37
			xalign 0.5
			
			null:
				xsize 0.32
				xalign 0.5
				
				hbox:
					yalign 0.5
					spacing 4
					
					$ image, size = get_icon('stack', theme.text_color)
					image image:
						yalign 0.5
						size size
					
					text _('Projects'):
						yalign 0.5
						font  theme.text_font
						color theme.text_color
						text_size text_size
				
				use icon_btn('refresh')
			
			null ysize 4
			
			$ image, size = get_dotted_line(theme.dotted_line_color, 0.34)
			image image:
				xalign 0.5
				size size
			
			null ysize 8
			
			vbox:
				xalign 0.5
				spacing 8
				alpha 1 if get_game_time() - last_update_project_list > 0.1 else 0
				
				for project_dir in projects_list[pl_page_index * pl_page_size : (pl_page_index + 1) * pl_page_size]:
					textbutton ('   ' + project_dir):
						xsize 0.3
						ground panel_btn_ground
						hover  panel_btn_hover
						font        theme.panel_btn_text_font
						color       theme.panel_btn_text_color
						hover_color theme.panel_btn_text_color_hover
						text_align 'left'
						selected project.dir == project_dir
						action project.select(project_dir)
		
		hbox:
			spacing 8
			xalign 0.5
			ypos 1.0
			yanchor btn_ysize + 8
			alpha 0 if pl_page_count <= 1 else 1
			
			for i in (0, 1, 2):
				if i == 1:
					$ text = '%s/%s' % (pl_page_index + 1, pl_page_count)
					
					image panel_image:
						corner_sizes -1
						xsize get_text_width(text, text_size) + 8
						ysize btn_ysize
						
						text text:
							align 0.5
							font 'Monospace' # for one size of all symbols (numbers in 'Consola' are not aligned)
							color theme.text_color
							text_size text_size
				
				else:
					python:
						if i == 0:
							text = '<'
							action = 'pl_page_index = max(0, pl_page_index - 1)'
							alpha = 0 if pl_page_index == 0 else 1
						else:
							text = '>'
							action = 'pl_page_index = min(pl_page_index + 1, pl_page_count - 1)'
							alpha = 0 if pl_page_index == pl_page_count - 1 else 1
					
					textbutton text:
						xsize btn_ysize
						ground btn_ground
						hover  btn_hover
						font       'Consola' # good '<' and '>' symbols
						color       theme.btn_text_color
						hover_color theme.btn_text_color_hover
						action action
						alpha alpha
	
	vbox:
		xpos 0.02
		ypos int(get_stage_height() * 0.67)
		
		for btn_name, text, action in new_doc_btn_params:
			$ image = get_gradient(btn_name)
			
			button:
				xalign 0.5
				xsize 0.37
				ysize 0.1
				ground image
				hover  image
				action action
				
				hovered   show_prompt(btn_name)
				unhovered hide_prompt(btn_name)
				
				hbox:
					align 0.5
					spacing 5
					
					$ image, size = get_icon(btn_name, theme.panel_btn_text_color_hover)
					image image:
						yalign 0.5
						size size
					
					text _(text):
						yalign 0.5
						font  theme.panel_btn_text_font
						color theme.panel_btn_text_color_hover
						text_size text_size
	
	hbox:
		xpos 16
		ysize 0.13
		yalign 1.0
		spacing 5
		
		image 'images/misc/icon.png':
			size min(64, get_stage_height() // 10)
			yalign 0.5
		text ('Ren-Engine\nver. ' + get_engine_version()):
			font  theme.version_text_font
			color theme.version_text_color
			text_size 18
			yalign 0.5
	
	image panel_image:
		corner_sizes -1
		clipping True
		pos  (0.41, 0.02)
		size (0.57, 0.85)
		
		vbox:
			ypos 10
			xalign 0.5
			
			text (project.dir or '-'):
				xalign 0.5
				font  theme.text_font
				color theme.text_color
				text_size text_size + 6
				ysize btn_ysize
				text_valign 'center'
			
			null ysize 5
			
			$ image, size = get_dotted_line(theme.dotted_line_color, 0.54)
			image image:
				xalign 0.5
				size size
			
			null ysize 10
			
			if project.dir:
				vbox:
					xalign 0.5
					spacing 8
					
					for text, action in panel_btn_params:
						python:
							btn_name = text.lower()
							text = _(text)
							if btn_name == 'start':
								text += ' (F5)'
								ground = hover = get_gradient('start')
								selected = True
							else:
								ground = panel_btn_ground
								hover  = panel_btn_hover
								selected = False
						
						textbutton text:
							xsize 280 / 1200
							ground ground
							hover  hover
							selected selected
							font        theme.panel_btn_text_font
							color       theme.panel_btn_text_color
							hover_color theme.panel_btn_text_color_hover
							action action
							
							hovered   show_prompt(btn_name)
							unhovered hide_prompt(btn_name)
				
				key 'F5' action project.start
				key 'F6' action project.open_log_file
		
		null:
			size (0.57, 0.2)
			yalign 1.0
			
			text _(showed_prompt):
				xsize 0.57
				ypos -5
				yanchor 1.0
				text_size text_size
				text_align 'center'
				font  theme.text_font
				color theme.open_text_color_inactive
			
			image panel_border:
				size (0.57, 2)
			
			vbox:
				xpos 0.25
				xanchor 0.5
				yalign 0.5
				spacing 4
				
				text (_('Open file') + ':'):
					xsize 0.235
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
									if exists:
										hover = open_btn_hover
										color       = theme.open_btn_text_color
										hover_color = theme.open_btn_text_color_hover
									else:
										hover = open_btn_ground
										color = theme.open_text_color_inactive
										hover_color = None
								
								textbutton name:
									xsize 0.125
									ysize text_size + 2
									ground open_btn_ground
									hover  hover
									font theme.open_btn_text_font
									color       color
									hover_color hover_color
									text_size text_size
									mouse exists
									action project.open('resources/' + path) if exists else None
			
			vbox:
				xpos 0.75
				xanchor 0.5
				yalign 0.5
				spacing 4
				
				text (_('Open directory') + ':'):
					xsize 0.235
					text_size text_size
					text_align 'center'
					font  theme.open_text_font
					color theme.open_text_color
				
				hbox:
					xalign 0.5
					
					for directories in dirs_to_open:
						vbox:
							for directory in directories:
								if directory:
									python:
										exists = directory in exists_files_and_dirs
										if exists:
											hover = open_btn_hover
											color       = theme.open_btn_text_color
											hover_color = theme.open_btn_text_color_hover
										else:
											hover = open_btn_ground
											color       = theme.open_text_color_inactive
											hover_color = None
									
									textbutton directory:
										xsize 0.09
										ysize text_size + 2
										ground open_btn_ground
										hover  hover
										font theme.open_btn_text_font
										color       color
										hover_color hover_color
										text_size text_size
										mouse exists
										action project.open('resources/' + directory) if exists else None
								else:
									null:
										xsize 0.09
										ysize text_size + 2
	
	hbox:
		align (0.95, 0.95)
		spacing 5
		
		for btn in ('console', 'update', 'settings', 'exit'):
			use icon_btn(btn)
