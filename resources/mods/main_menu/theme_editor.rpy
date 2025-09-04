init -100 python:
	user_themes = {}
	
	def theme_editor__load():
		if not os.path.exists(theme_editor.path):
			return
		
		with open(theme_editor.path, 'rb') as f:
			code = f.read().decode('utf-8')
			try:
				cmpl = compile(code, theme_editor.path, 'exec')
				eval(cmpl)
			except BaseException as e:
				print(e)
				notification.out('Error on loading of user themes, see var/log.txt')
	
	
	def theme_editor__create():
		if len(user_themes) >= 5:
			notification.out('Too many themes')
			return
		
		orig_name = persistent.theme_name
		i = orig_name.find('-')
		if i != -1:
			orig_name = orig_name[:i]
		
		i = 1
		while True:
			name = '%s-%s' % (orig_name, i)
			if name not in user_themes:
				break
			i += 1
		
		user_themes[name] = Object(theme)
		set_theme(name)
		theme_editor.save()
	
	def theme_editor__remove(name):
		names = list(user_themes.keys())
		index = names.index(name)
		theme_editor.bin_hovered_name = '' if index == len(names) - 1 else names[index + 1]
		
		del user_themes[name]
		if persistent.theme_name == name:
			set_theme('Day')
		theme_editor.save()
	
	
	def theme_editor__rename():
		prompt = 'Input theme name'
		allow = alphabet + alphabet.upper() + numbers + '-_.'
		input.ask_str(theme_editor.set_name, prompt, persistent.theme_name, allow = allow, length = 15)
	
	def theme_editor__set_name(name):
		if not name or name == persistent.theme_name:
			return
		
		if name in themes or name in user_themes:
			notification.out(_('A theme named <%s> already exists'), name)
			return
		
		del user_themes[persistent.theme_name]
		user_themes[name] = theme
		persistent.theme_name = name
		
		theme_editor.save()
	
	def theme_editor__hovered(name):
		theme_editor.hovered_name = name
	def theme_editor__unhovered(name):
		if theme_editor.hovered_name == name:
			theme_editor.hovered_name = ''
	
	def theme_editor__bin_hovered(name):
		theme_editor.bin_hovered_name = name
	def theme_editor__bin_unhovered(name):
		if theme_editor.bin_hovered_name == name:
			theme_editor.bin_hovered_name = ''
	
	def theme_editor__get_bin(name):
		path = 'images/btn/bin.png'
		w, h = get_image_size(path)
		
		selected = theme_editor.bin_hovered_name == name
		color = theme['icon_hover_color' if selected else 'icon_ground_color']
		image = im.color(path, color)
		
		xsize = icon_size * w // h
		ysize = icon_size
		return image, (xsize, ysize)
	
	
	def theme_editor__check_color(color):
		if type(color) is not str:
			return False
		
		if color.startswith('#'):
			color = color[1:]
		
		if len(color) not in (3, 4, 6, 8):
			return False
		
		for c in color:
			if c >= '0' and c <= '9': continue
			if c >= 'A' and c <= 'F': continue
			if c >= 'a' and c <= 'f': continue
			return False
		
		return True
	
	
	def theme_editor__change_prop(name, value):
		if 'font' in name:
			allow = alphabet + alphabet.upper() + numbers + '-_+.()'
		elif 'color' in name:
			allow = numbers + 'abcdefABCDEF'
			if 'colors' in name:
				allow += ', '
		else: # ?!
			return
		
		theme_editor.prop_name = name
		input.ask_str(theme_editor.set_prop, name, value, allow = allow)
	
	def theme_editor__set_prop(value):
		name = theme_editor.prop_name
		
		if 'font' in name:
			for f in os.listdir('fonts'):
				if f.startswith(value + '.'):
					break
			else:
				notification.out(_('Font not found in <%s>'), 'resources/fonts/')
				return
		else:
			value = value.replace(' ', '')
			ref = False
			
			if 'colors' in name:
				if value in ('new_btn_colors', 'doc_btn_colors', 'start_btn_colors'):
					ref = True
					if value == name:
						notification.out('Error')
						return
				else:
					if value.count(',') != 1:
						notification.out('Error')
						return
					colors = value.split(',')
			else:
				colors = [value]
			
			if not ref:
				for color in colors:
					if not theme_editor.check_color(color):
						notification.out('Error')
						return
				
				colors = tuple(('#' + color.lstrip('#')) for color in colors)
				if 'colors' in name:
					value = colors
				else:
					value = colors[0]
		
		theme[name] = value
		
		# update some params by theme params
		set_theme(persistent.theme_name)
		
		theme_editor.save()
	
	
	def theme_editor__save():
		if not user_themes:
			if os.path.exists(theme_editor.path):
				os.remove(theme_editor.path)
			return
		
		content = ''
		for name, theme in user_themes.items():
			content += 'user_themes[%r] = Object(\n' % name
			
			for prop, value in theme.items():
				content += '\t%s = %r,\n' % (prop, value)
			
			content += ')\n\n'
		
		with open(theme_editor.path, 'wb') as f:
			f.write(content.encode('utf-8'))
	
	
	
	build_object('theme_editor')
	
	theme_editor.path = '../var/user_themes.py'
	theme_editor.load()
	
	theme_editor.category = 'back'
	
	theme_editor.props = {
		'back': (
			'back_bg_color',
			'panel_border_color',
			'panel_bg_color',
			'dotted_line_color',
		),
		
		'text': (
			'text_font',
			'text_color',
			'version_text_font',
			'version_text_color',
		),
		
		'btn': (
			'btn_text_font',
			'btn_text_color',
			'btn_text_color_hover',
			'btn_ground_color',
			'btn_hover_color',
		),
		
		'panel_btn': (
			'panel_btn_text_font',
			'panel_btn_text_color',
			'panel_btn_text_color_hover',
			'panel_btn_ground_color',
			'panel_btn_hover_color',
		),
		
		'open_text': (
			'open_text_font',
			'open_text_color',
			'open_text_color_inactive',
		),
		
		'open_btn': (
			'open_btn_text_font',
			'open_btn_text_color',
			'open_btn_text_color_hover',
			'open_btn_ground_color',
			'open_btn_hover_color',
		),
		
		'gradients': (
			'new_btn_colors',
			'doc_btn_colors',
			'start_btn_colors',
		),
		
		'other': (
			'icon_ground_color',
			'icon_hover_color',
			'input_fog_color',
		),
	}


