init python:
	def stdout_viewer__add_proc(proc):
		stdout_viewer.started_procs.append(proc)
	
	def stdout_viewer__check():
		i = 0
		while i < len(stdout_viewer.started_procs):
			proc = stdout_viewer.started_procs[i]
			rc = proc.poll()
			if rc is None:
				i += 1
				continue
			
			stdout_viewer.started_procs.pop(i)
			
			stdout_viewer.lines.append('-' * 20)
			out = str(proc.stdout.read(), 'utf8')
			stdout_viewer.lines.extend(out.split('\n'))
			if rc:
				stdout_viewer.lines.append('Error exit code')
	
	def stdout_viewer__clear():
		stdout_viewer.lines = []
	
	build_object('stdout_viewer')
	stdout_viewer.lines = []
	stdout_viewer.started_procs = []


screen stdout_viewer:
	image theme.back_bg:
		size 1.0
	
	vbox:
		xalign 0.5
		ypos 0.92
		yanchor 1.0
		
		$ stdout_viewer.check()
		for line in stdout_viewer.lines[-60:]:
			text line:
				xsize 0.95
				font  theme.version_text_font
				color theme.version_text_color
	
	key 'ESCAPE' action Hide('stdout_viewer')
	textbutton _('Return'):
		align (0.03, 0.97)
		xsize 150
		ground im.round_rect(theme.btn_ground_color, 150, btn_ysize, 4)
		hover  im.round_rect(theme.btn_hover_color,  150, btn_ysize, 4)
		action HideScreen('stdout_viewer')
