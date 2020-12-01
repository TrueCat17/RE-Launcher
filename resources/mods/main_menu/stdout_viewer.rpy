init python:
	stdout_viewer_lines = []
	started_procs = []
	
	def add_proc(proc):
		started_procs.append(proc)
	
	def stdout_viewer_check():
		i = 0
		while i < len(started_procs):
			proc = started_procs[i]
			rc = proc.poll()
			if rc is None:
				i += 1
				continue
			
			started_procs.pop(i)
			
			stdout_viewer_lines.append('-' * 20)
			out = proc.stdout.read()
			stdout_viewer_lines.extend(out.split('\n'))
			if rc:
				stdout_viewer_lines.append('Error exit code')
	
	def stdout_viewer_clear():
		global stdout_viewer_lines
		stdout_viewer_lines = []


screen stdout_viewer:
	image back:
		size 1.0
	
	vbox:
		yalign 1.0
		
		$ stdout_viewer_check()
		for line in stdout_viewer_lines:
			text line
		
		null ysize 30
	
	key 'ESCAPE' action Hide('stdout_viewer')
	textbutton _('Return'):
		align (0.95, 0.95)
		action HideScreen('stdout_viewer')
