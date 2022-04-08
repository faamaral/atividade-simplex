from mimetypes import init

from numpy import void


class Simplex:

    def __init__(self):
        self.tableaus = []

    def set_funcao_objetivo(self, funcao_objetivo: list):
        self.tableaus.append(funcao_objetivo)

    def add_restricoes(self, restricoes: list):
        self.tableaus.append(restricoes)

    def get_coluna_entrada(self) -> int:
        # menor valor negativo da lista da função objetivo
        coluna_pivo = min(self.tableaus[0])
        # retorna o indice da coluna pivo
        return self.tableaus[0].index(coluna_pivo)

    def get_linha_saida(self, coluna_entreda: int) -> int:
        res = {}
        for linha in range(len(self.tableaus)):
            if linha > 0:
                if self.tableaus[linha][coluna_entreda] > 0:
                    res[linha] = self.tableaus[linha][-1] / \
                        self.tableaus[linha][coluna_entreda]

        # retorna o indice da linha da linha com o menor valor
        return min(res, key=res.get)

    def calcula_nova_linha_pivo(self, coluna_entrada : int, linha_saida : int) -> list:
        linha = self.tableaus[linha_saida]
        pivo = linha[coluna_entrada]

        # retorna a nova linha pivo
        return [valor / pivo for valor in linha]



    def calcula_nova_linha(self, linha: list, coluna_entrada: int, linha_pivo: list) -> list:
        pivo = linha[coluna_entrada] * -1
        linha_resultante = [valor * pivo for valor in linha_pivo]
        nova_linha = []
        for i in range(len(linha_resultante)):
            nova_linha.append(linha_resultante[i] + linha[i])

        return nova_linha

    '''Enquanto a primeira linha da tabela for negativa, a tabela deve ser recalculada'''

    def verifica_negativos(self) -> bool:
        negativo = list(filter(lambda x: x < 0, self.tableaus[0]))
        return True if len(negativo) > 0 else False

    def display(self):
        for linha in range(len(self.tableaus)):
            for coluna in range(len(self.tableaus[linha])):
                print(f"{self.tableaus[linha][coluna]}\t", end="")
            print()

    def calcular(self) -> void:
        coluna_entrada = self.get_coluna_entrada()
        linha_saida = self.get_linha_saida(coluna_entrada)
        linha_pivo = self.calcula_nova_linha_pivo(coluna_entrada, linha_saida)
        self.tableaus[linha_saida] = linha_pivo

        copia_tableaus = self.tableaus.copy()
        index = 0
        while index < len(self.tableaus):
            if index != linha_saida:
                linha = copia_tableaus[index]
                nova_linha = self.calcula_nova_linha(linha, coluna_entrada, linha_pivo)
                self.tableaus[index] = nova_linha
            index += 1

    def resolve(self) -> void:
        self.calcular()

        while self.verifica_negativos():
            self.calcular()
        self.display()


if __name__ == "__main__":
    '''
     MAX z = 2x1 + 3x2
     Sujeito a:x1 + x2 + w1 = 6
            2x1 + x2 + w2 = 10
            -x1 + x2 + w3 = 4
            x1, x2 >= 0

        forma simplex: 
        max    z - 2x1 - 3x2 = 0

        sa:    x1 + x2 + w1 = 6
            2x1 + x2 + w2 = 10
            -x1 + x2 + w3 = 4
            x1, x2 >= 0

        função objetivo: [1, -2, -3, 0, 0, 0, 0]
        restrições: [
            [0, 1, 1, 1, 0, 0, 6],
        [0, 2, 1, 0, 1, 0, 10],
         [0, -1, 1, 0, 0, 1, 4
        ]]

    '''
    simplex = Simplex()
    simplex.set_funcao_objetivo([1, -2, -3, 0, 0, 0, 0])
    simplex.add_restricoes([0, 1, 1, 1, 0, 0, 6])
    simplex.add_restricoes([0, 2, 1, 0, 1, 0, 10])
    simplex.add_restricoes([0, -1, 1, 0, 0, 1, 4])

    simplex.resolve()
