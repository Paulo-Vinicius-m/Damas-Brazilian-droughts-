from damas import Damas
import time
import random

class thinking_Bot:
    # Classe que contem o bot
    def __init__(self, damas: Damas) -> None:
        self.damas = damas

    def botmove(self):
        # Calcula lance por lance usando alpha-beta pruning

        # alpha-beta pruning: nesse tipo de algoritmo o alpha guarda a avaliação do melhor 
        # lance encontrado até então naquela posição enquanto o beta guarda 
        # a avaliação do melhor lance encontrado para o adversário na posição anterior. Ou seja,
        # com essas duas variáveis nós podemos otimizar a busca por lances descartando uma arvore
        # de lances a serem calculados assim que se detecta que ela é pior que alguma outra opção
        # descoberta pelo jogador anteriormente no cálculo ou, no caso do ponto de vista do adversário (para o qual usamos o beta), 
        # assim que se detecta que uma árvore de lances possíveis decorrente de um lance do adversário
        # é mais vantajosa pra mim (jogador que está pensando em qual lance fazer) do que para o adversário,
        # é possível descartá-la e partir pra próxima possibilidade, já que o adversário não vai escolher um lance que é pior pra ele

        # enfim, ficou meio confuso mas espero que tenha dado pra entender

        # ultimas considerações: a cada lance que se aprofunda durante a análise, os pontos de vista se alteram
        # então o que era, por exemplo, um alpha de 5 (ou seja, a melhor possibilidade encontrada até agora dá uma vantagem de 5 pontos)
        # será passado pra próxima profundidade da busca como um beta de -5 (uma desvantagem de 5 pontos para o adversário)

        # esse aprofundamento funciona usando recursividade na função search(), sempre alterando os pontos de vista:
        # pra cada lance possível na posição, ele é feito no tabuleiro, a função search é chamada na nova posição e retorna a avaliação dela
        # depois o lance é desfeito para que o próximo possa ser analisado (caso ainda valha a pena analisar a posição)

        # decidi fazer um algoritmo complicado desse jeito porque já tinha feito um nesse esquema pro jogo de lop (entreguei um bot de xadrez: https://github.com/Paulo-Vinicius-m/p5jchess.github.io)

        movelist = self.damas.legalmoves()
        bestmove = []
        alpha = -99999999
        aval = 0
        t1 = time.time()

        if len(movelist[1]) == 1:
            # se só tiver um lance possível, faz ele direto
            return self.damas.playermove(movelist[1][0], movelist)

        for move in movelist[1]:
            # passa por todos os lances possíveis, analisando eles
            self.analyse_move(move, movelist[0])

            if movelist[0] > 1:
                # caso o lance faça parte de uma sequência de capturas, não altera a perspectiva (já que não muda o turno)
                # na primeira profundidade não há beta, por isso que é passado um valor tão pequeno/grande -> para evitar que ele altere a decisão do bot, dada sua perspectiva
                aval = self.search(alpha, 9999999)
            else:
                aval = -self.search(-9999999, -alpha)

            self.damas.undo(move)
            #print(move)
            if aval > alpha:
                # se esse lance for o melhor encontrado, atualiza o alfa e o bestmove
                alpha = aval
                bestmove = move
            
            # essa primeira função não tem o beta porque não tem como considerar as escolhas do adversário no primeiro lance de profundidade
            
        # Faz o lance que ele avaliou como melhor
        self.damas.playermove(bestmove, movelist)

        # escreve quanto tempo a engine demorou calculando e a avaliação dela sobre a posição
        t2 = time.time() - t1
        print('search:', alpha, '\ntime:', t2)
        
        return bestmove


    def search (self, alpha, beta):
        
        # Coloca uma espectativa mínima para não perder muito tempo analisando capturas ruins
        aval = self.evaluation()
        if aval >= beta:
            return beta
        
        if aval > alpha:
            alpha = aval
        
        movelist = self.damas.legalmoves()
        
        for move in movelist[1]:
            # a ideia é passar por todos os lances, mas analizando apenas as capturas
            # só pra impedir que o bot fique entregando peças sem que ele fique muito forte
            if move[2]:
                self.analyse_move(move, movelist[0])
                
                if movelist[0] > 1:
                    # caso o lance faça parte de uma sequência de capturas, não altera a perspectiva (já que não muda o turno)
                    aval = self.search(alpha, beta)
                else:
                    aval = -self.search(-beta, -alpha)

                self.damas.undo(move)

                if aval >= beta:
                    # agora ja dá para usar o beta:
                    # se essa posição for melhor do que alguma outra posição que o adversário possa escolher,
                    # não vale a pena continuar analisando ela, já que não faz sentido pro outro jogador deixar esse posiçao ocorrer na partida
                    return beta
                
                if aval > alpha:
                    alpha = aval

        return alpha


    def evaluation(self):

        # verifica se a partida acabou
        if self.damas.game_result(self.damas.legalmoves()[1])[0]:
            return self.damas.game_result(self.damas.legalmoves()[1])[1]

        score = 0

        if self.damas.turn:
            # a avaliação também é em perspectiva
            side = 1
        else:
            side = -1

        # soma/subtrai 1 pra cada peça do cara/do adversário
        # soma/subtrai 3 pra cada dama do cara/do adversário
        for i in self.damas.board:
            for piece in i:
                if piece == 'w':
                    pass
                elif piece == 2:
                    score += 3
                elif piece == -2:
                    score -= 3
                else:
                    score += piece

        return score*side


    def analyse_move(self, move, capture_sequence):
        # Uma opção melhor pra realizar o lance:
        # sem verificação de legalidade, já que apenas lances legais são analisados pelo bot
        self.damas.lasttomove.append(self.damas.board[move[0][0]][move[0][1]])
        self.damas.board[move[1][0]][move[1][1]] = self.damas.board[move[0][0]][move[0][1]]
        self.damas.board[move[0][0]][move[0][1]] = 0
            
        if move[2]:
            self.damas.lastcaptured.append(self.damas.board[move[2][0]][move[2][1]])
            self.damas.piece_in_sequence.append(move[1])
            self.damas.board[move[2][0]][move[2][1]] = 0

        if ((move[1][1] == 0 and self.damas.turn) ^ (move[1][1] == 7 and not self.damas.turn)) and not (self.damas.board[move[1][0]][move[1][1]]**2 == 4):
            # verifica se é uma promoção de peça
            self.damas.board[move[1][0]][move[1][1]] = 2 * self.damas.board[move[1][0]][move[1][1]]
            self.damas.turn = not self.damas.turn
            self.damas.piece_in_sequence.append([])

        else:

            if capture_sequence < 2:
                #caso o lance não faça parte de uma sequência de capturas ou caso a sequência acabe nesse lance, muda o turno
                self.damas.piece_in_sequence.append([])
                self.damas.turn = not self.damas.turn
        
        self.damas.boardhistory.append(self.damas.copy(self.damas.board))


class random_Bot:
    # a classe usada para o modo fácil (escolhe movimentos aleatoriamente)
    def __init__(self, damas: Damas) -> None:
        self.damas = damas

    def botmove(self):
        movelist = self.damas.legalmoves()
        return self.damas.playermove(random.choice(movelist[1]), movelist)