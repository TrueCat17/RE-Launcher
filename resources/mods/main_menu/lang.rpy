init -1000 python:
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
	
	def project__get_config_path():
		return projects_dir + (project.dir or 'RE-Launcher') + '/resources/mods/common/config.rpy'
	
	def get_code_for_set_lang(lang):
		return (
			'init python:\n' +
			'\t' + 'config.default_language = "' + lang + '"\n'
		)
	
	def project__get_language():
		lang, enable_all = config.language, False
		
		config_path = project.get_config_path()
		if os.path.exists(config_path):
			for line in open(config_path, 'rb'):
				tmp_lang, tmp_enable_all = get_language_from_line(str(line, 'utf-8'))
				if tmp_lang:
					lang, enable_all = tmp_lang, tmp_enable_all
		
		return lang, enable_all
	
	def project__update_language():
		tl_path = '/Ren-Engine/rpy/tl/'
		tl_path_launcher = launcher_dir + tl_path
		tl_path_project = projects_dir + project.dir + tl_path
		
		config_path = project.get_config_path()
		if not os.path.exists(config_path):
			with open(config_path, 'wb') as f:
				f.write(bytes(get_code_for_set_lang(project.language), 'utf-8'))
		
		lang, enable_all = project.get_language()
		if not enable_all:
			if os.path.exists(tl_path_project):
				shutil.rmtree(tl_path_project)
			os.mkdir(tl_path_project)
			
			for f in os.listdir(tl_path_launcher):
				if f == lang + '.rpy':
					shutil.copyfile(tl_path_launcher + f, tl_path_project + f)
					break
	
	def project__set_language(lang, out_msg_ok = True):
		project.language = lang
		config_path = project.get_config_path()
		
		if os.path.exists(config_path):
			lines = [str(i, 'utf-8') for i in open(config_path, 'rb')]
		else:
			lines = []
		
		with open(config_path, 'wb') as f:
			was_lang = False
			for line in lines:
				lang, enable_all = get_language_from_line(line)
				if lang:
					was_lang = True
					i = line.rfind('=')
					line = line[:i].rstrip() + ' = "' + project.language + '"' + (' # enable all' if enable_all else '') + '\n'
				f.write(bytes(line, 'utf-8'))
			
			if not was_lang:
				if lines and lines[-1].strip():
					f.write(b'\n')
				f.write(bytes(get_code_for_set_lang(project.language), 'utf-8'))
		
		project.update_language()
		if out_msg_ok:
			notification.out('Language updated')
	
	def project__ask_lang():
		input.ask_str(project.set_language, 'Project Language', project.language, allow = alphabet)
