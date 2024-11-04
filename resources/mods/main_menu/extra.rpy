init -100 python:
	links = {
		'doc':      'https://github.com/TrueCat17/Ren-Engine/wiki',
		'Discord':  'https://discord.gg/DBagjrCWVp',
		'Telegram': 'https://t.me/ren_engine_tg',
		'VK':       'https://vk.com/ren_engine',
	}
	
	def copy_link(name):
		link = links[name]
		set_clipboard_text(link)
		notification.out(link)

screen extra:
	image im.rect(theme.back_bg_color):
		size 1.0
	
	$ xsize = get_stage_width() // 3
	$ ground = im.round_rect(theme.panel_btn_ground_color, 100, btn_ysize, 6)
	$ hover  = im.round_rect(theme.panel_btn_hover_color,  100, btn_ysize, 6)
	
	image get_panel():
		$ btn_params = (
			(_('Open Log File') + ' (F6)',                    project.open_log_file),
			(_('Project Language') + ': ' + project.language, project.ask_lang),
			(_('Delete Variables') + ' (/var)',               project.delete_var_directory),
		)
		
		corner_sizes -1
		xsize 0.5
		ysize 0.35
		align (0.5, 0.2)
		
		vbox:
			align 0.5
			spacing 8
			
			for text, action in btn_params:
				textbutton text:
					xsize xsize
					ground ground
					hover  hover
					font        theme.panel_btn_text_font
					color       theme.panel_btn_text_color
					hover_color theme.panel_btn_text_color_hover
					action action
	
	image get_panel():
		corner_sizes -1
		xsize 0.5
		ysize 0.35
		align (0.5, 0.8)
		
		vbox:
			align 0.5
			spacing 8
			
			text (_('Copy link') + ':'):
				xalign 0.5
				font  theme.text_font
				color theme.text_color
				text_size text_size * 1.5
			
			$ xsize = get_stage_width() // 7
			for name in links:
				if name != 'doc':
					textbutton name:
						xalign 0.5
						xsize xsize
						ground ground
						hover  hover
						font        theme.panel_btn_text_font
						color       theme.panel_btn_text_color
						hover_color theme.panel_btn_text_color_hover
						action copy_link(name)
	
	use icon_btn('return', 0.03, 0.97, get_stage_width() // 8, HideScreen('extra'))
	
	key 'ESCAPE' action HideScreen('extra')
