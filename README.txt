Para executar o jogo
 execute o arquivo game.py. 


Propósito do jogo
 é um jogo de damas normal, com tempo (o que eu chamei lá de ritmo) e com as seguintes regras (segui a página da wikipédia sobre 'brazilian draughts'):

-  É obrigatório comer o maior número de peças possível por lance (até para as damas)

-  Você pode e deve comer pra trás, mesmo com as peças normais

- Quando você captura uma peça com uma dama, você pode escolher qualquer canto pra parar depois (a menos que tenha outra peça sua atrás ou que você esteja obrigado a executar uma sequência de capturas)

- Se uma posição se repetir 3 vezes no tabuleiro ou se nenhum dos lados tiver lances legais, a 	partida empata

Inclusive, caso você tente fazer um lance e não consiga, provavelmente é por causa da primeira regra (acontece comigo o tempo todo)

Sobre o tempo:

- O tempo é para a partida inteira e não apenas para o lance

- Se seu o tempo acabar, você perde

- O tempo só corre durante a sua vez e, sempre que você executa um lance, você ganha alguns segundos de acréscimo

- No menu, você pode escolher o ritmo da partida (seu tempo). O primeiro número indica quantos 	minutos você terá no relógio e o segundo, quantos segundos você terá de acréscimos


Organização do código
o código está dividido em 4 arquivos:

- damas.py, contem a classe que lida com a execução de lances, com o armazenamento do estado do tabuleiro, com a criação da lista de lances legais e verificação do resultado da partida

- clock.py, contem a classe que cria, armazena, atualiza e incrementa o tempo do 	relógio

- bot.py, contem duas classes, uma pro bot fácil que faz lances aleatórios, e outra pro bot difícil que 	vasculha pelos lances possíveis procurando a melhor alternativa

- game.py, faz o jogo rodar lidando com as bibliotecas e ilustrando a janela com o pygame

