"""

if fase == 2:
     
        Antes eu tinha tentado pra mudar de fasecom só dois Oks.
        Deu errado, melhor 3 acertos contínuos, pra dar certeza
      
        if (t + 1 in trues and t + 2 in trues) or (t - 1 in trues and t - 2 in trues):
            a = min(trues)
            b = max(trues)
            return [CHUTE_DE_REGRA, ["int", a, b]]
        else:
            fase = 3


#pot
for p in range(2, 11):
            ok = True
            for n in trues:
                raiz = round(n ** (1/p))
                if raiz ** p != n:
                    ok = False
                    break
            if ok and len(trues) >= 2:
                return [CHUTE_DE_REGRA, ["pot", p, 0]]
            



"""