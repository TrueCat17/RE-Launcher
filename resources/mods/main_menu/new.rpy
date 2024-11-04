init -100 python:
	def new_project__set_name(name):
		new_project.name = name
	
	def new_project__create():
		if not new_project.name or new_project.name.isspace():
			notification.out('Input project name')
			return
		
		new_dir = projects_dir + new_project.name + '/'
		if os.path.exists(new_dir):
			notification.out(_('Directory already exists:\n%s') % new_dir)
			return
		os.mkdir(new_dir)
		
		copy_directory(launcher_dir + 'templates/common/resources', new_dir + 'resources')
		copy_directory(launcher_dir + 'templates/' + new_project.template + '/resources', new_dir + 'resources')
		project.select(new_project.name)
		project.update_engine(False)
		update_project_list(projects_dir)
		project.set_language(config.language, out_msg_ok = False)
		
		hide_screen('new')
		notification.out(_('Project created') + ':\n' + new_dir)
	
	def copy_directory(src, dst):
		src = make_sure_dir(src)
		dst = make_sure_dir(dst)
		
		for path, ds, fs in os.walk(src):
			path = make_sure_dir(path)
			dst_path = dst + path[len(src):]
			
			for d in ds:
				d = dst_path + d
				os.makedirs(d, exist_ok = True)
			
			for f in fs:
				f_from = path + f
				f_to   = dst_path + f
				shutil.copyfile(f_from, f_to)
	
	
	def new_project__show_prompt(template):
		new_project.hovered_template = template
	def new_project__hide_prompt(template):
		if new_project.hovered_template == template:
			new_project.hovered_template = ''
	
	def new_project__get_prompts():
		res = []
		if new_project.hovered_template:
			prompts = new_project.template_prompts[new_project.hovered_template]
			for prompt in prompts:
				prompt = _(prompt)
				if '%s' in prompt:
					template_name = _(new_project.template_names[new_project.hovered_template])
					prompt = prompt % template_name
				res.append(prompt + '.')
		while len(res) < 2:
			res.append('')
		return res
	
	def new_project__hide_screen(screen_name):
		if screen_name == 'new':
			new_project.hovered_template = ''
	signals.add('hide_screen', new_project__hide_screen)
	
	build_object('new_project')
	
	new_project.name = ''
	new_project.template = 'vn'
	
	new_project.templates = ('vn', 'rpg', 'other')
	new_project.template_names = {
		'vn': 'Visual Novell',
		'rpg': 'RPG',
		'other': 'Other',
	}
	
	new_project.template_prompts = {
		'vn': (
			'Options and resources best suited for <%s> games',
			'Mod <Move Sprites> for interactive scene creation',
		),
		'rpg': (
			'Options and resources best suited for <%s> games',
			'Mod <RPG Editor> for more convenient work with locations',
		),
		'other': (
			'No specialized setup',
		)
	}


screen new:
	image im.rect(theme.back_bg_color):
		size 1.0
	
	vbox:
		align (0.5, 0.3)
		spacing text_size
		xsize 1.0
		
		text _('New Project'):
			xalign 0.5
			text_size text_size * 1.5
			font  theme.text_font
			color theme.text_color
		
		null ysize 1
		
		image get_panel():
			corner_sizes 15
			xalign 0.5
			size (0.5, btn_ysize + 20)
			
			$ xsize = get_stage_width() * 2 // 7
			$ color = get_middle_color(theme.new_btn_colors[0], theme.new_btn_colors[1])
			textbutton (_('Name') + ': ' + (new_project.name)):
				align 0.5
				xsize xsize
				ground im.round_rect(color, xsize, btn_ysize, 6)
				font  theme.panel_btn_text_font
				color theme.panel_btn_text_color_hover
				action input.ask_str(new_project.set_name, 'Input project name', new_project.name, allow = alphabet + numbers + '-_.')
		
		image get_panel():
			corner_sizes -1
			xalign 0.5
			size (0.5, len(new_project.templates) * (btn_ysize + 8) + text_size * 6 + 60)
			
			vbox:
				align 0.5
				spacing 8
				
				text _('Template'):
					xalign 0.5
					text_size text_size
					font  theme.text_font
					color theme.text_color
				
				null size 1
				
				vbox:
					xalign 0.5
					spacing 8
					
					for template in new_project.templates:
						textbutton _(new_project.template_names[template]):
							xsize xsize
							ground im.round_rect(theme.panel_btn_ground_color, xsize, btn_ysize, 6)
							hover  im.round_rect(theme.panel_btn_hover_color,  xsize, btn_ysize, 6)
							font        theme.panel_btn_text_font
							color       theme.panel_btn_text_color
							hover_color theme.panel_btn_text_color_hover
							selected new_project.template == template
							action  'new_project.template = template'
							
							hovered   new_project.show_prompt(template)
							unhovered new_project.hide_prompt(template)
				
				null ysize 10
				
				image im.rect(theme.panel_border_color):
					size (0.5, 2)
				
				vbox:
					xpos 20
					
					for prompt in new_project.get_prompts():
						hbox:
							spacing 5
							ysize text_size * 2.3
							
							text '•':
								text_size text_size
								alpha 1 if prompt else 0
								font  theme.open_text_font
								color theme.open_text_color
							
							text prompt:
								text_size text_size
								xsize int(get_stage_width() * 0.5) - 20 * 2 - 5
								ysize text_size * 2.3
								font  theme.open_text_font
								color theme.open_text_color
	
	use icon_btn('create', 0.97, 0.97, get_stage_width() // 8)
	use icon_btn('return', 0.03, 0.97, get_stage_width() // 8, HideScreen('new'))
	
	key 'ESCAPE' action HideScreen('new')