screen theme_editor:
	zorder 10000
	modal True
	
	image back_bg:
		size 1.0
	
	python:
		indent = get_stage_width() // 70
		
		panel_ysize = (get_stage_height() - indent * 3) // 2
		panel_xsize3 = panel_ysize * 3               # props
		panel_xsize1 = (panel_xsize3 - indent) // 2  # theme names
		panel_xsize2 = panel_xsize1                  # categories
		
		btn_font        = theme.panel_btn_text_font
		btn_color       = theme.panel_btn_text_color
		btn_hover_color = theme.panel_btn_text_color_hover
		
		selected_user_theme = persistent.theme_name if persistent.theme_name in user_themes else ''
	
	text _('Editor'):
		align 0.03
		xsize 0.125
		text_align  'center'
		text_valign 'center'
		font  theme.text_font
		color theme.text_color
		text_size text_size * 1.5
	
	vbox:
		spacing indent
		ypos indent
		xpos get_stage_width() - indent
		xanchor 1.0
		
		hbox:
			spacing indent
			
			image panel_image:
				corner_sizes -1
				xsize panel_xsize1
				ysize panel_ysize
				yalign 0.5
				
				vbox:
					xalign 0.5
					ypos indent
					spacing 8
					
					for name in list(user_themes.keys()): # copy, because can remove
						hbox:
							spacing 8
							
							textbutton name:
								yalign 0.5
								xsize panel_xsize1 - btn_ysize - indent * 2 - 8
								ground panel_btn_ground
								hover  panel_btn_hover
								font        btn_font
								color       btn_color
								hover_color btn_hover_color
								selected name == selected_user_theme
								action set_theme(name)
							
							button:
								yalign 0.5
								size btn_ysize
								ground panel_btn_ground
								hover  panel_btn_hover
								action theme_editor.remove(name)
								
								hovered   theme_editor.bin_hovered(name)
								unhovered theme_editor.bin_unhovered(name)
								
								$ image, size = theme_editor.get_bin(name)
								image image:
									align 0.5
									size size
				
				textbutton _('Create'):
					xalign 0.5
					ypos    panel_ysize - indent
					yanchor 1.0
					action theme_editor.create
					
					xsize panel_xsize1 // 2
					ground panel_btn_ground
					hover  panel_btn_hover
					font        btn_font
					color       btn_color
					hover_color btn_hover_color
			
			
			image panel_image:
				corner_sizes -1
				xsize panel_xsize2
				ysize panel_ysize
				
				hbox:
					spacing 8
					pos indent
					alpha 1 if selected_user_theme else 0
					
					for i in (0, 1):
						vbox:
							spacing 8
							xalign 0.5
							
							for category in list(theme_editor.props.keys())[i * 4 : (i + 1) * 4]:
								textbutton category:
									xsize (panel_xsize2 - indent * 2 - 8) // 2
									ground panel_btn_ground
									hover  panel_btn_hover
									font        btn_font
									color       btn_color
									hover_color btn_hover_color
									selected theme_editor.category == category
									action  'theme_editor.category = category'
				
				textbutton _('Rename'):
					xalign 0.5
					ypos    panel_ysize - indent
					yanchor 1.0
					alpha 1 if selected_user_theme else 0
					action theme_editor.rename
					
					xsize panel_xsize2 // 2
					ground panel_btn_ground
					hover  panel_btn_hover
					font        btn_font
					color       btn_color
					hover_color btn_hover_color
		
		
		image panel_image:
			corner_sizes -1
			xsize panel_xsize3
			ysize panel_ysize
			
			vbox:
				spacing 8
				xalign 0.5
				ypos indent
				alpha 1 if selected_user_theme else 0
				
				for prop in theme_editor.props[theme_editor.category]:
					button:
						xsize panel_xsize3 - indent * 2
						ysize btn_ysize
						ground panel_btn_ground
						hover  panel_btn_hover
						
						hovered   theme_editor.hovered(prop)
						unhovered theme_editor.unhovered(prop)
						
						$ color = btn_color if theme_editor.hovered_name != prop else btn_hover_color
						
						text prop:
							xpos 0.05
							yalign 0.5
							font  btn_font
							color color
							text_size text_size
						
						python:
							value = theme[prop]
							str_value = str(value)
							for c in '()"\'':
								str_value = str_value.replace(c, '')
						
						action theme_editor.change_prop(prop, str_value)
						
						
						hbox:
							spacing 8
							xpos 0.95
							xanchor 1.0
							yalign 0.5
							
							text str_value:
								yalign 0.5
								font  str_value if 'font' in prop else 'Monospace'
								color color
								text_size text_size
							
							python:
								colors = []
								if 'colors' in prop:
									if type(value) is str:
										value = theme[value]
									if type(value) in (tuple, list):
										colors = value
								elif 'color' in prop:
									if type(value) is str:
										colors = [value]
							
							for color in colors:
								if theme_editor.check_color(color):
									image im.rect(color):
										size btn_ysize * 4 // 5
	
	
	use icon_btn('return', 0.03, 0.97, get_stage_width() // 8, HideScreen('theme_editor'))
	
	if not has_screen('input'):
		key 'ESCAPE' action Function(set_timeout, HideScreen('theme_editor'), 0.1)
