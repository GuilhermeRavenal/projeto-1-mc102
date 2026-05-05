### TODO: PREENCHA SUAS INFORMAÇÕES AQUI ###
# Nome #01 (quem entregou o código):    [NOME COMPLETO #01] 
# RA #01 (quem entregou o código):      [RA #01]
# Nome #02:                             [NOME COMPLETO #02]
# RA #02:                               [RA #02]


import random

CHUTE_DE_NUMERO = "NUMBER"
CHUTE_DE_REGRA = "RULE"

fase = 0
t = None #grava o primeiro numero que da ok
#para busca binaria
low = 1
high = 100000

def player(number_guesses, rule_guesses):
    global fase, t, low, high

    if len(rule_guesses) > 0:
        fase = 0
        t = None
        low = 1
        high = 100000

    #pegando todos os numeros que deram OK
    trues = [n for (n, _, ok) in number_guesses if ok]

    #------------------------------------------------------
    # Fase 0 -- Achar um True
    if fase == 0:
        if not number_guesses:
            #chute inicial alto
            return [CHUTE_DE_NUMERO, 50000]
        
        ultimo = number_guesses[-1]
    
        if ultimo[2]: # True!! achou :)
            t = ultimo[0]
            fase = 1
        else:

            if ultimo[1] == "maior":
                low = ultimo[0] + 1
            else:
                high = ultimo[0] - 1
            
            return [CHUTE_DE_NUMERO, (low + high) // 2]
        
    #------------------------------------------------------
    # Fase 1 - Testar os vizinhos
    if fase == 1:
        # mais ou menos um teste binário : ) quis dar um reforço
        if len(trues) == 1:
            return [CHUTE_DE_NUMERO, t + 1]
        elif len(trues) == 2:
            return [CHUTE_DE_NUMERO, min(100000, t + 2)]
        elif len(trues) == 3:
            return [CHUTE_DE_NUMERO, max(1, t - 1)]
        else:
            fase = 2
    #------------------------------------------------------
    # Fase 2 - detectando intervalo
    if fase == 2:
        """ 
        Antes eu tinha tentado pra mudar de fasecom só dois Oks.
        Deu errado, melhor 3 acertos contínuos, pra dar certeza
        """
        if (t + 1 in trues and t + 2 in trues) or (t - 1 in trues and t - 2 in trues):
            a = min(trues)
            b = max(trues)
            return [CHUTE_DE_REGRA, ["int", a, b]]
        else:
            fase = 3

    #------------------------------------------------------
    # Fase 3 - regra pot agr
    if fase == 3:
        for p in range(2, 11):
            ok = True
            for n in trues:
                raiz = round(n ** (1/p))
                if raiz ** p != n:
                    ok = False
                    break
            if ok and len(trues) >= 2:
                return [CHUTE_DE_REGRA, ["pot", p, 0]]
        fase = 4

    #------------------------------------------------------
    #unico que tenho mais certeza que funciona.... 
    # Fase 4 - assumir o MOD
    if fase == 4:
        if len(trues) >= 2:
            trues.sort()
            k = trues[1] - trues[0]
            if k > 0:
                r = trues[0] % k
                return [CHUTE_DE_REGRA, ["mod", k, r]]

        
    # embicada de segurança (versão 4.2) melhorada pqp
    guess = (low + high) // 2

    if guess in [n for (n, _, _) in number_guesses]:
        guess = min(100000, guess + 1)

    return [CHUTE_DE_NUMERO, guess]