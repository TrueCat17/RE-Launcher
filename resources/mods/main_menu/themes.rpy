init python:
	themes = []
	
	def set_theme(name):
		for i in themes:
			if i.name == name:
				global theme
				theme = i
				persistent.theme_name = name
				break
	
	
	day_theme = Object(name = 'Day')
	themes.append(day_theme)
	
	day_theme.back_bg  = im.rect('#E8EEF4')
	day_theme.front_bg = im.rect('#BDCBD9')
	day_theme.open_bg  = im.rect('#555588')
	
	day_theme.text_font = 'Fregat_bold'
	day_theme.text_color = '#558'
	
	day_theme.version_text_font = 'Arial'
	day_theme.version_text_color = '#558'
	
	day_theme.btn_text_font = 'Fregat_bold'
	day_theme.btn_text_color = '#FFF'
	day_theme.btn_ground_color = '#08F'
	day_theme.btn_hover_color  = '#0AF'
	day_theme.btn_ground_color_active = '#F80'
	day_theme.btn_hover_color_active  = '#F90'
	day_theme.doc_btn_ground_color = '#80F'
	day_theme.doc_btn_hover_color  = '#F08'
	day_theme.refresh_btn_ground = 'images/misc/refresh_ground.png'
	day_theme.refresh_btn_hover  = 'images/misc/refresh_hover.png'
	day_theme.open_btn_ground_color = '#00000002'
	day_theme.open_btn_hover_color  = '#08F'
	day_theme.open_btn_text_font = 'Arial'
	day_theme.open_btn_text_color = '#FFF'
	day_theme.open_text_font = 'Fregat_bold'
	day_theme.open_text_color = '#FFF'
	day_theme.open_text_color_inactive = '#AAA'
	
	
	night_theme = Object(day_theme, name = 'Night')
	themes.append(night_theme)
	
	night_theme.back_bg = im.rect('#046')
	night_theme.front_bg = im.rect('#ABC')
	night_theme.version_text_color = '#FFF'
	night_theme.btn_ground_color = '#07F'
	night_theme.btn_hover_color  = '#08F'
	night_theme.btn_ground_color_active = '#F70'
	night_theme.btn_hover_color_active  = '#F80'
	night_theme.doc_btn_ground_color = '#60C'
	night_theme.doc_btn_hover_color  = '#C06'
	
	
	green_theme = Object(day_theme, name = 'Green')
	themes.append(green_theme)
	
	green_theme.back_bg = im.rect('#4B4')
	green_theme.front_bg = im.rect('#4D6')
	green_theme.open_bg  = im.rect('#272')
	green_theme.text_color = '#00F'
	green_theme.version_text_color = green_theme.text_color
	
	
	contrast_theme = Object(day_theme, name = 'Contrast')
	themes.append(contrast_theme)
	
	contrast_theme.back_bg = im.rect('#DDD')
	contrast_theme.front_bg = im.rect('#AAA')
	contrast_theme.open_bg = im.rect('#04C')
	contrast_theme.btn_ground_color = '#000'
	contrast_theme.btn_hover_color  = '#444'
	contrast_theme.btn_ground_color_active = '#E00'
	contrast_theme.btn_hover_color_active  = '#F00'
	contrast_theme.text_color = '#000'
	contrast_theme.version_text_color = contrast_theme.text_color
	
	
	
	if persistent.theme_name is None:
		persistent.theme_name = 'Day'
	set_theme(persistent.theme_name)
