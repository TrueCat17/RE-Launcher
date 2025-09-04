init python:
	def ico__make(image_path):
		import struct
		
		if not os.path.exists(ico.tmp_path):
			os.makedirs(ico.tmp_path)
		
		paths = []
		sizes = {}
		w, h = sizes[image_path] = get_image_size(image_path)
		while min(w, h) >= 16:
			if max(w, h) <= 256:
				path = ico.tmp_path + 'icon-%sx%s' % (w, h) + '.png'
				im.save(image_path, path, w, h)
				
				paths.append(path)
				sizes[path] = (w, h)
			w //= 2
			h //= 2
		
		if not paths:
			raise Exception('Incorrect icon image')
		
		data_sizes = {}
		for path in paths + [image_path]:
			data_sizes[path] = os.path.getsize(path)
		
		if sizes[image_path] == sizes[paths[0]] and data_sizes[image_path] < data_sizes[paths[0]]:
			if image_path.lower().endswith('.png'):
				paths[0] = image_path
		
		header_size = 6
		record_size = 16
		data_offset = header_size + record_size * len(paths)
		
		# ico header
		res = struct.pack('HHH', 0, 1, len(paths))
		
		# records
		for path in paths:
			w, h = sizes[path]
			data_size = data_sizes[path]
			res += struct.pack('BBBBHHII', w % 256, h % 256, 0, 0, 1, 32, data_size, data_offset)
			data_offset += data_size
		
		# datas (pngs)
		for path in paths:
			with open(path, 'rb') as f:
				res += f.read()
		
		res_path = ico.tmp_path + 'icon.ico'
		with open(res_path, 'wb') as f:
			f.write(res)
		return res_path
	
	def ico__set(exe_path, icon_path):
		# disabled
		return
		
		# make set of png and build ico with it
		new_icon_path = ico.make(icon_path)
		
		# import, don't use abs-path (error on cygwin)
		cur_path = os.path.dirname(get_filename(0)) + '/'
		cur_path = cur_path.replace('\\', '/')
		
		old_value = sys.dont_write_bytecode
		sys.dont_write_bytecode = True
		sys.path.insert(0, cur_path)
		try:
			from change_icon import change_icons # thanks to renpy project
		finally:
			sys.path.pop(0)
			sys.dont_write_bytecode = old_value
		
		# set icon
		content = change_icons(exe_path, new_icon_path)
		
		with open(exe_path, 'wb') as f:
			f.write(content)
	
	
	build_object('ico')
	ico.tmp_path = '../var/ico/'
