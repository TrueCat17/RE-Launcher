init -100 python:
	
	# pl = projects_list
	pl_page_index = 0
	pl_page_size = 4
	
	# pdl = projects_dir_list
	pdl_page_index = 0
	pdl_page_size = 6
	
	
	launcher_dir = get_root_dir()
	
	
	def load_persistent_data():
		global projects_dir
		
		if persistent.projects_dir is None or not os.path.exists(persistent.projects_dir):
			if persistent.projects_dir is not None:
				notification.out('Prev projects directory is not exists, set default value')
				persistent.active_project = None
			persistent.projects_dir = os.path.dirname(launcher_dir[:-1]) + '/'
		
		projects_dir = persistent.projects_dir
		project.dir = persistent.active_project
		
		if project.dir and not os.path.exists(projects_dir + project.dir):
			project.dir = persistent.active_project = None
		if project.dir:
			project.select(project.dir)
	
	
	def update_project_list(new_dir = None):
		global last_update_project_list
		last_update_project_list = get_game_time()
		
		global projects_dir
		if new_dir is None:
			new_dir = projects_dir
		new_dir = make_sure_dir(new_dir)
		
		if new_dir.endswith('/../'):
			i = new_dir.rfind('/', 0, -4)
			if i != -1:
				new_dir = new_dir[:i]
			min_path_len = 1 # /
			if sys.platform in ('win32', 'cygwin'):
				min_path_len = 3 # C:/
			if len(new_dir) < min_path_len:
				new_dir += '/'
			new_dir = make_sure_dir(new_dir)
		
		if projects_dir != new_dir:
			projects_dir = persistent.projects_dir = new_dir
			project.select(None)
		
		global projects_dir_list
		projects_dir_list = ['..']
		for d in os.listdir(projects_dir):
			if os.path.isdir(projects_dir + d):
				projects_dir_list.append(d)
		projects_dir_list.sort()
		
		global projects_list
		projects_list = []
		for d in projects_dir_list:
			if d != '..' and os.path.exists(projects_dir + d + '/resources/mods'):
				projects_list.append(d)
		projects_list.sort()
		
		global pl_page_index, pdl_page_index
		pl_page_index = pdl_page_index = 0
		
		global pl_page_size, pdl_page_size
		pl_page_size = int(get_stage_height() * 0.45 / (btn_ysize + 10))
		pdl_page_size = int((get_stage_height() * 0.9 - 200) / (btn_ysize + 10))
		
		global pl_page_count
		pl_page_count = int(math.ceil(len(projects_list) / pl_page_size))
		
		global pdl_page_count
		pdl_page_count = int(math.ceil(len(projects_dir_list) / pdl_page_size))
	
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
		path = projects_dir + project.dir + '/' + path
		if not os.path.exists:
			notification.out(_('Path <%s> not found') % path)
			return
		
		if sys.platform in ('win32', 'cygwin'):
			os.startfile(path)
		else:
			import subprocess
			subprocess.Popen(['xdg-open', path])
	
	def project__get_param(name, project_root = None):
		if project_root is None:
			project_root = projects_dir + project.dir
		
		params = open(project_root + '/resources/params.conf', 'rb')
		for line in params:
			line = str(line, 'utf8')
			if line.startswith(name):
				s = line.find('=') + 1
				e = line.find('#')
				return line[s:e].strip()
		return None
	
	def project__update_engine(out_msg_ok = True):
		if project.dir == 'RE-Launcher':
			notification.out('Disallowed action')
			return
		
		root = projects_dir + project.dir + '/'
		
		name = project.get_param('window_title')
		if not name:
			name = 'Ren-Engine'
			notification.out('window_title not found in resources/params.conf')
		start_exe = name + '.exe'
		start_sh = name + '.sh'
		
		# delete old files
		for fn in ('start.exe', 'start.sh', start_exe, start_sh):
			if os.path.exists(root + fn):
				os.remove(root + fn)
		
		launcher_name = get_from_hard_config('window_title', str)
		
		launcher_start_exe = launcher_name + '.exe'
		launcher_start_sh = launcher_name + '.sh'
		to_copy = ['Ren-Engine', launcher_start_exe, launcher_start_sh]
		for path in to_copy:
			old_path = launcher_dir + path
			new_path = root + path
			
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
		
		os.rename(root + 'Ren-Engine/' + launcher_start_exe, root + 'Ren-Engine/' + start_exe)
		os.rename(root + launcher_start_exe, root + start_exe)
		os.rename(root + launcher_start_sh,  root + start_sh)
		
		icon_path = project.get_param('window_icon')
		if icon_path:
			icon_path = root + '/resources/' + icon_path
			if not os.path.exists(icon_path):
				notification.out('Icon from <params.conf> not found')
			else:
				try:
					ico.set(root + start_exe, icon_path)
				except Exception as e:
					notification.out(_('Error on update icon for <%s>: %s') % (start_exe, e))
		
		if out_msg_ok:
			notification.out('Ren-Engine updated')
	
	def project__start():
		root = projects_dir + project.dir + '/'
		name = project.get_param('window_title')
		
		if sys.platform in ('win32', 'cygwin'):
			ext = '.exe'
		else:
			ext = '.sh'
		
		if not name:
			notification.out('window_title not found in resources/params.conf')
			for fn in os.listdir(root):
				if fn.endswith(ext):
					name, ext = os.path.splitext(fn)
					break
			else:
				notification.out('Execution file not found')
				return
		
		path = root + name + ext
		
		env = dict(os.environ, RE_LANG=config.language)
		
		import subprocess
		proc = subprocess.Popen([path], stdout=subprocess.PIPE, cwd=root, close_fds=False, env=env)
		stdout_viewer.add_proc(proc)
	
	
	def project__build():
		if 'zip_paths' in dont_save:
			return
		
		zip_path = projects_dir + project.dir + '.zip'
		
		var_path = project.dir + '/var'
		
		import zipfile
		zf = dont_save.zf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
		
		zip_paths = dont_save.zip_paths = []
		dont_save.zip_paths_added = 0
		
		for path, dirs, files in os.walk(projects_dir + project.dir):
			path = make_sure_dir(path)
			
			project_path = path[len(projects_dir):]
			if project_path.startswith(var_path):
				continue
			
			for f in dirs + files:
				path_from = path + f
				path_to = project_path + f
				if path_to != var_path:
					zip_paths.append((path_from, path_to))
		
		notification.out(project.get_zip_progress)
		interruptable_while(project.add_to_zip)
	
	def project__get_zip_progress():
		if 'zip_paths' not in dont_save:
			return None
		return int(dont_save.zip_paths_added / len(dont_save.zip_paths) * 100)
	
	def project__add_to_zip():
		if 'zip_paths_added' not in dont_save: # will never be True (no saving/loading in Launcher), but... this is good style
			return True
		
		path_from, path_to = dont_save.zip_paths[dont_save.zip_paths_added]
		dont_save.zip_paths_added += 1
		
		ext_sep_index = path_to.rfind('.')
		ext = path_to[ext_sep_index+1:].lower() if ext_sep_index != -1 else ''
		
		exts_dont_compress = ('zip', 'dll', 'exe', '', 'jpg', 'jpeg', 'png', 'webp', 'mp3', 'ogg', 'woff2')
		compress_by_ext = ext not in exts_dont_compress
		# exceptions (good compression):
		is_cygwin_dll = path_to.endswith('cygwin1.dll')
		in_root = path_to.count('/') == 1 # small exe start file
		
		need_compress = compress_by_ext or is_cygwin_dll or in_root
		dont_save.zf.write(path_from, path_to, compresslevel = 9 if need_compress else 0)
		
		if dont_save.zip_paths_added == len(dont_save.zip_paths):
			dont_save.zf.close()
			del dont_save.zf
			del dont_save.zip_paths
			del dont_save.zip_paths_added
			notification.out('Zip built')
			return True
		
		return False
	
	
	def project__delete_var_directory():
		var = projects_dir + project.dir + '/var'
		if os.path.exists(var):
			shutil.rmtree(var)
		notification.out('Variable data deleted')

init 1 python:
	build_object('project')
	project.language = 'english'
	
	load_persistent_data()
	update_project_list()
