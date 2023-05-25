init python:
	def ico__make(png_path):
		import struct
		
		if not os.path.exists(ico.tmp_path):
			os.makedirs(ico.tmp_path)
		
		count = 0
		paths = []
		sizes = {}
		sizes[png_path] = get_image_size(png_path)
		w, h = sizes[png_path]
		while min(w, h) >= 16:
			if max(w, h) <= 256:
				path = ico.tmp_path + 'icon-%sx%s' % (w, h) + '.png'
				im.save(png_path, path, w, h)
				
				paths.append(path)
				sizes[path] = (w, h)
			
				count += 1
			w //= 2
			h //= 2
		
		if count == 0:
			raise Exception('Incorrect icon image')
		
		data_sizes = {}
		for path in paths + [png_path]:
			data_sizes[path] = os.path.getsize(path)
		
		if sizes[png_path] == sizes[paths[0]] and data_sizes[png_path] < data_sizes[paths[0]]:
			paths[0] = png_path
		
		header_size = 6
		record_size = 16
		data_offset = header_size + record_size * len(paths)
		
		# ico header
		res = struct.pack('HHH', 0, 1, count)
		
		# records
		for path in paths:
			w, h = sizes[path]
			data_size = data_sizes[path]
			res += struct.pack('BBBBHHII', w % 256, h % 256, 0, 0, 1, 32, data_size, data_offset)
			data_offset += data_size
		
		# datas (pngs)
		for path in paths:
			f = open(path, 'rb')
			png_content = f.read()
			f.close()
			res += png_content
		
		res_path = ico.tmp_path + 'icon.ico'
		f = open(res_path, 'wb')
		f.write(res)
		f.close()
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
		
		f = open(exe_path, 'wb')
		f.write(content)
		f.close()
	
	
	build_object('ico')
	ico.tmp_path = '../var/ico/'

