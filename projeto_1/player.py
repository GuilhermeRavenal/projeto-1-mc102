### TODO: PREENCHA SUAS INFORMAÇÕES AQUI ###
# Nome #01 (quem entregou o código):    [NOME COMPLETO #01] 
# RA #01 (quem entregou o código):      [RA #01]
# Nome #02:                             [NOME COMPLETO #02]
# RA #02:                               [RA #02]


import random

CHUTE_DE_NUMERO = "NUMBER"
CHUTE_DE_REGRA = "RULE"

def player(number_guesses, rule_guesses):
    """Função principal do jogador. 
    
    Exemplo de estratégia: chutar regras aleatórias.
    """
    
    TIPO = random.choice(["mod", "pot", "int"])
    
    if TIPO == "mod":
        k = random.randint(2, 100)
        r = random.randint(0, k - 1)
        chute = [TIPO, k, r]
    elif TIPO == "pot":
        p = random.randint(2, 10)
        chute = [TIPO, p, 0]
    else:
        a = random.randint(1, 100_000) # Dica: o underline (_) pode ser usado para melhorar a legibilidade de números grandes em Python!
        b = random.randint(a, min(100_000, a + 100))
        chute = [TIPO, a, b]
    
    return [CHUTE_DE_REGRA, chute]