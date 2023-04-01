screen extra:
	image theme.back_bg:
		size 1.0
	
	vbox:
		align 0.5
		spacing 10
		
		$ btn_params = (
			(_('Project Language') + ': ' + project.language, project.ask_lang),
			(_('Delete Variables') + ' (/var)', project.delete_var_directory),
			(_('Stdout (from print)') + ' (F6)', Show('stdout_viewer')),
		)
		for text, action in btn_params:
			textbutton text:
				xsize 400
				ground im.round_rect(theme.btn_ground_color, 400, btn_ysize, 4)
				hover  im.round_rect(theme.btn_hover_color,  400, btn_ysize, 4)
				action action
	
	
	key 'ESCAPE' action HideScreen('extra')
	textbutton _('Return'):
		align (0.03, 0.97)
		xsize 150
		ground im.round_rect(theme.btn_ground_color, 150, btn_ysize, 4)
		hover  im.round_rect(theme.btn_hover_color,  150, btn_ysize, 4)
		action HideScreen('extra')
