init python:
	new_project_name = ''
	new_project_genre = 'vn'
	
	new_project_genres = ('vn', 'rpg', 'other')
	new_project_genre_names = {
		'vn': 'Visual Novell',
		'rpg': 'RPG',
		'other': 'Other',
	}
	
	
	def set_new_project_name(name):
		global new_project_name
		new_project_name = name
	
	def create_new_project():
		if not new_project_name or new_project_name.isspace():
			notification('Input project name')
			return
		
		new_dir = projects_dir + '/' + new_project_name
		if os.path.exists(new_dir):
			notification(_('Directory already exists:\n%s') % new_dir)
			return
		os.mkdir(new_dir)
		
		copy_directory(launcher_dir + '/templates/common/resources', new_dir + '/resources')
		copy_directory(launcher_dir + '/templates/' + new_project_genre + '/resources', new_dir + '/resources')
		select_project(new_project_name)
		update_project_engine(False)
		update_projects(projects_dir)
		
		hide_screen('new')
		notification(_('Project created') + ':\n' + new_dir)
	
	def copy_directory(src, dst):
		if not src.endswith('/'):
			src += '/'
		if not dst.endswith('/'):
			dst += '/'
		
		for path, ds, fs in os.walk(src):
			dst_path = os.path.join(dst, path[len(src):])
			
			for d in ds:
				d = os.path.join(dst_path, d)
				if not os.path.exists(d):
					os.makedirs(d)
			
			for f in fs:
				f_from = os.path.join(path, f)
				f_to   = os.path.join(dst_path, f)
				shutil.copyfile(f_from, f_to)


screen new:
	image back:
		size 1.0
	
	vbox:
		align (0.5, 0.05)
		spacing 20
		xsize 1.0
		
		image im.rect('#F80'):
			xalign 0.5
			size (0.5, 30)
			
			text _('New Project'):
				align 0.5
				color 0
		
		image front:
			xalign 0.5
			size (0.9, 50)
			
			textbutton (_('Name') + ': ' + (new_project_name)):
				align 0.5
				xsize 350
				action ask_str(set_new_project_name, new_project_name)
		
		image front:
			xalign 0.5
			size (0.9, 100)
			
			vbox:
				align 0.5
				spacing 10
				
				text (_('Genre') + ': ' + _(new_project_genre_names[new_project_genre])):
					xalign 0.5
					color 0
				
				hbox:
					xalign 0.5
					spacing 10
					
					for genre in new_project_genres:
						textbutton _(new_project_genre_names[genre]):
							xsize 200
							action SetVariable('new_project_genre', genre)
		
	
	textbutton _('Ready'):
		align (0.95, 0.95)
		action create_new_project
	
	key 'ESCAPE' action Hide('new')
	textbutton _('Return'):
		align (0.05, 0.95)
		action HideScreen('new')
