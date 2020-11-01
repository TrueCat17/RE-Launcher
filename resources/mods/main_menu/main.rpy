init 10 python:
	set_fps(20)
	set_can_mouse_hide(False)
	set_can_autosave(False)
	
	db_hide_interface = True # for disable pause-menu in screen <hotkeys>
	start_screens = ['hotkeys', 'main_menu']
	
	back  = im.rect('#4B4')
	front = im.rect('#4D6')
	
	
	style.text.color = 0x0000FF
	style.text.text_size = 30
	
	style.textbutton.ground = im.rect('#08F')
	style.textbutton.hover  = im.rect('#09F')
	style.textbutton.text_size = 20
	style.textbutton.font = 'Arial'
	
	
	console_background_alpha = 0.6


screen main_menu:
	zorder -1
	
	image back:
		size 1.0
	
	image front:
		clipping True
		pos  (0.02, 0.02)
		size (0.47, 0.65)
		
		vbox:
			ypos 10
			xalign 0.5
			spacing 10
			
			text (_('Projects') + ':')
			
			null:
				xalign 0.5
				xsize 0.45
				
				hbox:
					spacing 10
					
					textbutton '<-':
						action SetVariable('pl_page_index', max(0, pl_page_index - 1))
						alpha (0 if pl_page_index == 0 else 1)
						xsize 50
						font 'Monospace'
					
					text (str(pl_page_index + 1) + '/' + str(pl_page_count)):
						font 'Monospace'
						text_size 20
						alpha (0 if pl_page_count <= 1 else 1)
					
					textbutton '->':
						action SetVariable('pl_page_index', min(pl_page_count - 1, pl_page_index + 1))
						alpha (0 if pl_page_count == 0 or pl_page_index == pl_page_count - 1 else 1)
						xsize 50
						font 'Monospace'
				
				textbutton _('Refresh'):
					xalign 1.0
					xsize 100
					font 'Monospace'
					action update_projects(projects_dir)
			
			vbox:
				xalign 0.5
				spacing 10
				
				for project in projects_list[pl_page_index * pl_page_size : (pl_page_index + 1) * pl_page_size]:
					textbutton project:
						xsize 280
						action select_project(project)
	
	
	textbutton _('New Project'):
		pos (0.25, 0.75)
		anchor 0.5
		ground im.rect('#F80')
		hover  im.rect('#F90')
		action Show('new')
	
	
	image front:
		clipping True
		pos  (0.51, 0.02)
		size (0.47, 0.85)
		
		vbox:
			ypos 10
			xalign 0.5
			spacing 10
		
			text (_('Active Project') + ':\n' + (active_project or '-'))
			
			if active_project:
				textbutton _('Open directory')    xsize 280 xalign 0.5 action open_project_dir
				textbutton (_('Start') + ' (F5)') xsize 280 xalign 0.5 action start_project
				textbutton _('Update Ren-Engine') xsize 280 xalign 0.5 action update_project_engine
				textbutton _('Build/Zip')         xsize 280 xalign 0.5 action build_project
				textbutton _('Extra...')          xsize 280 xalign 0.5 action Show('extra')
				
				key 'F5' action start_project
	
	hbox:
		align (0.05, 0.95)
		spacing 5
		
		textbutton _('Documentation'):
			xsize 200
			ground im.rect('#80F')
			hover  im.rect('#F08')
			action open_documentation
	
	hbox:
		align (0.95, 0.95)
		spacing 5
		
		textbutton _('Console')  xsize 120 action Show('console')
		textbutton _('Settings') xsize 120 action Show('settings')
		textbutton _('Exit')     xsize 120 action exit_from_game

