init python:
	k = get_from_hard_config('window_w_div_h', float)
	settings_resolutions = tuple((i, int(i/k)) for i in (960, 1200, 1366))

screen settings:
	image back_bg:
		size 1.0
	
	vbox:
		pos (0.02, 0.02)
		spacing text_size
		
		image panel_image:
			corner_sizes -1
			xsize 0.47
			ysize btn_ysize * 2 + 16 + text_size * 2
			
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
						
						for w, h in settings_resolutions[i * 2 : (i + 1) * 2]:
							textbutton ('%sx%s' % (w, h)):
								xsize 0.1
								ground panel_btn_ground
								hover  panel_btn_hover
								font        theme.panel_btn_text_font
								color       theme.panel_btn_text_color
								hover_color theme.panel_btn_text_color_hover
								selected get_stage_size() == (w, h)
								action set_stage_size(w, h)
		
		image panel_image:
			corner_sizes -1
			xsize 0.47
			ysize btn_ysize + 8 + text_size * 2
			
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
					
					for lang in ('english', 'russian'):
						textbutton lang:
							xsize 0.1
							ground panel_btn_ground
							hover  panel_btn_hover
							font        theme.panel_btn_text_font
							color       theme.panel_btn_text_color
							hover_color theme.panel_btn_text_color_hover
							selected config.language == lang
							action Language(lang)
		
		image panel_image:
			corner_sizes -1
			xsize 0.47
			ysize btn_ysize * 3 + 24 + text_size * 2
			
			vbox:
				align 0.5
				spacing 8
				
				text _('Themes'):
					xalign 0.5
					font  theme.text_font
					color theme.text_color
					text_size text_size
				
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
										panel_btn_ground,
										panel_btn_hover,
										theme.panel_btn_text_color,
									])
								if len(btn_params) != 3:
									btn_params.append([
										'Editor',
										ShowScreen('theme_editor'),
										like_new_btn_ground,
										like_new_btn_hover,
										theme.panel_btn_text_color_hover,
									])
							
							for name, action, ground, hover, color in btn_params:
								textbutton _(name):
									xsize 0.1
									ground ground
									hover  hover
									font        theme.panel_btn_text_font
									color       color
									hover_color theme.panel_btn_text_color_hover
									selected name == persistent.theme_name
									action action
	
	image panel_image:
		corner_sizes -1
		clipping True
		pos  (0.51, 0.02)
		size (0.47, 0.95)
		
		vbox:
			xsize 0.47
			xalign 0.5
			ypos    text_size // 2
			spacing text_size // 2
			
			null:
				xsize 0.4
				xalign 0.5
				
				text _('Directory of projects'):
					xsize 0.4
					font  theme.text_font
					color theme.text_color
					text_size text_size
				
				textbutton _('Reset'):
					xsize 0.08
					xalign 1.0
					ysize text_size + 4
					ground like_doc_btn_ground
					font  theme.panel_btn_text_font
					color theme.panel_btn_text_color_hover
					action set_default_projects_dir
			
			image panel_image:
				corner_sizes 15
				xsize 0.45
				ysize text_size * 3
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
						
						image panel_image:
							corner_sizes -1
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
							xsize btn_ysize
							ground btn_ground
							hover  btn_hover
							font       'Consola'
							color       theme.btn_text_color
							hover_color theme.btn_text_color_hover
							action action
							alpha alpha
			
			vbox:
				xsize 0.5
				xalign 0.5
				spacing 8
				
				for directory in projects_dir_list[pdl_page_index * pdl_page_size : (pdl_page_index + 1) * pdl_page_size]:
					textbutton directory:
						xalign 0.5
						xsize 0.25
						ground panel_btn_ground
						hover  panel_btn_hover
						font        theme.panel_btn_text_font
						color       theme.panel_btn_text_color
						hover_color theme.panel_btn_text_color_hover
						action update_project_list(projects_dir + directory)
	
	use icon_btn('return', 0.03, 0.97, get_stage_width() // 8, HideScreen('settings'))
	
	key 'ESCAPE' action HideScreen('settings')
