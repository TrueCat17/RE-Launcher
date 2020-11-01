screen extra:
	image back:
		size 1.0
	
	vbox:
		align 0.5
		spacing 10
		
		textbutton _('Stdout (from print)') xsize 200 action Show('stdout_viewer')
	
	key 'ESCAPE' action Hide('extra')
