from aigyminsper.search.search_algorithms import BuscaLargura, BuscaProfundidade, BuscaProfundidadeIterativa
from aigyminsper.search.csp_algorithms import SubidaMontanhaEstocastico
from aigyminsper.search.graph import State
import numpy as np
import random
import time
import copy

class N_QueensProblem(State):
  

    # ([x,y] , 0) # vazio 
    # ([x, y], 1) # com dama 
    # ([x,y], 2) # marcado


    def __init__(self, op, size, board):
        self.size = size
        self.board = board

    def gera_marcacoes(self, board):

        for i in range(self.size**2):
            if board[i][1] == 2:
                board[i][1] = 0

        for i in range(self.size**2):
            x = board[i][0][0]
            y = board[i][0][1]
            estado = board[i][1]

            if estado == 1:
                for j in range(self.size):
                    for k in range(self.size):
                        idx  = j * self.size + k # converte para o indice na board
                        if (j == x) or (k == y) or (abs(j - x) == abs(k - y)):
                            if board[idx][1] == 0:
                                board[idx][1] = 2
        return board
                
    def env(self):
        return self.board
    
    def successors(self):
        successors = []
        posicoes_vazias = [i for i in range(self.size ** 2) if self.board[i][1] == 0]

        if not posicoes_vazias:
            return []
        for indice in posicoes_vazias:
            board_copia = []
            for p in range(self.size ** 2):
                xi = self.board[p][0][0]
                yi = self.board[p][0][1]
                ei = self.board[p][1]
                board_copia.append([[xi, yi], ei])
            board_copia[indice][1] = 1

            board_copia = self.gera_marcacoes(board_copia)

            successors.append(N_QueensProblem("preencher", self.size, board_copia))

        return successors
                      
    def is_goal(self):
        qtd_damas = 0
        for i in range(self.size ** 2):
            if self.board[i][1] == 1:
                qtd_damas += 1
        return qtd_damas == self.size

    
    def description(self):
        return "Queens Problem"
    
    def cost(self):
        return 1
    

def main():
    def imprime_tabuleiro(board):
        N = max(max(x, y) for (x, y), _ in board) + 1
        matriz = [[0] * N for _ in range(N)]
        for (x, y), e in board:
            matriz[x][y] = e

        for linha in matriz:
            print(" ".join(
                "[ ]" if e == 0 else " D " if e == 1 else " P "
                for e in linha
            ))
    N = int(input("Digite o tamanho do tabuleiro (4-8): "))
    
    boardus = []
    for i in range(N):
        for j in range(N):
            boardus.append([[i,j], 0])

    state = N_QueensProblem("", size = N, board = boardus)
    start = time.time()
    algorithm = BuscaProfundidade()
    result = algorithm.search(state, m =N)
    end = time.time()
    tabuleiro = result.state.env()
    if result != None:
        print("Achou")
        imprime_tabuleiro(tabuleiro)

        print(f"Tempo de execução {end-start:2f} segundos") 
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()