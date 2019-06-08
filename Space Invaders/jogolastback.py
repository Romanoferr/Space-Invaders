from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.collision import *
from lugarmenu import lugar
import random
from numpy import shape


'''Implementacoes de colisoes otimizacao:'''
''''
	Implementacao de ranking, cada monstro vale uma certa quantidade de pontos
	a pontuacao que cada monstro da diminui em relacao ao tempo
	
	Implementar nova fase quando monstros morrem
'''


janela = Window(800, 600)
janela.set_title("Space invaders")
botao_play = Sprite("img/play.png")
botao_playhover = Sprite("img/playhover.png")

botao_dificuldade = Sprite("img/dificuldade.png")
botao_dificuldadehover = Sprite("img/dificuldadehover.png")

botao_rank = Sprite("img/rank.png")
botao_rankhover = Sprite("img/rankhover.png")

botao_quit = Sprite("img/quit.png")
botao_quithover = Sprite("img/quithover.png")

nave = Sprite("img/spaceship.png")

fundo = GameImage("img/fundo.png")
over = Sprite("img/gameover.jpg")
mouse = Window.get_mouse()
teclado = Window.get_keyboard()

lugar(janela, botao_play, botao_playhover, botao_dificuldade, botao_dificuldadehover, botao_rank, botao_rankhover, botao_quit, botao_quithover)

nave.set_position(janela.width / 2 - nave.width / 2, janela.height - nave.height - 10)
over.set_position(janela.width/2 - over.width/2, janela.height/2 - over.height/2)

# inicializacoes de variaveis
listatiros = []
listatiros_enemy = []
matriz = []
delay = 0
dificult = 3
sentido = 1
lose = 0
gamestate = 0
matriz_x = 4
matriz_y = 3
fps = fpsatual = delayfps = 0
tempo = 1
pontos = 0
pontobase = 10
pulobase = 35
reloadmonstro = 2
tempomonstro = 0
tempodano = 0


def colisaonave():
	global listatiros_enemy, tempodano, lose
	for tiro in range(len(listatiros_enemy)):
		if nave.collided(listatiros_enemy[tiro]):
			listatiros_enemy.remove(listatiros_enemy[tiro])
			lose = 1


def desenhatiro_enemy():
	global listatiros_enemy, tiroenemy
	vel_tiro_enemy = 350 * janela.delta_time()
	for tiroenemy in listatiros_enemy:

		tiroenemy.move_y(vel_tiro_enemy)
		tiroenemy.draw()

		if tiroenemy.y > janela.height:
			listatiros_enemy.remove(tiroenemy)


def novotiro_enemy():
	global tempomonstro, reloadmonstro, listatiros_enemy, matriz
	if reloadmonstro <= tempomonstro:
		x = random.randint(0, len(matriz) - 1)
		y = random.randint(0, matriz_y - 1)
		tiro_enemy = Sprite("img/tirospace.png")

		if matriz[x][y] == 0:
			novotiro_enemy()
		else:
			tiro_enemy.set_position(matriz[x][y].x + matriz[x][y].width/2, matriz[x][y].y + matriz[x][y].height)
			listatiros_enemy.append(tiro_enemy)
			tempomonstro = 0


def novonivel():
	global matriz, matriz_x, matriz_y, tempo, dificult, pontobase, pulobase, reloadmonstro
	vivo = 1
	for i in range(len(matriz)):
		if (matriz[i]) == 0:
			vivo = 0
			break

	# atualiza valores para proxima fase e cria nova matriz
	if vivo == 0:
		pulobase += 3
		pontobase += 2
		tempo = 1
		matriz_y += 1
		matriz_x += 1
		dificult += 1
		reloadmonstro -= 0.1

		if matriz_x >= 8:
			matriz_x = 8
		if matriz_y >= 6:
			matriz_y = 6
		if dificult >= 6:
			dificult = 6
		if pulobase >= 60:
			pulobase = 60
		if reloadmonstro <= 0.9:
			reloadmonstro = 0.9

		matrizmonstros(matriz_x, matriz_y)


def pontuacao():
	global pontos, tempo
	pontos += int(50/tempo) + pontobase


def gameover():
	janela.set_background_color((255, 255, 255))
	over.draw()


