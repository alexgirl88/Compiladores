import re

alfab = "$()+-._0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

estFinais = {1:"NUM", 2:"NUM", 4:"ID", 6:"ID", 7:"ID", 8:"ID", 9: "ID", 10: "ID", 11: "ID", 12: "IMPRIMIR", 13: "+", 14: "-", 15: "(", 16: ")", 
                 17:"ID", 18:"SE", 19 : "ID", 20: "ID", 21:"ID", 22: "PARA", 23: "ID", 24: "ID", 25: "ID", 26: "ID", 27: "ID", 28: "ID", 29: "ID", 
                 30: "ENQUANTO", 32: "CONST", 33: "CONST"}
grafo = [
          (0, "[0-9]", 1), (1, "[0-9]", 1), (1, "[.]", 2), (2, "[0-9]", 2), (0, "[.]", 3), (3, "[0-9]", 2), (0, "[a-z]", 4), (0, "[a-z$]", 5), 
          (5, "[a-z 0-9_]", 6), (6, "[a-z 0-9_]", 6), (0, "[i]", 7), (7, "[m]", 8), (8, "[p]", 9), (9, "[r]", 10), (10, "[i]", 11), (11, "[r]", 12), (0, "[+]", 13), 
          (0, "[-]", 14), (0, "[(]" , 15), (0, "[)]", 16), (0,"[s]", 17), (17, "[e]", 18), (0, "[p]", 19), (19, "[a]" , 20), (20, "[r]", 21),
          (21, "[a]", 22), (0, "[e]", 23), (23, "[n]", 24), (24, "[q]", 25), (25, "[u]", 26), (26, "[a]", 27), (27, "[t]", 29), (29, "[o]", 30),
          (0, "[A-Z]", 32),  (32, "[A-Z0-9_]", 33), (33, "[A-Z0-9_]", 33)
        ]


delta = []
N = 50
M = 300

def initDelta():
    for i in range(0, N):
        linha = []
        for j in range(0, M):
            linha.append(-1)
        delta.append(linha)

def conecta(v, expressaoRegular, u):
    padrao = re.compile(expressaoRegular)
    listaSimbolos = padrao.findall(alfab)
    for simbolo in listaSimbolos:
        delta[v][ord(simbolo)] = u

def buildDelta():
    initDelta()
    for aresta in grafo:
        v = aresta[0]
        expressaRegular = aresta[1]
        u = aresta[2]
        conecta(v, expressaRegular, u)
        
def mySplit(arquivo):
    l = []
    for linha in arquivo:
        for simb in linha:
            l.append(simb)
    return l

def geraTokens(arquivo):
    listaTokens = []
    indice = 0
    l = mySplit(arquivo)
    while True:
        lexema = ""
        pilha = []
        estadoAtual = 0
        if indice == len(l):
            break
        while(indice < len(l)):
            simbolo = str(l[indice])            
            if delta[estadoAtual][ord(simbolo)] == -1:
                break
            lexema += simbolo
            pilha.append(estadoAtual)
            estadoAtual = delta[estadoAtual][ord(simbolo)]
            indice+=1  
        while not (estadoAtual in estFinais) and pilha:
            estadoAtual = pilha.pop()
            lexema = lexema[0:len(lexema)-1]
            indice -= 1
        if not pilha:
            print("Erro")
            exit(0)
        listaTokens.append( (estFinais[estadoAtual], lexema) )
    return listaTokens


def main():
    buildDelta()
    arq = open("/CompiladoresAlexandra.txt", "r")
    arquivo = arq.readlines()
    print(geraTokens(arquivo))

if __name__ == "__main__":
    main()
