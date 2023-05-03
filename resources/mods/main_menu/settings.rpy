init python:
	k = get_from_hard_config("window_w_div_h", float)
	settings_resolutions = tuple((i, int(i/k)) for i in (960, 1200, 1366))

screen settings:
	image theme.back_bg:
		size 1.0
	
	vbox:
		pos (0.02, 0.02)
		spacing int(0.02 * get_stage_width())
		
		image theme.front_bg:
			size (0.47, 120)
			
			vbox:
				align 0.5
				spacing 10
				
				text _('Window size'):
					xalign 0.5
					text_size 24
					font  theme.text_font
					color theme.text_color
				
				for i in (0, 1):
					hbox:
						xalign 0.5
						spacing 5
						
						for w, h in settings_resolutions[i * 2 : (i + 1) * 2]:
							textbutton ('%sx%s' % (w, h)):
								xsize 120
								ground im.round_rect(theme.btn_ground_color, 120, btn_ysize, 4)
								hover  im.round_rect(theme.btn_hover_color,  120, btn_ysize, 4)
								action set_stage_size(w, h)
		
		image theme.front_bg:
			size (0.47, 120)
			
			vbox:
				align 0.5
				spacing 10
				
				text 'Language':
					xalign 0.5
					text_size 24
					font  theme.text_font
					color theme.text_color
				
				hbox:
					xalign 0.5
					spacing 10
					
					for lang in ('english', 'russian'):
						textbutton lang:
							xsize 120
							ground im.round_rect(theme.btn_ground_color, 120, btn_ysize, 4)
							hover  im.round_rect(theme.btn_hover_color,  120, btn_ysize, 4)
							action Language(lang)
		
		image theme.front_bg:
			size (0.47, 200)
			
			vbox:
				align 0.5
				spacing 10
				
				text _('Themes'):
					xalign 0.5
					text_size 24
					font  theme.text_font
					color theme.text_color
				
				for i in themes:
					python:
						if i.name == theme.name:
							ground_color = theme.btn_ground_color_active
							hover_color  = theme.btn_hover_color_active
						else:
							ground_color = theme.btn_ground_color
							hover_color  = theme.btn_hover_color
					textbutton _(i.name):
						xsize 140
						ground im.round_rect(ground_color, 140, btn_ysize, 4)
						hover  im.round_rect(hover_color,  140, btn_ysize, 4)
						action set_theme(i.name)
	
	image theme.front_bg:
		clipping True
		pos  (0.51, 0.02)
		size (0.47, 0.95)
		
		vbox:
			ypos 10
			xsize 0.47
			xalign 0.5
			spacing 10
			
			null:
				xsize 0.4
				xalign 0.5
				
				text _('Projects directory'):
					size (0.4, 24)
					yalign 0.5
					text_size 24
					font  theme.text_font
					color theme.text_color
				
				textbutton _('Default'):
					align (1.0, 0.5)
					size (100, 24)
					ground im.round_rect(theme.btn_ground_color, 100, 24, 4)
					hover  im.round_rect(theme.btn_hover_color,  100, 24, 4)
					font  theme.btn_text_font
					color theme.btn_text_color
					action set_default_projects_dir
			
			image get_dotted_line(theme.text_color, 8, 3, 100, 3):
				size (1100, 3)
			
			image theme.open_bg:
				size (0.45, 60)
				xalign 0.5
				
				text projects_dir:
					xpos 5
					xsize 0.4
					align 0.5
					font  theme.open_text_font
					color theme.open_text_color
			
			null size 10
			
			hbox:
				xalign 0.5
				spacing 10
				
				textbutton '<-':
					xsize 50
					ground im.round_rect(theme.btn_ground_color, 50, btn_ysize, 4)
					hover  im.round_rect(theme.btn_hover_color,  50, btn_ysize, 4)
					font  theme.btn_text_font
					color theme.btn_text_color
					action SetVariable('pdl_page_index', max(0, pdl_page_index - 1))
					alpha 0 if pdl_page_index == 0 else 1
				
				text (str(pdl_page_index + 1) + '/' + str(pdl_page_count)):
					font  theme.text_font
					color theme.text_color
					alpha 0 if pdl_page_count <= 1 else 1
				
				textbutton '->':
					xsize 50
					ground im.round_rect(theme.btn_ground_color, 50, btn_ysize, 4)
					hover  im.round_rect(theme.btn_hover_color,  50, btn_ysize, 4)
					font  theme.btn_text_font
					color theme.btn_text_color
					action SetVariable('pdl_page_index', min(pdl_page_count - 1, pdl_page_index + 1))
					alpha 0 if pdl_page_count == 0 or pdl_page_index == pdl_page_count - 1 else 1
			
			vbox:
				xsize 0.5
				xalign 0.5
				spacing 10
				
				for directory in projects_dir_list[pdl_page_index * pdl_page_size : (pdl_page_index + 1) * pdl_page_size]:
					textbutton directory:
						xalign 0.5
						xsize 300
						ground im.round_rect(theme.btn_ground_color, 300, btn_ysize, 4)
						hover  im.round_rect(theme.btn_hover_color,  300, btn_ysize, 4)
						action update_project_list(os.path.join(projects_dir, directory))
	
	
	key 'ESCAPE' action HideScreen('settings')
	textbutton _('Return'):
		align (0.03, 0.97)
		xsize 150
		ground im.round_rect(theme.btn_ground_color, 150, btn_ysize, 4)
		hover  im.round_rect(theme.btn_hover_color,  150, btn_ysize, 4)
		action HideScreen('settings')

