display_width = 1400
display_height = 800

display_table_width = 800
display_table_height = 400

bola_branca_posicao_inicial = ( (display_width / 2 - display_table_width / 2) + display_table_width / 5,
                                (display_height / 2 - display_table_height / 2) + display_table_height / 2)


table_x_min = (display_width / 2 - display_table_width / 2)
table_x_max = table_x_min + display_table_width
table_y_min = (display_height / 2 - display_table_height / 2)
table_y_max = table_y_min + display_table_height



bola_branca_raio = 10
bola_branca_massa = 1.7

bola_raio  = 10
bola_massa = 1.5

raio_buraco = 40

apply_background = True
background_image = 'imgs/Background/inf1.jpg'

apply_cue = True
cue_image = 'imgs/Cue/cue.png'
cue_width = 200
cue_height = 60


initial_screen = True
initial_screen_background = 'imgs/Background/snooker.jpg'

tittle_font = 'imgs/Font/apes_tittle.ttf'

end_screen = initial_screen
celebration_walpapper = 'imgs/Background/happy_monkey2.jpg'



device = 'cpu'
# fisica
limiar_atrito=0.5

friccao_dinamica = 0.989 
friccao_estatica = 0.95 
resistencia_ar = 0.9999
elasticidade = 0.95
delta_tempo = 1



# cue
# max
forca_maxima =  30 

use_clock = True