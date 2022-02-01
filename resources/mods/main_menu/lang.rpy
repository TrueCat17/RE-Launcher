init -1000 python:
	active_project_language = 'english'
	
	def get_language_from_line(line):
		if ('config.default_language' not in line) or ('=' not in line):
			return None, False
		
		parts = line.split('=')
		value = parts[-1].strip()
		enable_all = value.endswith('enable all')
		try:
			return eval(value, {}), enable_all
		except:
			return None, enable_all
	
	def get_active_config_path():
		return projects_dir + '/' + active_project + '/resources/mods/common/config.rpy'
	
	def get_code_for_set_lang(lang):
		return (
			'init python:\n' +
			'\t' + 'config.default_language = "' + lang + '"\n'
		)
	
	def get_active_project_language():
		lang, enable_all = config.language, False
		
		config_path = get_active_config_path()
		if os.path.exists(config_path):
			for line in open(config_path, 'rb'):
				tmp_lang, tmp_enable_all = get_language_from_line(line)
				if tmp_lang:
					lang, enable_all = tmp_lang, tmp_enable_all
		
		return lang, enable_all
	
	def update_active_project_language():
		tl_path = '/Ren-Engine/rpy/tl/'
		tl_path_launcher = launcher_dir + '/' + tl_path
		tl_path_active = projects_dir + '/' + active_project + tl_path
		
		config_path = get_active_config_path()
		if not os.path.exists(config_path):
			f = open(config_path, 'wb')
			f.write(get_code_for_set_lang(active_project_language))
		
		lang, enable_all = get_active_project_language()
		if not enable_all:
			if os.path.exists(tl_path_active):
				shutil.rmtree(tl_path_active)
			os.mkdir(tl_path_active)
			
			for f in os.listdir(tl_path_launcher):
				if f.endswith(lang + '.rpy'):
					shutil.copyfile(tl_path_launcher + f, tl_path_active + f)
					break
	
	def set_active_project_language(lang):
		global active_project_language
		active_project_language = lang
		
		config_path = get_active_config_path()
		
		if os.path.exists(config_path):
			lines = open(config_path, 'rb').readlines()
		else:
			lines = []
		
		f = open(config_path, 'wb')
		was_lang = False
		for line in lines:
			lang, enable_all = get_language_from_line(line)
			if lang:
				was_lang = True
				i = line.rfind('=')
				line = line[:i].rstrip() + ' = "' + active_project_language + '"' + (' # enable all' if enable_all else '') + '\n'
			f.write(line)
		
		if not was_lang:
			if lines and lines[-1].strip():
				f.write('\n')
			f.write(get_code_for_set_lang(active_project_language))
		
		update_active_project_language()
		notification('Language updated')
	
	