def ifps():
	global delayfps, fps, fpsatual
	if delayfps < 1:
		fps += 1
	else:
		fpsatual = fps
		fps = 0
		delayfps = 0


def colisao():
	global matriz, listatiros, nave, lose
	for tiro in range(len(listatiros)):
		for mxx in range(len(matriz)):
			for myy in range(len(matriz[mxx])):
				if matriz[mxx][myy] != 0:

					if matriz[mxx][myy].collided(nave):
						lose = 1

					if listatiros[tiro].collided(matriz[mxx][myy]):
						matriz[mxx][myy] = 0
						listatiros.remove(listatiros[tiro])
						pontuacao()
						return


def novotiro_nave():
	global listatiros
	tiro = Sprite("img/tirospace.png")
	tiro.set_position(nave.x + nave.width / 2 - tiro.width / 2, nave.y)
	listatiros.append(tiro)


def movenave():
	global delay
	vel_nave = 560 * janela.delta_time()
	if teclado.key_pressed("RIGHT"):
		if nave.x + nave.width < janela.width:
			nave.move_x(vel_nave)
	if teclado.key_pressed("LEFT"):
		if nave.x > 0:
			nave.move_x(-vel_nave)

	if teclado.key_pressed("SPACE") and delay*dificult >= 1:
		novotiro_nave()
		delay = 0


def desenhatiro():
	global listatiros
	vel_tiro_nave = -350 * janela.delta_time()
	for tiro in listatiros:
		if tiro.y < 0 - tiro.height:
			listatiros.remove(tiro)
		tiro.move_y(vel_tiro_nave)
		tiro.draw()


def matrizmonstros(a, b):
	global matriz
	for i in range(a):
		linha = []
		for j in range(b):
			enemy = Sprite("img/enemy.png")
			enemy.set_position(i * 2 * enemy.width, (j * 2 * enemy.height) + 30)
			linha.append(enemy)
		matriz.append(linha)


def moveenemy():
	global matriz, sentido, lose
	# move a matriz de monstros horizontalmente
	vel_enemy = 120 * janela.delta_time()
	movimento = vel_enemy * sentido
	for linha in range(len(matriz)):
		for coluna in range(len(matriz[linha])):
			if matriz[linha][coluna] != 0:
				matriz[linha][coluna].move_x(movimento)

				if matriz[linha][coluna].y + matriz[linha][coluna].height > janela.height:
					lose = 1

				if matriz[linha][coluna].x >= janela.width - matriz[linha][coluna].width or matriz[linha][coluna].x <= 0:
					sentido *= -1
					matriz[linha][coluna].move_x(5 * sentido)

				# Move verticalmente a matriz de monstros pensar
					for abc in range(matriz_x * matriz_y):
						for l in range(len(matriz)):
							for c in range(len(matriz[l])):
								if matriz[l][c] != 0:
									matriz[l][c].move_y(pulobase)
						return


def desenhaenemy():
	global matriz
	for mx in range(len(matriz)):
		for my in range(len(matriz[mx])):
			if matriz[mx][my] != 0:
				matriz[mx][my].draw()


def telajogo():
	global gamestate, delay, listatiros, lose
	if lose == 0:
		fundo.draw()
		movenave()
		desenhatiro()
		moveenemy()
		desenhaenemy()
		colisao()
		ifps()
		novonivel()
		novotiro_enemy()
		desenhatiro_enemy()
		colisaonave()
		nave.draw()

	else:
		gameover()


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

	# desenha os hover e detecta mudanca de estados
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


matrizmonstros(matriz_x, matriz_y)


while True:

	delay += janela.delta_time()
	delayfps += janela.delta_time()
	tempo += janela.delta_time()
	tempomonstro += janela.delta_time()

	if gamestate == 0:
		menu()
	if gamestate == 1:
		telajogo()
		janela.draw_text(str(fpsatual), 740, 3, size=12, color=(255, 255, 255), bold=True)
		janela.draw_text('Pontuação: ' + str(pontos), 700, janela.height-15, size=12, color=(255, 255, 255), bold=True)
	if gamestate == 2:
		teladificuldade()
	if gamestate == 3:
		telarank()
	if gamestate == 4:
		break

	janela.update()
