init python:
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
		copy_directory(launcher_dir + 'templates/' + new_project.genre + '/resources', new_dir + 'resources')
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
	
	
	build_object('new_project')
	
	new_project.name = ''
	new_project.genre = 'vn'
	
	new_project.genres = ('vn', 'rpg', 'other')
	new_project.genre_names = {
		'vn': 'Visual Novell',
		'rpg': 'RPG',
		'other': 'Other',
	}


screen new:
	image theme.back_bg:
		size 1.0
	
	vbox:
		align (0.5, 0.15)
		spacing 20
		xsize 1.0
		
		image im.rect(theme.btn_ground_color_active):
			xalign 0.5
			size (0.35, 35)
			
			text _('New Project'):
				align 0.5
				text_size 24
				font  theme.open_text_font
				color theme.open_text_color
		
		null size 10
		
		image theme.front_bg:
			xalign 0.5
			size (0.5, 50)
			
			textbutton (_('Name') + ': ' + (new_project.name)):
				align 0.5
				xsize 350
				ground im.round_rect(theme.btn_ground_color, 350, btn_ysize, 4)
				hover  im.round_rect(theme.btn_hover_color,  350, btn_ysize, 4)
				font  theme.btn_text_font
				color theme.btn_text_color
				action input.ask_str(new_project.set_name, '', new_project.name, allow = alphabet + numbers + '-_.')
		
		image theme.front_bg:
			xalign 0.5
			size (0.5, 180)
			
			vbox:
				align 0.5
				spacing 10
				
				text (_('Genre') + ': ' + _(new_project.genre_names[new_project.genre])):
					xalign 0.5
					text_size 24
					font  theme.text_font
					color theme.text_color
				
				null size 1
				
				vbox:
					xalign 0.5
					spacing 10
					
					for genre in new_project.genres:
						textbutton _(new_project.genre_names[genre]):
							xsize 250
							ground im.round_rect(theme.btn_ground_color, 250, btn_ysize, 4)
							hover  im.round_rect(theme.btn_hover_color,  250, btn_ysize, 4)
							font  theme.btn_text_font
							color theme.btn_text_color
							action SetVariable('new_project.genre', genre)
		
	
	textbutton _('Ready'):
		align (0.97, 0.97)
		xsize 150
		ground im.round_rect(theme.btn_ground_color, 150, btn_ysize, 4)
		hover  im.round_rect(theme.btn_hover_color,  150, btn_ysize, 4)
		font  theme.btn_text_font
		color theme.btn_text_color
		action new_project.create
	
	key 'ESCAPE' action Hide('new')
	textbutton _('Return'):
		align (0.03, 0.97)
		xsize 150
		ground im.round_rect(theme.btn_ground_color, 150, btn_ysize, 4)
		hover  im.round_rect(theme.btn_hover_color,  150, btn_ysize, 4)
		font  theme.btn_text_font
		color theme.btn_text_color
		action HideScreen('new')
