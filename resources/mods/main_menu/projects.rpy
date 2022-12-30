init -100 python:
	
	# pl = projects_list
	pl_page_index = 0
	pl_page_size = 4
	
	# pdl = projects_dir_list
	pdl_page_index = 0
	pdl_page_size = 6
	
	
	launcher_dir = os.path.abspath(get_filename(0)).replace('\\', '/')
	i = launcher_dir.rfind('/resources')
	launcher_dir = launcher_dir[:i]
	
	
	def load_persistent_data():
		global projects_dir
		
		if persistent.projects_dir is None or not os.path.exists(persistent.projects_dir):
			if persistent.projects_dir is not None:
				notification.out('Prev projects directory is not exists, set default value')
				persistent.active_project = None
			persistent.projects_dir = os.path.dirname(launcher_dir)
		
		projects_dir = persistent.projects_dir
		project.dir = persistent.active_project
		
		if project.dir and not os.path.exists(projects_dir + '/' + project.dir):
			project.dir = persistent.active_project = None
		if project.dir:
			project.select(project.dir)
	
	
	def update_project_list(new_dir = None):
		global last_update_project_list
		last_update_project_list = get_game_time()
		
		global projects_dir
		if new_dir is None:
			new_dir = projects_dir
		if projects_dir != new_dir:
			projects_dir = persistent.projects_dir = new_dir
			project.select(None)
		
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
		
		global pl_page_size, pdl_page_size
		pl_page_size = int(get_stage_height() * 0.45 / (btn_ysize + 10))
		pdl_page_size = int((get_stage_height() * 0.9 - 200) / (btn_ysize + 10))
		
		global pl_page_count
		pl_page_count = int(math.ceil(len(projects_list) / float(pl_page_size)))
		
		global pdl_page_count
		pdl_page_count = int(math.ceil(len(projects_dir_list) / float(pdl_page_size)))
	
	signals.add('resized_stage', update_project_list)
	
	
	def set_default_projects_dir():
		persistent.projects_dir = None
		load_persistent_data()
		update_project_list(projects_dir)
	
	
	def project__select(project_dir):
		project.dir = persistent.active_project = project_dir
		project.language, project.enable_all = project.get_language()
		stdout_viewer.clear()
		check_exists_files_and_dirs()
	
	def project__open(path = ''):
		path = projects_dir + '/' + project.dir + '/' + path
		if not os.path.exists:
			notification.out(_('Path <%s> not found') % path)
			return
		
		if sys.platform == 'win32':
			os.startfile(path)
		else:
			import subprocess
			if sys.platform == 'darwin':
				subprocess.Popen(["open", path])
			else:
				subprocess.Popen(["xdg-open", path])
	
	def project__get_param(name, project_root = None):
		if project_root is None:
			project_root = projects_dir + '/' + project.dir
		
		params = open(project_root + '/resources/params.conf', 'rb')
		for line in params:
			if line.startswith(name):
				s = line.find('=') + 1
				e = line.find('#')
				return line[s:e].strip()
		return None
	
	def project__update_engine(out_msg_ok = True):
		if project.dir == 'RE-Launcher':
			notification.out('Disallowed action')
			return
		
		root = projects_dir + '/' + project.dir
		
		to_copy = ['Ren-Engine', 'start.exe', 'start.sh']
		for path in to_copy:
			old_path = launcher_dir + '/' + path
			new_path = root + '/' + path
			
			try:
				if os.path.isdir(old_path):
					if os.path.exists(new_path):
						shutil.rmtree(new_path)
					shutil.copytree(old_path, new_path)
				else:
					shutil.copyfile(old_path, new_path)
					shutil.copystat(old_path, new_path)
			except:
				notification.out(_('Error on copy <%s> to <%s>') % (old_path, new_path))
		
		project.update_language()
		
		name = project.get_param('window_title')
		if not name:
			name = 'Ren-Engine'
			notification.out('window_title not found in resources/params.conf')
		
		exe_dir = root + '/Ren-Engine/'
		exe_path = None
		for f in os.listdir(exe_dir):
			if f.endswith('.exe'):
				exe_path = exe_dir + f
				if f != name:
					os.rename(exe_path, exe_dir + name + '.exe')
				break
		else:
			notification.out('*.exe file not found in /Ren-Engine')
		
		icon_path = project.get_param('window_icon')
		if icon_path:
			icon_path = root + '/resources/' + icon_path
			if not os.path.exists(icon_path):
				notification.out('Icon from <params.conf> not found')
			else:
				try:
					ico.set(root + '/start.exe', icon_path)
				except Exception as e:
					notification.out(_('Error on update icon for <%s>: %s') % ('start.exe', str(e)))
		
		if out_msg_ok:
			notification.out('Ren-Engine updated')
	
	def project__start():
		root = projects_dir + '/' + project.dir
		path = root + '/start.'
		if sys.platform == 'win32':
			path += 'exe'
		else:
			path += 'sh'
		
		env = dict(os.environ, RE_LANG=config.language)
		
		import subprocess
		proc = subprocess.Popen([path], stdout=subprocess.PIPE, cwd=root, close_fds=False, env=env)
		stdout_viewer.add_proc(proc)
	
	def project__build():
		zip_path = projects_dir + '/' + project.dir + '.zip'
		
		import zipfile
		zf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
		for path, dirs, files in os.walk(projects_dir + '/' + project.dir):
			project_path = path[len(projects_dir) + 1:]
			if project_path.startswith(project.dir + '/var'):
				continue
			
			for f in files:
				zf.write(path + '/' + f, project_path + '/' + f)
			
			if not dirs and not files:
				zf.writestr(project_path + '/empty.txt', '')
		zf.close()
		
		notification.out('Zip built')
	
	def project__delete_var_directory():
		var = projects_dir + '/' + project.dir + '/var'
		if os.path.exists(var):
			shutil.rmtree(var)
		notification.out('Variable data deleted')

init 1 python:
	build_object('project')
	project.language = 'english'
	
	load_persistent_data()
	update_project_list()
