from damas import Damas
from clock import Clock
from bot import random_Bot, thinking_Bot
import pygame
import time

# Criação das classes usadas durante o código (com excessão do bot, pois essa dependerá da dificuldade escolhida):
pygame.init()
fps = pygame.time.Clock()
som = pygame.mixer.Sound('lib/soundefect.wav')
screen = pygame.display.set_mode([600, 600])
menu = pygame.image.load('lib/menu.png')

# Declaração de algumas das variáveis usadas durante o código
new_move = True
running = True
from_ = []
to = []
possible_moves = []
lastmove = []
gameover = [False, 0]
is_game = False
side = 0
ritimo = []
dificuldade = ''
config_ready = False


def xytoij(dict, side):
    # Associa a posição do click para uma casa do tabuleiro
    x, y = dict
    if 100 <= x <= 500 and 100 <= y <= 500:
        i = (x-100)//50
        j = (y-100)//50

        if (i+j)%2 != 0:
            # Verifica se o click foi numa casa negra

            if side == 1:
                # if else para discernir quais casas estão sendo usadas dependendo do ponto de vista do jogador (se está de peças brancas ou pretas)
                a = i
                b = j
                    
            else:
                a = 7 - i
                b = 7 - j

            return [a, b]

        return []

while running:
    # loop que faz o jogo rodar

    fps.tick(40)
    # limita o jogo a 40 fps
    
    for event in pygame.event.get():
        # passa por todos os inputs dados pelo jogador

        if event.type == pygame.MOUSEBUTTONDOWN:

            if not is_game:
                # caso esteja no menú, verifica em qual botão o jogador ta clicando
                side = 1 if 280 < event.__dict__['pos'][0] < 320 and 265 < event.__dict__['pos'][1] < 305 else side
                side = -1 if 280 < event.__dict__['pos'][0] < 320 and 315 < event.__dict__['pos'][1] < 355 else side

                
                dificuldade = 'f' if 50 < event.__dict__['pos'][0] < 170 and 263 < event.__dict__['pos'][1] < 303 else dificuldade
                dificuldade = 'd' if 50 < event.__dict__['pos'][0] < 170 and 312 < event.__dict__['pos'][1] < 352 else dificuldade

                
                ritimo = [60, 3] if 410 < event.__dict__['pos'][0] < 565 and 260 < event.__dict__['pos'][1] < 303 else ritimo
                ritimo = [180, 2] if 410 < event.__dict__['pos'][0] < 565 and 313 < event.__dict__['pos'][1] < 355 else ritimo

                if config_ready and 130 < event.__dict__['pos'][0] < 505 and 500 < event.__dict__['pos'][1] < 550:
                    # se a opção de começar o jogo já estiver disponível, começa a detectar a hitbox do botão
                    # quando o botão for selecionado, iniciará as classes e variáveis necessárias para a partida
                    is_game = True
                    damas = Damas()

                    # cria o bot dependendo da dificuldade escolhida pelo jogador
                    if dificuldade == 'd':
                        bot = thinking_Bot(damas)
                    else:
                        bot = random_Bot(damas)

                    m = damas.legalmoves()
                    tempo = Clock((side == 1), ritimo[0], ritimo[1])

            elif not gameover[0]:
                # caso a partida já tenha começado, detcta em quais casas do tabuleiro o jogador ta clicando
                p = xytoij(event.__dict__['pos'], side)

                if p:
                    if (damas.is_white(p) and damas.turn) or (damas.board[p[0]][p[1]] < 0 and not damas.turn):
                        # Detecta os cliques do usuário e o lance que ele está fazendo
                        from_ = p
                        to = []

                    else:
                        to = p
                        
            if (18 < event.__dict__['pos'][0] < 248) and (39 < event.__dict__['pos'][1] < 64):
                # if do botão de voltar para o menu
                is_game = False
                gameover = [False, 0]
                lastmove = []
                del damas, bot, tempo

        elif event.type == pygame.QUIT:
            # detecta se é para fechar o jogo
            running = False

    pygame.event.clear()
    
    if not is_game:
        # desenha o menu e seus botões
        screen.blit(menu, [0, 0])

        pygame.draw.circle(screen, (235, 235, 235), [300, 285], 20)


        pygame.draw.circle(screen, (20, 20, 20), [300, 335], 20)

        if side == 1:
            pygame.draw.circle(screen, (50, 50, 50), [300, 285], 14)
            pygame.draw.circle(screen, (235, 235, 235), [300, 285], 12)

        elif side == -1:
            pygame.draw.circle(screen, (205, 205, 205), [300, 335], 14)
            pygame.draw.circle(screen, (20, 20, 20), [300, 335], 12)

        if dificuldade == 'f':
            pygame.draw.circle(screen, (251, 240, 168), [154, 282], 6)

        elif dificuldade == 'd':
            pygame.draw.circle(screen, (251, 240, 168), [154, 332], 6)

        if ritimo == [60, 3]:
            pygame.draw.circle(screen, (251, 240, 168), [545, 280], 6)

        elif ritimo == [180, 2]:
            pygame.draw.circle(screen, (251, 240, 168), [545, 335], 6)

        if side and ritimo and dificuldade:
            # só permite começar a partida caso todas as configurações sejam dadas
            config_ready = True
            font = pygame.font.Font(None, 50)
            text = font.render("Começar a partida  -->", True, (251, 240, 168))
            screen.blit(text, [130, 500])

        pygame.display.flip()

    else:
        # caso esteja na partida:

        if tempo.remaining <= 0:
            # vê se o tempo do player acabou
            gameover = [True, 'Pretas ganham!' if damas.turn else 'Brancas ganham!']
            new_move = lastmove

        possible_moves = []
        # esvazia a variável, pro caso do jogador clicar em outra casa

        if gameover[0]:
            # se o jogo tiver acabado, impede que lances sejam feitos
            pass
        
        elif from_ and to and (damas.turn == (side == 1)):
            # caso o jogador tenha feito um lance, tenta realizá-lo no tabuleiro
            new_move = damas.playermove([from_, to], m)

            if new_move:
                # caso o lance tenha sido legal, toca o som, incrementa o relógio, atualiza a variável pra mostrar qual o ultimo lance feito e prepara a movelist pro bot
                lastmove = [from_, to]
                tempo.incremento()
                m = damas.legalmoves()
                som.play()

            from_ = []
            to = []

        elif damas.turn != (side == 1):
                # caso seja o lance do bot, dá um tempinho pro jogador perceber que fez besteira kkkk 
                # brincadeira, esse delay é o fake-thinking, se não tivesse ele o bot fazia o lance quase instantaneamente e isso dá uma sensação estranha
                time.sleep(0.7)
                new_move = bot.botmove()

                if new_move:
                    # caso o bot tenha conseguido fazer o lance, toca o som e atualiza as casas roxas (acho que esse if é inútil, mas, já que eu já implementei, decidi deixar)
                    lastmove = [new_move[0], new_move[1]]
                    som.play()
                #new_move = damas.playermove(random.choice(m[1]), m)
                #print(damas.legalmoves()[1])
                m = damas.legalmoves()

        elif from_:
            # caso seja a vez do player, ele ainda esteja pensando e clique em uma peça, mostra quais lances ele pode fazer com aquela peça
            for move in m[1]:
                if from_ == move[0]:
                    possible_moves.append(move[1])


        if new_move and not gameover[0]:
            if damas.game_result(m[1])[0]:
                # verifica se o jogo acabou
                new_move = lastmove

                if damas.game_result(m[1])[1] > 0:
                    gameover = [True, 'Brancas ganham!']

                elif damas.game_result(m[1])[1] < 0:
                    gameover = [True, 'Pretas ganham!']

                else:
                    gameover = [True, 'Empate!']


        # cor do background
        screen.fill((25, 20, 20))
        piece = 0

        for i in range(8):
            for j in range(8):
                # imprime o tabuleiro e as peças de acordo com a situação do tabuleiro damas.board
                if (i+j)%2 != 0:

                    if side == 1:
                        # altera a perspectiva de acordo com as peças do jogador
                        a = i
                        b = j
                    
                    else:
                        # altera a perspectiva de acordo com as peças do jogador
                        a = 7 - i
                        b = 7 - j

                    if [a, b] in lastmove:
                        # imprime as casas do ultimo lance feito
                        pygame.draw.rect(screen, (135,170,0), [100 + i*50, 100 + j*50, 50, 50])

                    elif [a, b] == from_:
                        # imprime a casa na qual o jogador está clicando numa cor um pouco diferente
                        pygame.draw.rect(screen, (130, 66, 11), [100 + i*50, 100 + j*50, 50, 50])

                    else:
                        # imprime uma casa marrom normal
                        pygame.draw.rect(screen, (156, 87, 20), [100 + i*50, 100 + j*50, 50, 50])
                    
                    if [a, b] in possible_moves:
                        # desenha a bolinha verde que mostra os lances possíveis
                        pygame.draw.circle(screen, (20, 105, 30), (125 + i*50, 125 + j*50), 9)
                    
                    # essa parte descobre qual peça está na casa e a desenha:
                    if damas.board[a][b] > 0:
                        pygame.draw.circle(screen, (235, 235, 235), (125 + i*50, 125 + j*50), 20)

                        if damas.board[a][b] != 1:
                            pygame.draw.circle(screen, (50, 50, 50), (125 + i*50, 125 + j*50), 14)
                            pygame.draw.circle(screen, (235, 235, 235), (125 + i*50, 125 + j*50), 12)

                    elif damas.board[a][b] < 0:
                        pygame.draw.circle(screen, (20, 20, 20), (125 + i*50, 125 + j*50), 20)

                        if damas.board[a][b] != -1:
                            pygame.draw.circle(screen, (205, 205, 205), (125 + i*50, 125 + j*50), 14)
                            pygame.draw.circle(screen, (20, 20, 20), (125 + i*50, 125 + j*50), 12)
                
                else:
                    # imprime uma casa branca
                    pygame.draw.rect(screen, (251, 240, 168), [100 + i*50, 100 + j*50, 50, 50])
                    

        if new_move or (damas.turn == (side == 1)):
            # só atualiza a tela caso algum novo lance tenha ocorrido
            # ou caso seja necessário atualizar o relógio
            
            pygame.draw.rect(screen, (255, 255, 255), [500, 380, 100, 70])
            font = pygame.font.Font(None, 62)
            t = tempo.get_time(damas.turn)
            text = font.render(f"{int(t//60)}:{int(t%60)}", True, (0, 0, 0))
            screen.blit(text, [510, 396])
            # desenha o relógio

            font = pygame.font.Font(None, 35)
            text = font.render("<-- Voltar ao menu", True, (255, 255, 255))
            screen.blit(text, [20, 40])
            # desenha o voltar pro menu

            if gameover[0]:
                # caso o jogo tenha terminado, mostra o resultado
                text = font.render("Fim de jogo", True, (255, 255, 255))
                screen.blit(text, [225, 510])
                text = font.render(gameover[1], True, (255, 255, 255))
                screen.blit(text, [286, 535])

            # atualiza a tela
            pygame.display.flip()
            new_move = False
