### TODO: PREENCHA SUAS INFORMAÇÕES AQUI ###
# Nome #01 (quem entregou o código):    [NOME COMPLETO #01]
# RA #01 (quem entregou o código):      [RA #01]
# Nome #02:                             [NOME COMPLETO #02]
# RA #02:                               [RA #02]


CHUTE_DE_NUMERO = "NUMBER"
CHUTE_DE_REGRA = "RULE"

# -------------------------------------------------
# Estado global da partida
# -------------------------------------------------

fase = "buscar"          # fase atual do algoritmo
low = 1                  # limite inferior da busca
high = 100000            # limite superior da busca
anchor = None            # primeiro número que deu True

# Para intervalo
left_true = None
right_true = None

# Para potência perfeita
pot_exp = 1
pot_results = {}
pot_found = None

# Para mod
mod_scan_dist = 1
mod_scan_side = 1
mod_other_true = None
mod_k = None

# Para não repetir regras já chutadas
tried_rules = set()

# Para processar só os novos itens do histórico
processed_number_count = 0
processed_rule_count = 0


def _reset():
    """Reinicia tudo quando uma nova partida começa."""
    global fase, low, high, anchor
    global left_true, right_true
    global pot_exp, pot_results, pot_found
    global mod_scan_dist, mod_scan_side, mod_other_true, mod_k
    global tried_rules
    global processed_number_count, processed_rule_count

    fase = "buscar"
    low = 1
    high = 100000
    anchor = None

    left_true = None
    right_true = None

    pot_exp = 1
    pot_results = {}
    pot_found = None

    mod_scan_dist = 1
    mod_scan_side = 1
    mod_other_true = None
    mod_k = None

    tried_rules = set()

    processed_number_count = 0
    processed_rule_count = 0


def _mid(a, b):
    """Ponto médio inteiro."""
    return (a + b) // 2


def _gcd(a, b):
    """Máximo divisor comum."""
    while b != 0:
        a, b = b, a % b
    return a


def _used_numbers(number_guesses):
    """Conjunto com todos os números já chutados."""
    return {g[0] for g in number_guesses}


def _normalize_rule(item):
    """
    A entrada de rule_guesses pode vir como:
      - [tipo, p1, p2]
      - ou algo aninhado no primeiro elemento
    Esta função padroniza para uma tupla simples.
    """
    if item and isinstance(item[0], (list, tuple)):
        return tuple(item[0])
    return tuple(item)


def _process_rules(rule_guesses):
    """Registra as regras que já foram chutadas."""
    global processed_rule_count, tried_rules

    while processed_rule_count < len(rule_guesses):
        tried_rules.add(_normalize_rule(rule_guesses[processed_rule_count]))
        processed_rule_count += 1


def _infer_pot():
    """
    Tenta descobrir qual p (1 a 10) encaixa no padrão
    dos testes 2^1, 2^2, ..., 2^10.

    Se n é potência perfeita de ordem p, então 2^e também é
    potência perfeita exatamente quando e é múltiplo de p.
    """
    for p in range(1, 11):
        ok = True
        for e in range(1, 11):
            esperado = (e % p == 0)
            if pot_results.get(e) != esperado:
                ok = False
                break
        if ok:
            return p
    return None


def _process_number_guess(chute, direcao, ok):
    """
    Atualiza o estado interno usando o resultado do último chute de número.
    """
    global fase, low, high, anchor
    global left_true, right_true
    global pot_exp, pot_results, pot_found
    global mod_scan_dist, mod_scan_side, mod_other_true, mod_k

    # 1) Ainda procurando um número verdadeiro
    if fase == "buscar":
        if ok:
            anchor = chute
            fase = "check_left"
        else:
            if direcao == "maior":
                low = max(low, chute + 1)
            else:
                high = min(high, chute - 1)
        return

    # 2) Testando o vizinho da esquerda
    if fase == "check_left":
        if ok:
            left_true = chute
            fase = "expand_left"
        else:
            fase = "check_right"
        return

    # 3) Testando o vizinho da direita
    if fase == "check_right":
        if ok:
            right_true = chute
            fase = "expand_right"
        else:
            fase = "test_pot"
            pot_exp = 1
            pot_results = {}
        return

    # 4) Expandindo a faixa contínua para a esquerda
    if fase == "expand_left":
        if ok:
            left_true = chute
        else:
            fase = "expand_right"
        return

    # 5) Expandindo a faixa contínua para a direita
    if fase == "expand_right":
        if ok:
            right_true = chute
        else:
            fase = "emit_int"
        return

    # 6) Testando potências perfeitas com 2^1, 2^2, ..., 2^10
    if fase == "test_pot":
        pot_results[pot_exp] = ok
        pot_exp += 1

        if pot_exp > 10:
            p = _infer_pot()
            if p is not None:
                pot_found = p
                fase = "emit_pot"
            else:
                fase = "collect_mod"
                mod_scan_dist = 1
                mod_scan_side = 1
                mod_other_true = None
                mod_k = None
        return

    # 7) Procurando outro número verdadeiro para deduzir mod
    if fase == "collect_mod":
        if ok and chute != anchor and mod_other_true is None:
            mod_other_true = chute
            mod_k = abs(chute - anchor)
            fase = "emit_mod"
        return


