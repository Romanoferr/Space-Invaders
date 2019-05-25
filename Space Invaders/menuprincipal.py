from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from lugarmenu import lugar
'''Implementacoes de colisoes otimizacao:
'''


janela = Window(800, 600)
janela.set_title("Space invaders")
botao_play = Sprite("play.png")
botao_playhover = Sprite("playhover.png")

botao_dificuldade = Sprite("dificuldade.png")
botao_dificuldadehover = Sprite("dificuldadehover.png")

botao_rank = Sprite("rank.png")
botao_rankhover = Sprite("rankhover.png")

botao_quit = Sprite("quit.png")
botao_quithover = Sprite("quithover.png")

nave = Sprite("spaceship.png")

fundo = GameImage("fundo.png")
mouse = Window.get_mouse()
teclado = Window.get_keyboard()

lugar(janela, botao_play, botao_playhover, botao_dificuldade, botao_dificuldadehover, botao_rank, botao_rankhover, botao_quit, botao_quithover)

nave.set_position(janela.width / 2 - nave.width / 2, janela.height - nave.height - 10)


# inicializacoes de variaveis
listatiros = []
matriz = []
delayfps = 1
delay = 3
dificult = 1
sentido = 1
lose = 0
gamestate = 0


def calculafps():
	global delayfps, fps
	delayfps += janela.delta_time()
	if delayfps >= 1:
		fps = int(1 / janela.delta_time())
		delayfps = 0


def novotiro():
	tiro = Sprite("tirospace.png")
	tiro.set_position(nave.x + nave.width / 2 - tiro.width / 2, nave.y)
	listatiros.append(tiro)


def movenave():
	global delay
	vel_nave = 560 * janela.delta_time()
	if teclado.key_pressed("RIGHT"):
		if nave.x + nave.width < janela.width:
			nave.x += vel_nave
	if teclado.key_pressed("LEFT"):
		if nave.x > 0:
			nave.x -= vel_nave

	if teclado.key_pressed("SPACE") and delay*dificult >= 1:
		novotiro()
		delay = 0


def desenhatiro():
	vel_tiro = -350 * janela.delta_time()
	for tiro in listatiros:
		if tiro.y < 0 - tiro.height:
			listatiros.remove(tiro)
		tiro.move_y(vel_tiro)
		tiro.draw()


def matrizmonstros(a, b):
	global matriz
	for i in range(a):
		linha = []
		for j in range(b):
			enemy = Sprite("enemy.png")
			enemy.set_position(i * 2 * enemy.width, (j * 2 * enemy.height) + 10)
			linha.append(enemy)
		matriz.append(linha)


def moveenemy():
	global matriz, sentido, lose
	vel_enemy = 100 * janela.delta_time()
	movimento = vel_enemy * sentido
	for linha in range(len(matriz)):
		for coluna in range(len(matriz[linha])):
			matriz[linha][coluna].move_x(movimento)

			if matriz[linha][coluna].x >= janela.width - matriz[linha][coluna].width or matriz[linha][coluna].x <= 0:
				sentido *= -1

			if matriz[linha][coluna].y >= janela.height - matriz[linha][coluna].height:
				lose = 1


def desenhaenemy():
	for mx in range(len(matriz)):
		for my in range(len(matriz[mx])):
			matriz[mx][my].draw()


def telajogo():
	global gamestate
	global delay
	delay += janela.delta_time()
	fundo.draw()
	movenave()
	desenhatiro()
	moveenemy()
	desenhaenemy()
	nave.draw()


def teladificuldade():
	global gamestate
	fundo.draw()
	janela.draw_text("ESSA EH A TELA DE DIFICULDADE", janela.width/2 - 200, janela.height/2, 40, (255, 255, 255))


def telarank():
	global gamestate
	fundo.draw()
	janela.draw_text("ESSA EH A TELA DE RANK", janela.width/2 - 150, janela.height/2, 40, (255, 255, 255))


def menu():
	global gamestate
	fundo.draw()
	botao_play.draw()
	botao_dificuldade.draw()
	botao_rank.draw()
	botao_quit.draw()

	if mouse.is_over_object(botao_play):
		botao_playhover.draw()
		if mouse.is_button_pressed(1):
			gamestate = 1

	if mouse.is_over_object(botao_dificuldade):
		botao_dificuldadehover.draw()
		if mouse.is_button_pressed(1):
			gamestate = 2

	if mouse.is_over_object(botao_rank):
		botao_rankhover.draw()
		if mouse.is_button_pressed(1):
			gamestate = 3

	if mouse.is_over_object(botao_quit):
		botao_quithover.draw()
		if mouse.is_button_pressed(1):
			gamestate = 4


matrizmonstros(7, 7)


while True:
	if gamestate == 0:
		menu()
	if gamestate == 1:
		telajogo()
		calculafps()
		janela.draw_text(str(fps), 740, 3, size=12, color=(255, 255, 255), bold=True)
	if gamestate == 2:
		teladificuldade()
	if gamestate == 3:
		telarank()
	if gamestate == 4:
		break

	janela.update()
