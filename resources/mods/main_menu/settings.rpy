init python:
	k = get_from_hard_config("window_w_div_h", float)
	settings_resolutions = tuple((i, int(i/k)) for i in (640, 960, 1200, 1366, 1920))

screen settings:
	image back:
		size 1.0
	
	image front:
		pos (0.02, 0.02)
		size (0.47, 0.95)
		
		vbox:
			pos 10
			spacing 10
			
			text (_('Projects directory') + ':\n{color=0}' + projects_dir):
				text_size 20
				xsize 0.4
			
			null:
				xalign 0.5
				xsize 0.45
				
				hbox:
					spacing 10
					
					textbutton '<-':
						action SetVariable('pdl_page_index', max(0, pdl_page_index - 1))
						alpha (0 if pdl_page_index == 0 else 1)
						xsize 50
						font 'Monospace'
					
					text (str(pdl_page_index + 1) + '/' + str(pdl_page_count)):
						font 'Monospace'
						text_size 20
						alpha (0 if pdl_page_count <= 1 else 1)
					
					textbutton '->':
						action SetVariable('pdl_page_index', min(pdl_page_count - 1, pdl_page_index + 1))
						alpha (0 if pdl_page_count == 0 or pdl_page_index == pdl_page_count - 1 else 1)
						xsize 50
						font 'Monospace'
					
					null xsize 100
				
				textbutton _('Default'):
					xalign 1.0
					xsize 100
					font 'Monospace'
					action set_default_projects_dir
			
			vbox:
				spacing 10
				
				for directory in projects_dir_list[pdl_page_index * pdl_page_size : (pdl_page_index + 1) * pdl_page_size]:
					textbutton directory action update_projects(os.path.realpath(projects_dir + '/' + directory))
	
	image front:
		pos (0.51, 0.02)
		size (0.47, 0.95)
		
		vbox:
			ypos 10
			xalign 0.5
			spacing 10
			
			text _('Window size') xalign 0.5
			
			for i in (0, 1):
				hbox:
					xalign 0.5
					spacing 5
					
					for w, h in settings_resolutions[i * 3 : (i + 1) * 3]:
						textbutton ('%sx%s' % (w, h)) xsize 100 action set_stage_size(w, h)
			
			null ysize 20
			
			text _('Fullscreen') xalign 0.5
			hbox:
				xalign 0.5
				spacing 10
				
				textbutton _('On')  xsize 50 action set_fullscreen(True)
				text 'F11'
				textbutton _('Off') xsize 50 action set_fullscreen(False)
			
			null ysize 20
			
			text 'Language' xalign 0.5
			hbox:
				xalign 0.5
				spacing 10
				
				textbutton 'english' action Language(None)
				textbutton 'russian' action Language('russian')
	
	key 'ESCAPE' action HideScreen('settings')
	textbutton _('Return'):
		align (0.95, 0.95)
		action HideScreen('settings')

