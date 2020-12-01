init -100 python:
	
	# pl = projects_list
	pl_page_index = 0
	pl_page_size = 4
	
	# pdl = projects_dir_list
	pdl_page_index = 0
	pdl_page_size = 6
	
	
	launcher_dir = os.path.abspath(get_filename(1)).replace('\\', '/')
	i = launcher_dir.rfind('/resources')
	launcher_dir = launcher_dir[:i]
	
	
	def load_persistent_data():
		global projects_dir, active_project, active_project_language
		
		if persistent.projects_dir is None:
			persistent.projects_dir = os.path.dirname(launcher_dir)
		
		projects_dir = persistent.projects_dir
		active_project = persistent.active_project
		if active_project:
			active_project_language = get_active_project_language()
		else:
			active_project_language = config.language
	
	load_persistent_data()
	
	
	def update_projects(new_dir):
		global projects_dir
		if projects_dir != new_dir:
			projects_dir = persistent.projects_dir = new_dir
			select_project(None)
		
		global projects_dir_list
		projects_dir_list = ['..']
		for d in os.listdir(projects_dir):
			if os.path.isdir(projects_dir + '/' + d):
				projects_dir_list.append(d)
		projects_dir_list.sort()
		
		global projects_list
		projects_list = []
		for d in projects_dir_list:
			if d != '..' and os.path.exists(projects_dir + '/' + d + '/resources/mods'):
				projects_list.append(d)
		projects_list.sort()
		
		global pl_page_index, pdl_page_index
		pl_page_index = pdl_page_index = 0
		
		global pl_page_count
		pl_page_count = int(math.ceil(len(projects_list) / float(pl_page_size)))
		
		global pdl_page_count
		pdl_page_count = int(math.ceil(len(projects_dir_list) / float(pdl_page_size)))
	
	
	def set_default_projects_dir():
		persistent.projects_dir = None
		load_persistent_data()
		update_projects(projects_dir)
	
	
	def select_project(project):
		global active_project, active_project_language
		active_project = persistent.active_project = project
		active_project_language = get_active_project_language()
		stdout_viewer_clear()
	
	update_projects(projects_dir)


init python:
	def open_project_dir():
		directory = projects_dir + '/' + active_project
		if sys.platform == 'win32':
			os.startfile(directory)
		else:
			import subprocess
			if sys.platform == 'darwin':
				subprocess.Popen(["open", directory])
			else:
				subprocess.Popen(["xdg-open", directory])
			
	
	def update_project_engine(out_msg_ok = True):
		if active_project == 'Ren-Engine Launcher':
			notification(_('Disallowed action'))
			return
		
		to_copy = ['Ren-Engine', 'start.exe', 'start.sh']
		
		for path in to_copy:
			old_path = launcher_dir + '/' + path
			new_path = projects_dir + '/' + active_project + '/' + path
			
			try:
				if os.path.isdir(old_path):
					if os.path.exists(new_path):
						shutil.rmtree(new_path)
					shutil.copytree(old_path, new_path)
				else:
					shutil.copyfile(old_path, new_path)
					shutil.copystat(old_path, new_path)
			except:
				notification(_('Error on copy <%s> to <%s>') % (old_path, new_path))
		
		update_active_project_language()
		
		params = open(projects_dir + '/' + active_project + '/resources/params.conf', 'rb')
		for line in params:
			if line.startswith('window_title'):
				s = line.find('=') + 1
				e = line.find('#')
				name = line[s:e].strip()
				break
		else:
			name = 'Ren-Engine'
			notification(_('window_title not found in resources/params.conf'))
		
		exe_path = projects_dir + '/' + active_project + '/Ren-Engine/'
		for f in os.listdir(exe_path):
			if f.endswith('.exe'):
				os.rename(exe_path + f, exe_path + name + '.exe')
				break
		else:
			notification(_('*.exe file not found in /Ren-Engine'))
		
		
		if out_msg_ok:
			notification(_('Ren-Engine updated'))
	
	def start_project():
		root = projects_dir + '/' + active_project
		path = root + '/start.'
		if sys.platform == 'win32':
			path += 'exe'
		else:
			path += 'sh'
		
		env = dict(os.environ, RE_LANG=config.language)
		
		import subprocess
		proc = subprocess.Popen([path], stdout=subprocess.PIPE, cwd=root, close_fds=False, env=env)
		add_proc(proc)
	
	def build_project():
		zip_path = projects_dir + '/' + active_project + '.zip'
		
		import zipfile
		zf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
		for path, dirs, files in os.walk(projects_dir + '/' + active_project):
			project_path = path[len(projects_dir) + 1:]
			if project_path.startswith(active_project + '/var'):
				continue
			
			for f in files:
				zf.write(path + '/' + f, project_path + '/' + f)
			
			if not dirs and not files:
				zf.writestr(project_path + '/empty.txt', '')
		zf.close()
		
		notification(_('Zip built'))
	
	
