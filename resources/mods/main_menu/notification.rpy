init python:
	notification_size = (300, 150)
	
	notification_msgs = []
	notification_show_time = 3
	notification_hiding_time = 1
	
	def notification(msg):
		show_screen('notification')
		notification_msgs.append([str(msg), time.time(), 1.0])
	
	def notification_update():
		i = 0
		while i < len(notification_msgs):
			msg, start_time, alpha = notification_msgs[i]
			dtime = time.time() - start_time
			
			if dtime < notification_show_time:
				alpha = 1
			elif dtime < notification_show_time + notification_hiding_time:
				alpha = 1 - (dtime - notification_show_time) / notification_hiding_time
			else:
				alpha = 0
			
			if alpha:
				notification_msgs[i][2] = alpha
				i += 1
			else:
				notification_msgs.pop(i)
	
	def notification_remove(index):
		notification_msgs.pop(index)

screen notification:
	zorder 1000
	
	$ notification_update()
	vbox:
		align 1.0
		spacing 10
		
		$ i = 0
		while i < len(notification_msgs):
			$ msg, start_time, alpha = notification_msgs[i]
			
			image im.rect('#222'):
				size notification_size
				alpha alpha
				
				text msg:
					size notification_size
					color 0x0080FF
					text_size 24
					text_align 'center'
					text_valign 'center'
				button:
					ground im.rect('#000')
					hover  im.rect('#000')
					
					size notification_size
					alpha 0.01
					action [notification_remove(i), SetVariable('i', i - 1)]
			
			$ i += 1

