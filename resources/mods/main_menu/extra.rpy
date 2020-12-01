init python:
	def delete_var_directory():
		var = projects_dir + '/' + active_project + '/var'
		if os.path.exists(var):
			shutil.rmtree(var)
		notification(_('Variable data deleted'))

screen extra:
	image back:
		size 1.0
	
	vbox:
		align 0.5
		spacing 10
		
		textbutton (_('Project Language') + ': ' + active_project_language):
			xsize 400
			action ask_str(set_active_project_language, active_project_language)
		
		textbutton (_('Delete Variables') + ' (/var)'):
			xsize 400
			action delete_var_directory
		
		textbutton _('Stdout (from print)'):
			xsize 400
			action Show('stdout_viewer')
	
	
	key 'ESCAPE' action HideScreen('extra')
	textbutton _('Return'):
		align (0.95, 0.95)
		action HideScreen('extra')
