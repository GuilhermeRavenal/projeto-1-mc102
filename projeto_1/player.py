### TODO: PREENCHA SUAS INFORMAÇÕES AQUI ###
# Nome #01 (quem entregou o código):    [NOME COMPLETO #01] 
# RA #01 (quem entregou o código):      [RA #01]
# Nome #02:                             [NOME COMPLETO #02]
# RA #02:                               [RA #02]

import random

CHUTE_DE_NUMERO = "NUMBER"
CHUTE_DE_REGRA = "RULE"

# variaveis globais de estado
fase = 0
t = None # primeiro numero que deu True
low = 1
high = 100000
next_offset = 1
last_rule_count = 0
tried_rules = set()

def _reiniciar():
    global fase, t, low, high, next_offset, last_rule_count, tried_rules
    fase = 0
    t = None
    low = 1
    high = 100000
    next_offset = 1
    last_rule_count = 0
    tried_rules = set()

def _pegar_inicio_fim(number_guesses):
    # percorre a lista toda pra achar o low e high mais recentes
    # (ideia da camila de varrer a lista)
    INICIO = 1
    FIM = 100000
    POS = -1
    for i in number_guesses:
        if number_guesses[POS][1] == 'maior':
            INICIO = number_guesses[POS][0] + 1
            break
        POS -= 1
    POS = -1
    for i in number_guesses:
        if number_guesses[POS][1] == 'menor':
            FIM = number_guesses[POS][0] - 1
            break
        POS -= 1
    return INICIO, FIM

def _checar_potencia(trues):
    # ideia da camila: testa se a raiz da um numero "redondo"
    for p in range(2, 11):
        todos_ok = True
        for num in trues:
            raiz = num ** (1 / p)
            raiz_str = str(raiz)
            casas = raiz_str.split('.')[1]
            # se so tem 1 casa decimal assume que e inteiro
            if len(casas) > 1:
                todos_ok = False
                break
        if todos_ok == True:
            return p
    return None

def _checar_intervalo(trues):
    # so tenta se tiver pelo menos 4 Trues consecutivos
    if len(trues) < 4:
        return None
    ordenados = sorted(trues)
    for i in range(len(ordenados) - 3):
        if (ordenados[i+1] - ordenados[i] == 1 and
            ordenados[i+2] - ordenados[i+1] == 1 and
            ordenados[i+3] - ordenados[i+2] == 1):
            return (ordenados[i], ordenados[i+3])
    return None

def _checar_mod(trues):
    # verifica se as diferencas consecutivas sao iguais
    if len(trues) < 3:
        return None
    ordenados = sorted(trues)
    k1 = ordenados[1] - ordenados[0]
    k2 = ordenados[2] - ordenados[1]
    if k1 == k2 and k1 > 1:
        return (k1, ordenados[0] % k1)
    return None

def player(number_guesses, rule_guesses):
    global fase, t, low, high, next_offset, last_rule_count, tried_rules

    # nova partida
    if len(number_guesses) == 0 and len(rule_guesses) == 0:
        _reiniciar()
        return [CHUTE_DE_NUMERO, 50000]

    # atualiza tried_rules se entrou regra nova
    if len(rule_guesses) > last_rule_count:
        tried_rules.add(tuple(rule_guesses[-1]))
        last_rule_count = len(rule_guesses)

        # regra foi rejeitada, avanca fase
        if fase == 2:
            fase = 3
        elif fase == 3:
            fase = 4
        elif fase == 4:
            fase = 0

    # lista de todos os Trues ate agora
    trues = [n for (n, _, ok) in number_guesses if ok]

    # -------------------------------------------------------
    # Fase 0 -- achar um True via busca binaria
    if fase == 0:
        if not number_guesses:
            return [CHUTE_DE_NUMERO, 50000]

        ultimo = number_guesses[-1]

        if ultimo[2] == True:
            t = ultimo[0]
            fase = 1
            next_offset = 1
        else:
            # atualiza intervalo e chuta o meio
            # usa _pegar_inicio_fim que varre a lista toda
            INICIO, FIM = _pegar_inicio_fim(number_guesses)
            low = INICIO
            high = FIM
            MEIO = ((FIM - INICIO) // 2) + INICIO
            return [CHUTE_DE_NUMERO, MEIO]

    # -------------------------------------------------------
    # Fase 1 - testar vizinhos do t pra entender a regra
    if fase == 1:
        usados = {n for (n, _, _) in number_guesses}

        # testa 4 vizinhos proximos
        for delta in (1, -1, 2, -2):
            cand = t + delta
            if 1 <= cand <= 100000 and cand not in usados:
                return [CHUTE_DE_NUMERO, cand]

        # testou os 4 vizinhos, vai tentar deduzir a regra
        fase = 2

    # -------------------------------------------------------
    # Fase 2 - tenta regra de intervalo
    if fase == 2:
        resultado = _checar_intervalo(trues)
        if resultado != None:
            esq, dir = resultado
            chute_regra = ("int", esq, dir)
            if chute_regra not in tried_rules:
                return [CHUTE_DE_REGRA, ["int", esq, dir]]
        # nao achou intervalo obvio, tenta potencia
        fase = 3

    # -------------------------------------------------------
    # Fase 3 - tenta regra de potencia
    if fase == 3:
        if len(trues) >= 2:
            p = _checar_potencia(trues)
            if p != None:
                chute_regra = ("pot", p, 0)
                if chute_regra not in tried_rules:
                    return [CHUTE_DE_REGRA, ["pot", p, 0]]
        fase = 4

    # -------------------------------------------------------
    # Fase 4 - tenta regra de mod
    if fase == 4:
        resultado = _checar_mod(trues)
        if resultado != None:
            k, r = resultado
            chute_regra = ("mod", k, r)
            if chute_regra not in tried_rules:
                return [CHUTE_DE_REGRA, ["mod", k, r]]

        # nao achou nenhuma regra, precisa de mais numeros
        # coleta mais Trues explorando a partir do t
        if t != None:
            usados = {n for (n, _, _) in number_guesses}
            while next_offset <= 500:
                cand = t + next_offset
                next_offset = next_offset + 1
                if 1 <= cand <= 100000 and cand not in usados:
                    return [CHUTE_DE_NUMERO, cand]

        # se chegou aqui, volta ao inicio e tenta achar outro True
        fase = 0
        low = 1
        high = 100000

    # embicada de segurança: busca binaria simples no intervalo atual
    guess = (low + high) // 2
    used = {n for (n, _, _) in number_guesses}

    tentativas = 0
    while guess in used and tentativas < 100:
        guess = guess + 1 if guess < 100000 else guess - 1
        tentativas = tentativas + 1

    return [CHUTE_DE_NUMERO, guess]