def _next_search_guess(used):
    """
    Próximo chute na busca binária.
    Tenta o meio do intervalo e, se já foi usado, procura perto.
    """
    global low, high

    if low > high:
        low, high = 1, 100000

    meio = _mid(low, high)

    if meio not in used:
        return meio

    for delta in range(1, 200):
        a = meio - delta
        b = meio + delta

        if low <= a <= high and a not in used:
            return a
        if low <= b <= high and b not in used:
            return b

    return meio


def _next_mod_guess(used):
    """
    Vai alternando:
      anchor+1, anchor-1, anchor+2, anchor-2, ...
    """
    global mod_scan_dist, mod_scan_side, anchor

    if anchor is None:
        return None

    while mod_scan_dist <= 100:
        cand = anchor + (mod_scan_side * mod_scan_dist)

        if mod_scan_side == 1:
            mod_scan_side = -1
        else:
            mod_scan_side = 1
            mod_scan_dist += 1

        if 1 <= cand <= 100000 and cand not in used:
            return cand

    return None


def _rule_to_emit():
    """Monta a regra final quando o algoritmo acha que descobriu."""
    if fase == "emit_int" and left_true is not None and right_true is not None:
        return ["int", left_true, right_true]

    if fase == "emit_pot" and pot_found is not None:
        return ["pot", pot_found, 0]

    if fase == "emit_mod" and mod_k is not None and anchor is not None:
        return ["mod", mod_k, anchor % mod_k]

    return None


def player(number_guesses, rule_guesses):
    """
    Função principal do jogo.
    Recebe:
      - number_guesses: histórico dos chutes de número
      - rule_guesses: histórico dos chutes de regra
    Retorna:
      - [NUMBER, n] ou [RULE, [tipo, p1, p2]]
    """
    global fase, pot_exp, pot_results, pot_found
    global mod_scan_dist, mod_scan_side, mod_other_true, mod_k
    global processed_number_count, processed_rule_count

    # Nova partida
    if not number_guesses and not rule_guesses:
        if processed_number_count != 0 or processed_rule_count != 0 or fase != "buscar" or anchor is not None:
            _reset()
        return [CHUTE_DE_NUMERO, 50_000]

    # Registra regras já tentadas
    _process_rules(rule_guesses)

    # Processa somente os novos resultados de número
    while processed_number_count < len(number_guesses):
        chute, direcao, ok = number_guesses[processed_number_count]
        _process_number_guess(chute, direcao, ok)
        processed_number_count += 1

    used = _used_numbers(number_guesses)

    # Decide a próxima ação
    while True:
        if fase == "buscar":
            return [CHUTE_DE_NUMERO, _next_search_guess(used)]

        if fase == "check_left":
            if anchor is None:
                fase = "buscar"
                continue

            cand = anchor - 1
            if cand >= 1 and cand not in used:
                return [CHUTE_DE_NUMERO, cand]

            fase = "check_right"
            continue

        if fase == "check_right":
            if anchor is None:
                fase = "buscar"
                continue

            cand = anchor + 1
            if cand <= 100000 and cand not in used:
                return [CHUTE_DE_NUMERO, cand]

            fase = "test_pot"
            pot_exp = 1
            pot_results = {}
            continue

        if fase == "expand_left":
            if left_true is None:
                fase = "expand_right"
                continue

            cand = left_true - 1
            if cand >= 1 and cand not in used:
                return [CHUTE_DE_NUMERO, cand]

            fase = "expand_right"
            continue

        if fase == "expand_right":
            if right_true is None:
                fase = "emit_int"
                continue

            cand = right_true + 1
            if cand <= 100000 and cand not in used:
                return [CHUTE_DE_NUMERO, cand]

            fase = "emit_int"
            continue

        if fase == "emit_int":
            regra = _rule_to_emit()
            if regra is not None and tuple(regra) not in tried_rules:
                tried_rules.add(tuple(regra))
                # Se errar, a próxima fase útil é testar potência.
                fase = "test_pot"
                pot_exp = 1
                pot_results = {}
                return [CHUTE_DE_REGRA, regra]

            fase = "test_pot"
            continue

        if fase == "test_pot":
            while pot_exp <= 10:
                cand = 2 ** pot_exp
                if cand not in used:
                    return [CHUTE_DE_NUMERO, cand]
                pot_exp += 1

            p = _infer_pot()
            if p is not None:
                pot_found = p
                fase = "emit_pot"
            else:
                fase = "collect_mod"
                mod_scan_dist = 1
                mod_scan_side = 1
                mod_other_true = None
                mod_k = None
            continue

        if fase == "emit_pot":
            regra = _rule_to_emit()
            if regra is not None and tuple(regra) not in tried_rules:
                tried_rules.add(tuple(regra))
                # Se errar, parte para procurar outro True e deduzir mod.
                fase = "collect_mod"
                mod_scan_dist = 1
                mod_scan_side = 1
                mod_other_true = None
                mod_k = None
                return [CHUTE_DE_REGRA, regra]

            fase = "collect_mod"
            continue

        if fase == "collect_mod":
            if anchor is None:
                fase = "buscar"
                continue

            cand = _next_mod_guess(used)
            if cand is not None:
                return [CHUTE_DE_NUMERO, cand]

            fase = "buscar"
            continue

        if fase == "emit_mod":
            regra = _rule_to_emit()
            if regra is not None and tuple(regra) not in tried_rules:
                tried_rules.add(tuple(regra))
                fase = "buscar"
                return [CHUTE_DE_REGRA, regra]

            fase = "buscar"
            continue

        # Segurança geral
        fase = "buscar"
        return [CHUTE_DE_NUMERO, _next_search_guess(used)]