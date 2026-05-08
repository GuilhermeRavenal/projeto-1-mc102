### TODO: PREENCHA SUAS INFORMAÇÕES AQUI ###
# Nome #01 (quem entregou o código):    [NOME COMPLETO #01] 
# RA #01 (quem entregou o código):      [RA #01]
# Nome #02:                             [NOME COMPLETO #02]
# RA #02:                               [RA #02]

import random

CHUTE_DE_NUMERO = "NUMBER"
CHUTE_DE_REGRA = "RULE"

# variaveis global
fase = 0
t = None  # primeiro numero que deu True
low = 1
high = 100000
tried_rules = set()
last_rule_count = 0


def mdc(a, b):
    #Calcula o maximo divisor comum
    while b != 0:
        a, b = b, a % b
    return a

def player(number_guesses, rule_guesses):
    global fase, t, low, high, tried_rules, last_rule_count

    # checa se uma regra nova foi rejeitada e avanca de fase
    if len(rule_guesses) > last_rule_count:
        tried_rules.add(tuple(rule_guesses[-1]))
        last_rule_count = len(rule_guesses)
        if fase == 2:
            fase = 3
        elif fase == 3:
            fase = 4
        elif fase == 4:
            fase = 0   # se nada dar certo ele busca mais numeros

    trues = [n for (n, _, ok) in number_guesses if ok]
    falses_set = {n for (n, _, ok) in number_guesses if not ok}
    usados = {n for (n, _, _) in number_guesses}

    # --------------------------------------------------------
    # Fase 0 - busca binaria pra achar qualquer True
    if fase == 0:
        if not number_guesses:
            return [CHUTE_DE_NUMERO, 50000]

        ultimo = number_guesses[-1]

        if ultimo[2]:
            # achou um True :) guarda e vai explorar os vizinhos
            t = ultimo[0]
            fase = 1
        else:
            if ultimo[1] == "maior":
                low = ultimo[0] + 1
            else:
                high = ultimo[0] - 1
            MEIO = (low + high) // 2
            return [CHUTE_DE_NUMERO, MEIO]

    # --------------------------------------------------------
    # Fase 1 - explora pra esquerda e direita de t ate achar False
    if fase == 1:
        if t is None:
            fase = 0
            return [CHUTE_DE_NUMERO, (low + high) // 2]

        trues_esq = sorted([n for n in trues if n <= t])
        trues_dir = sorted([n for n in trues if n >= t])

        # extremo esquerdo ja confirmado como True
        INICIO_ATUAL = trues_esq[0] if trues_esq else t
        cand_esq = INICIO_ATUAL - 1

        # extremo direito ja confirmado como True
        FIM_ATUAL = trues_dir[-1] if trues_dir else t
        cand_dir = FIM_ATUAL + 1

        # so para de explorar se achou False ou saiu dos limites
        esq_pronta = cand_esq < 1 or cand_esq in falses_set
        dir_pronta = cand_dir > 100000 or cand_dir in falses_set

        if not esq_pronta and cand_esq not in usados:
            return [CHUTE_DE_NUMERO, cand_esq]
        if not dir_pronta and cand_dir not in usados:
            return [CHUTE_DE_NUMERO, cand_dir]

        # explorou o suficiente, parte pra tentar a regra
        fase = 2

    # --------------------------------------------------------
    # Fase 2 - tenta regra de intervalo com os limites encontrados
    if fase == 2:
        if len(trues) >= 1:
            falses_abaixo = [n for n in falses_set if n < min(trues)]
            falses_acima = [n for n in falses_set if n > max(trues)]

            # estima INICIO e FIM pelos falsos mais proximos dos trues
            INICIO = max(falses_abaixo) + 1 if falses_abaixo else 1
            FIM = min(falses_acima) - 1 if falses_acima else 100000

            chute = ("int", INICIO, FIM)
            if chute not in tried_rules:
                return [CHUTE_DE_REGRA, ["int", INICIO, FIM]]
        fase = 3

    # --------------------------------------------------------
    # Fase 3 -- tenta regra de potencia
    if fase == 3:
        if len(trues) >= 2:
            for p in range(2, 11):
                bate = True
                for n in trues:
                    raiz = round(n ** (1 / p))
                    if raiz ** p != n:
                        bate = False
                        break
                chute = ("pot", p, 0)
                if bate and chute not in tried_rules:
                    return [CHUTE_DE_REGRA, ["pot", p, 0]]
        fase = 4

    # --------------------------------------------------------
    # Fase 4 - tenta regra de mod
    if fase == 4:
        if len(trues) >= 2:
            trues_ord = sorted(trues)

            # pega todas as diferencas entre Trues consecutivos
            diferencas = []
            i = 0
            while i < len(trues_ord) - 1:
                dif = trues_ord[i + 1] - trues_ord[i]
                if dif > 0:
                    diferencas.append(dif)
                i = i + 1

            # calcula o MDC de todas as diferencas
            if diferencas:
                d = diferencas[0]
                for prox in diferencas[1:]:
                    d = mdc(d, prox)

                # se o MDC > 1, pode ser uma regra de mod
                if d > 1:
                    k = d
                    resto = trues_ord[0] % k
                    chute = ("mod", k, resto)
                    if chute not in tried_rules:
                        return [CHUTE_DE_REGRA, ["mod", k, resto]]

        # nao conseguiu identificar a regra com o que tem
        # volta a buscar mais numeros pra ter mais informacao
        fase = 0

    # --------------------------------------------------------
    # embicada de seguranca - busca binaria normal pra encontrar mais trues
    MEIO = (low + high) // 2
    tentativas = 0
    while MEIO in usados and tentativas < 100:
        if MEIO < 100000:
            MEIO = MEIO + 1
        else:
            MEIO = MEIO - 1
        tentativas = tentativas + 1

    return [CHUTE_DE_NUMERO, MEIO]