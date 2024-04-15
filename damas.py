class Damas:
    def __init__(self) -> None:

        self.board = [['w', -1, 'w', 0, 'w', 1, 'w', 1],  #a8      a1
                      [-1, 'w', -1, 'w', 0, 'w', 1, 'w'],
                      ['w', -1, 'w', 0, 'w', 1, 'w', 1], 
                      [-1, 'w', -1, 'w', 0, 'w', 1, 'w'],
                      ['w', -1, 'w', 0, 'w', 1, 'w', 1],
                      [-1, 'w', -1, 'w', 0, 'w', 1, 'w'], 
                      ['w', -1, 'w', 0, 'w', 1, 'w', 1], 
                      [-1, 'w', -1, 'w', 0, 'w', 1, 'w']] #h8       h1
        
        # representa o estado atual do tabuleiro:
        # w -> casa branca
        # 0 -> casa negra sem peça
        # 1 -> casa com peça branca
        # -1 -> casa com peça preta
        # 2 -> casa com dama branca
        # -2 -> casa com dama preta
        self.boardhistory = []

        self.lastcaptured = []
        # armazena qual foi a ultima peça capturada para uso no método undo()

        self.piece_in_sequence = []

        self.lasttomove = []

        self.turn = True
        # diz de quem é a vez: true = brancas, false = pretas

        # movimentos são representados por listas com 3 elementos:
        #   1. uma lista com as coordednadas da casa inicial
        #   2. outra lista com as coordednadas da casa final
        #   3. uma lista com as coordenadas da peça que foi capturada durante o movimento (caso não haja captura, a lista estará vazia)


    def playermove(self, move, lm = []):
        # função que tenta realizar o lance do jogador
        if len(move) == 2:
            # caso seja um lance do jogador, verifica se é uma captura e vê quais lances são legais
            # caso o lance seja executado por um bot, ele terá lenght = 3 e a lista de movimentos legais será dada
            move = self.is_capture(move)
            lm = self.legalmoves()
            #print('piece:', self.board[move[0][0]][move[0][1]])
            #print('move:', move)
            #print('legal moves:', lm)

        if move in lm[1]:
            # verifica se o lance é legal e o realiza
            self.lasttomove.append(self.board[move[0][0]][move[0][1]])

            if move[2]:
                # caso seja uma captura, retira a peça do jogo
                self.lastcaptured.append(self.board[move[2][0]][move[2][1]])
                self.board[move[2][0]][move[2][1]] = 0
                self.piece_in_sequence.append(move[1])

            if ((move[1][1] == 0 and self.turn) ^ (move[1][1] == 7 and not self.turn)) and not (self.board[move[0][0]][move[0][1]]**2 == 4):
                # verifica se é uma promoção de peça
                self.board[move[1][0]][move[1][1]] = 2 * self.board[move[0][0]][move[0][1]]
                self.turn = not self.turn
                self.piece_in_sequence.append([])

            else:
                # realiza o movimento
                self.board[move[1][0]][move[1][1]] = self.board[move[0][0]][move[0][1]]

                if lm[0] < 2:
                    #caso o lance não faça parte de uma sequência de capturas ou caso a sequência acabe nesse lance, muda o turno
                    self.piece_in_sequence.append([])
                    self.turn = not self.turn

            self.board[move[0][0]][move[0][1]] = 0
            self.boardhistory.append(self.copy(self.board))
            return move

    def is_there_capture_after(self, move):
        # faz o lance no tabuleiro e depois verifica se há uma sequência de capturas (para uso no self.most_captures())
        self.lasttomove.append(self.board[move[0][0]][move[0][1]])
        self.board[move[1][0]][move[1][1]] = self.board[move[0][0]][move[0][1]]
        self.board[move[0][0]][move[0][1]] = 0
            
        if move[2]:
            self.lastcaptured.append(self.board[move[2][0]][move[2][1]])
            self.piece_in_sequence.append(move[1])
            self.board[move[2][0]][move[2][1]] = 0

        if ((move[1][1] == 0 and self.turn) ^ (move[1][1] == 7 and not self.turn)) and not (self.board[move[1][0]][move[1][1]]**2 == 4):
            # verifica se é uma promoção de peça
            self.board[move[1][0]][move[1][1]] = 2 * self.board[move[1][0]][move[1][1]]
            self.turn = not self.turn
            self.piece_in_sequence.append([])
                
        elif self.legalmoves()[0] < 1:
            self.turn = not self.turn

        
    def legalmoves(self):
        # retorna uma lista de lances legais e o tamanho da sequência de capturas caso haja uma
        moves = []
        capturas = []

        for i in range(8):
            for j in range(8):
                # verifica os lances possíveis de cada peça do tabuleiro
                if (i+j)%2 and self.is_white([i, j]) == self.turn:
                    for move in self.piecemoves([i, j]):
                        if move[2]:
                            capturas.append(move)
                        else:
                            moves.append(move)

        if len(capturas):
            # caso haja captura de peça, identifica se há e qual é a maior sequência

            if self.piece_in_sequence[-1]:
                # se estiver no meio de uma sequência de capturas, considera apenas as capturas que posem ser feitas pela peça que iniciou a sequência
                movestop = []

                for move in capturas:
                    if move[0] == self.piece_in_sequence[-1]:
                        # verifica se a captura foi realizada pela peça que ta na sequência
                        movestop.append(move)
                
                return self.most_captures(movestop)

            else:
                # se não estiver numa sequência retorna capturas feitas por qualquer peça
                lista =  self.most_captures(capturas)
                return lista

        else:
            return 0, moves



    def piecemoves(self, piece, capture_sequence = 0):
        # gera os possíveis lances para uma única peça
        if 0 == self.board[piece[0]][piece[1]]:
            # caso não haja peça nessa casa
            return []

        elif 1 == self.board[piece[0]][piece[1]]**2:
            # caso seja uma peça normal, verifica o que há nas 4 casas diagonais à peça
            # os movimentos para trás também estão inclusos, mas apenas para verificar se há possibilidade de captura
            moves = [[piece, [piece[0]+1, piece[1] - 1], []], [piece, [piece[0]-1, piece[1] - 1], []], 
                    [piece, [piece[0] + 1, piece[1] + 1], []], [piece, [piece[0] - 1, piece[1] + 1], []]]
            movestop = []

            for move in moves:
                c = piece[1] - move[1][1]

                if move[1][0] > 7 or move[1][0] < 0 or move[1][1] > 7 or move[1][1] < 0:
                    # descarta o lance caso ele vá pra fora do tabuleiro
                    pass
                
                elif (self.board[piece[0]][piece[1]] > 0) == (self.board[move[1][0]][move[1][1]] > 0) and  (self.board[move[1][0]][move[1][1]] != 0):
                    # descarta o lance caso ele termine numa peça de mesma cor
                    pass

                elif (self.board[piece[0]][piece[1]] > 0) == (self.board[move[1][0]][move[1][1]] < 0) and  (self.board[move[1][0]][move[1][1]] != 0):
                    # caso o lance sejá em direção a uma peça adversária, verifica se é possível capturá-la
                    l = move[1][0] - piece[0]

                    if 0 <= (move[1][1] - c) < 8 and 0 <= (move[1][0] + move[1][0] - piece[0]) < 8 and not self.board[move[1][0] + l][move[1][1] - c]:
                        movestop.append([piece, [move[1][0] + l, move[1][1] - c], [move[1][0], move[1][1]]])

                elif c != self.board[move[0][0]][move[0][1]]:
                    # descarta o lance caso ele vá pra traz mas não seja uma captura
                    pass

                else:
                    # caso não tenha uma peça na casa, guarda o lance
                    movestop.append(move)

        else:
            # caso a peça seja uma dama
            movestop = self.damasmovement(piece)

        if capture_sequence:
            # caso tenha sido chamado pelo most_captures(), retorna o lance que faz parte da maior sequência de capturas possível pra essa peça
            captures = []

            for move in movestop:
                if move[2]:
                    captures.append(move)

            return self.most_captures(captures)[0] + capture_sequence

        return movestop

    def damasmovement(self, dama):
        # gera os lances possíveis pras damas
        moves = []

        for c, l in [(1,1),(-1,1),(-1,-1),(1,-1)]:
            # vê quais lances são possíveis em todas as 4 direções (o 'c' indica a direção vertical e o 'l' a horizontal)
            for x in range(1, 7):

                if  0 > dama[0] + l*x or dama[0] + l*x > 7 or 0 > dama[1] + c*x or dama[1] + c*x > 7:
                    # caso vá para fora do tabuleiro, interrompe a busca nessa direção
                    break

                elif (self.board[dama[0]][dama[1]] > 0) == (self.board[dama[0] + l*x][dama[1] + c*x] > 0) and (self.board[dama[0] + l*x][dama[1] + c*x] != 0):
                    # caso chegue numa peça de mesma cor, interrompe a busca nessa direção
                    break

                elif (self.board[dama[0]][dama[1]] > 0) == (self.board[dama[0] + l*x][dama[1] + c*x] < 0) and (self.board[dama[0] + l*x][dama[1] + c*x] != 0):
                    # caso o lance sejá em direção a uma peça adversária, verifica se é possível capturá-la e gera todas as posições finais possíveis
                    for y in range(1, 7-x):
                        # passa pelas casas atrás da peça adversária pra verificar em quais casas a dama pode parar
                        if 0 <= dama[0] + l*x + y*l < 8 and 0 <= dama[1] + c*x + y*c < 8 and not self.board[dama[0] + l*x + y*l][dama[1] + c*x + y*c]:
                            
                            moves.append([dama, [dama[0] + l*x + y*l, dama[1] + c*x + y*c], [dama[0] + l*x, dama[1] + c*x]])
                        
                        else:
                            # caso chegue numa casa em que não é possível pousar, interrompe a busca nessa direção
                            break
                    break

                else:
                    # caso não hja captura de peça, garda a opção de lance 
                    moves.append([dama, [dama[0] + l*x, dama[1] + c*x], []])

        return moves
            


    def is_capture(self, move: list):
        # identifica sé o conjunto posição inicial/final executado pelo jogador é uma captura
        move.append([])

        if self.board[move[0][0]][move[0][1]] == 0:
            pass
        
        elif self.board[move[0][0]][move[0][1]]**2 == 1:
            # caso uma peça normal esteja se movendo, só verifica o que há na casa entre o iníciodo pulo e o final
            c = (move[1][1]-move[0][1])//2
            
            l = 1 if move[0][0] < move[1][0] else -1
            l = 0 if move[0][0] == move[1][0] else l
                
            if self.board[move[1][0] - l][move[1][1] - c] != 'w' and (self.board[move[0][0]][move[0][1]] > 0) == (self.board[move[1][0] - l][move[1][1] - c] < 0) and  (self.board[move[1][0] - l][move[1][1] - c] != 0):
                move[2] = [move[1][0] - l, move[1][1] - c]
            
        else:
            # caso uma dama esteja se movendo, verifica todas as casas entre a inicial e a final em busca de uma peça inimiga
            c = -1 if move[0][1] > move[1][1] else 1

            l = -1 if move[0][0] > move[1][0] else 1

            for a in range(7):
                if move[0][0] + l*a == move[1][0] or move[0][1] + c*a == move[1][1]:
                    break

                elif (self.board[move[0][0]][move[0][1]] > 0) == (self.board[move[0][0] + l*a][move[0][1] + c*a] < 0) and (self.board[move[0][0] + l*a][move[0][1] + c*a] != 0):
                    move[2] = [move[0][0] + l*a, move[0][1] + c*a]
                    break
                  
        return move

    def most_captures(self, movelist):
        # dada uma lista de possíveis capturas, retorna a que inicie a maior sequência de capturas e o tamanho da sequência
        if not movelist:
            return [0, []]

        most = [1, []]
        for move in movelist:
            self.is_there_capture_after(move)

            if self.piece_in_sequence[-1]:
                # se ainda estiver numa sequência (leia-se não foi uma coroação) verifica o quão longa ela é
                nota = self.piecemoves(move[1], 1)

            else:
                # caso uma coroação tenha ocorrido, encerra a sequência
                nota = 1
                self.piece_in_sequence.pop()

            self.undo(move, in_history = False)
            
            if nota == most[0]:
                most[1].append(move)

            elif nota > most[0]:
                most = [nota, [move]]
  
        return most
            
    def undo(self, move, in_history = True):
        # desfaz o último lance
        self.board[move[0][0]][move[0][1]] = self.lasttomove[-1]
        self.board[move[1][0]][move[1][1]] = 0
        self.lasttomove.pop()
        if move[2]:
            #self.board[move[2][0]][move[2][1]] = -1 if self.board[move[0][0]][move[0][1]] == 1 else 1
            self.board[move[2][0]][move[2][1]] = self.lastcaptured[-1]
            self.lastcaptured.pop()
            self.piece_in_sequence.pop()
            #self.lastcaptured = 0
        
        self.turn = True if self.board[move[0][0]][move[0][1]] > 0 else False

        if in_history and len(self.boardhistory):
            # caso a posição estivesse no histórico (leia-se: não foi feito no self.is_there_capture_after()), apaga a ultima posição
            self.boardhistory.pop()
        

    def game_result(self, legalmoves):
        # Verifica se a partida acabou

        if not len(legalmoves):
            self.turn = not self.turn

            if not len(self.legalmoves()):
                # se apenas um dos lados não tem lances legais, ele perdeu
                self.turn = not self.turn
                return (True, 0)
            else:
                # se os dois lados não tem lances legais, é um empate
                self.turn = not self.turn
                return (True, -100)

        else:
            # se uma posição se repetiu 3 vezes, há um empate
            lista = []
            for z in self.boardhistory:
                if z == self.board:
                    lista.append(1)
            print(lista)
            if len(lista) >= 3:
                return [True, 0]
            else:
                return [False, 0]

    def is_white(self, piece):
        # diz se a peça dada é branca
        return (self.board[piece[0]][piece[1]] > 0)

    def copy(self, board):
        # fiz essa função pra conseguir adicionar posições ao histórico do tabuleiro, pois não consegui fazer dar certo usando self.boardhistory.append(self.board[:])
        # se eu tivesse tido a ideia de fazer essa função antes, teria economizado muita dor de cabeça com a função undo() afff
        copia = []
        for coluna in board:
            copia.append([])
            for casa in coluna:
                copia[-1].append(casa)

        return copia