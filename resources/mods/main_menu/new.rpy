init -100 python:
	def new_project__set_name(name):
		new_project.name = name
	
	def new_project__create():
		if not new_project.name or new_project.name.isspace():
			notification.out('Input project name')
			return
		
		new_dir = projects_dir + new_project.name + '/'
		if os.path.exists(new_dir):
			notification.out(_('Directory already exists') + ':\n' + new_dir)
			return
		os.mkdir(new_dir)
		
		common_dir = launcher_dir + 'templates/common/resources'
		spec_dir   = launcher_dir + 'templates/' + new_project.template + '/resources'
		new_resources = new_dir + 'resources'
		shutil.copytree(common_dir, new_resources)
		shutil.copytree(spec_dir,   new_resources, dirs_exist_ok = True)
		
		project.select(new_project.name)
		project.update_engine(False)
		update_project_list(projects_dir)
		project.set_language(config.language, out_msg_ok = False)
		
		new_project.close()
		notification.out(_('Project created') + ':\n' + new_dir)
	
	
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
	
	def new_project__close():
		new_project.hovered_template = ''
		hide_screen('new')
	
	build_object('new_project')
	
	new_project.name = ''
	new_project.template = 'vn'
	
	new_project.template_names = {
		'vn':    'Visual Novell',
		'rpg':   'RPG',
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
	image back_bg:
		size 1.0
	
	vbox:
		align (0.5, 0.3)
		spacing text_size
		
		text _('New Project'):
			xalign 0.5
			text_size text_size * 1.5
			font  theme.text_font
			color theme.text_color
		
		null ysize 1
		
		image panel_image:
			corner_sizes 15
			xsize 0.5
			ysize btn_ysize + 20
			
			textbutton (_('Name') + ': ' + new_project.name):
				align 0.5
				xsize 0.3
				ground like_new_btn_ground
				font  theme.panel_btn_text_font
				color theme.panel_btn_text_color_hover
				action input.ask_str(new_project.set_name, 'Input project name', new_project.name, allow = alphabet + numbers + '-_.')
		
		image panel_image:
			corner_sizes -1
			xsize 0.5
			ysize len(new_project.template_names) * (btn_ysize + 8) + text_size * 6 + 60
			
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
					
					for template, name in new_project.template_names.items():
						textbutton _(name):
							xsize 0.3
							ground panel_btn_ground
							hover  panel_btn_hover
							font        theme.panel_btn_text_font
							color       theme.panel_btn_text_color
							hover_color theme.panel_btn_text_color_hover
							selected new_project.template == template
							action  'new_project.template = template'
							
							hovered   new_project.show_prompt(template)
							unhovered new_project.hide_prompt(template)
				
				null ysize 10
				
				image panel_border:
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
	use icon_btn('return', 0.03, 0.97, get_stage_width() // 8, new_project.close)
	
	key 'ESCAPE' action new_project.close
