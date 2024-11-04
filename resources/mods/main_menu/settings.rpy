init python:
	k = get_from_hard_config('window_w_div_h', float)
	settings_resolutions = tuple((i, int(i/k)) for i in (960, 1200, 1366))

screen settings:
	image im.rect(theme.back_bg_color):
		size 1.0
	
	vbox:
		pos (0.02, 0.02)
		spacing text_size
		
		image get_panel():
			corner_sizes -1
			size (0.47, btn_ysize * 2 + 20 + text_size * 2)
			
			vbox:
				align 0.5
				spacing 8
				
				text _('Window size'):
					xalign 0.5
					font  theme.text_font
					color theme.text_color
					text_size text_size
				
				for i in (0, 1):
					hbox:
						xalign 0.5
						spacing 8
						
						$ xsize = get_stage_width() // 10
						for w, h in settings_resolutions[i * 2 : (i + 1) * 2]:
							textbutton ('%sx%s' % (w, h)):
								xsize xsize
								ground im.round_rect(theme.panel_btn_ground_color, xsize, btn_ysize, 6)
								hover  im.round_rect(theme.panel_btn_hover_color,  xsize, btn_ysize, 6)
								font        theme.panel_btn_text_font
								color       theme.panel_btn_text_color
								hover_color theme.panel_btn_text_color_hover
								selected get_stage_size() == (w, h)
								action set_stage_size(w, h)
		
		image get_panel():
			corner_sizes -1
			size (0.47, btn_ysize + 20 + text_size * 2)
			
			vbox:
				align 0.5
				spacing 8
				
				text 'Language':
					xalign 0.5
					font  theme.text_font
					color theme.text_color
					text_size text_size
				
				hbox:
					xalign 0.5
					spacing 8
					
					$ xsize = get_stage_width() // 10
					for lang in ('english', 'russian'):
						textbutton lang:
							xsize xsize
							ground im.round_rect(theme.panel_btn_ground_color, xsize, btn_ysize, 6)
							hover  im.round_rect(theme.panel_btn_hover_color,  xsize, btn_ysize, 6)
							font        theme.panel_btn_text_font
							color       theme.panel_btn_text_color
							hover_color theme.panel_btn_text_color_hover
							selected config.language == lang
							action Language(lang)
		
		image get_panel():
			corner_sizes -1
			size (0.47, btn_ysize * 3 + 16 + 20 + text_size * 2)
			
			vbox:
				align 0.5
				spacing 8
				
				text _('Themes'):
					xalign 0.5
					font  theme.text_font
					color theme.text_color
					text_size text_size
				
				$ xsize = get_stage_width() // 10
				$ ground = im.round_rect(theme.panel_btn_ground_color, xsize, btn_ysize, 6)
				$ hover  = im.round_rect(theme.panel_btn_hover_color,  xsize, btn_ysize, 6)
				
				hbox:
					spacing 8
					
					$ theme_names = list(themes.keys())
					for i in (0, 1):
						vbox:
							spacing 8
							
							python:
								btn_params = []
								for name in theme_names[i*3 : (i+1)*3]:
									btn_params.append([
										name,
										Function(set_theme, name),
										ground,
										hover,
										theme.panel_btn_text_color,
									])
								if len(btn_params) != 3:
									color = get_middle_color(theme.new_btn_colors[0], theme.new_btn_colors[1])
									ground = im.round_rect(color, xsize, btn_ysize, 6)
									hover  = im.matrix_color(ground, im.matrix.brightness(0.1))
									btn_params.append([
										'Editor',
										ShowScreen('theme_editor'),
										ground,
										hover,
										theme.panel_btn_text_color_hover,
									])
							
							for name, action, ground, hover, color in btn_params:
								textbutton _(name):
									xsize xsize
									ground ground
									hover  hover
									font        theme.panel_btn_text_font
									color       color
									hover_color theme.panel_btn_text_color_hover
									selected name == persistent.theme_name
									action action
	
	image get_panel():
		corner_sizes -1
		clipping True
		pos  (0.51, 0.02)
		size (0.47, 0.95)
		
		vbox:
			ypos 10
			xsize 0.47
			xalign 0.5
			spacing text_size // 2
			
			null:
				xsize 0.4
				xalign 0.5
				
				text _('Projects directory'):
					xsize 0.4
					yalign 0.5
					font  theme.text_font
					color theme.text_color
					text_size text_size
				
				$ xsize = get_stage_width() // 12
				$ color = get_middle_color(theme.doc_btn_colors[0], theme.doc_btn_colors[1])
				textbutton _('Default'):
					align (1.0, 0.5)
					xsize xsize
					ground im.round_rect(color, xsize, btn_ysize, 6)
					font  theme.btn_text_font
					color theme.btn_text_color_hover
					action set_default_projects_dir
			
			image get_panel():
				corner_sizes 15
				size (0.45, text_size * 3)
				xalign 0.5
				
				text projects_dir:
					xsize 0.4
					align 0.5
					font  theme.open_text_font
					color theme.open_text_color
					text_size text_size
			
			hbox:
				xalign 0.5
				spacing 8
				alpha 0 if pdl_page_count <= 1 else 1
				
				for i in (0, 1, 2):
					if i == 1:
						$ text = '%s/%s' % (pdl_page_index + 1, pdl_page_count)
						
						image get_panel():
							corner_sizes -1
							yalign 0.5
							xsize get_text_width(text, text_size) + 8
							ysize btn_ysize
							
							text text:
								align 0.5
								font 'Monospace'
								color theme.text_color
								text_size text_size
					else:
						python:
							if i == 0:
								text = '<'
								action = 'pdl_page_index = max(0, pdl_page_index - 1)'
								alpha = 0 if pdl_page_index == 0 else 1
							else:
								text = '>'
								action = 'pdl_page_index = min(pdl_page_index + 1, pdl_page_count - 1)'
								alpha = 0 if pdl_page_index == pdl_page_count - 1 else 1
						
						textbutton text:
							yalign 0.5
							xsize btn_ysize
							ground im.round_rect(theme.btn_ground_color, btn_ysize, btn_ysize, 6)
							hover  im.round_rect(theme.btn_hover_color,  btn_ysize, btn_ysize, 6)
							font       'Consola'
							color       theme.btn_text_color
							hover_color theme.btn_text_color_hover
							action action
							alpha alpha
			
			vbox:
				xsize 0.5
				xalign 0.5
				spacing 8
				
				$ xsize = get_stage_width() // 4
				for directory in projects_dir_list[pdl_page_index * pdl_page_size : (pdl_page_index + 1) * pdl_page_size]:
					textbutton directory:
						xalign 0.5
						xsize xsize
						ground im.round_rect(theme.panel_btn_ground_color, xsize, btn_ysize, 6)
						hover  im.round_rect(theme.panel_btn_hover_color,  xsize, btn_ysize, 6)
						font        theme.panel_btn_text_font
						color       theme.panel_btn_text_color
						hover_color theme.panel_btn_text_color_hover
						action update_project_list(os.path.join(projects_dir, directory))
	
	use icon_btn('return', 0.03, 0.97, get_stage_width() // 8, HideScreen('settings'))
	
	key 'ESCAPE' action HideScreen('settings')
