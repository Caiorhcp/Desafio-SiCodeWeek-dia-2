"""SI Code Week 2026 · Desafio 02 · Torneio de Algoritmos

Escreva a função despachar() abaixo. Não mude o nome nem os parâmetros:
os testes de correção chamam a função exatamente assim.

Regras completas: página do Desafio 02 no sistema da SI Code Week.
Python 3.12, só com a biblioteca padrão.
"""
SIMBOLOS = {"+": "CHEGA", "-": "CANCELA", ">": "SAI", "<": "DESFAZ"}


def despachar(log: list[str]) -> list[str]:
    """Recebe as linhas do log de despacho e devolve os códigos dos pedidos
    entregues, na ordem em que saíram.

    >>> despachar(["CHEGA P1", "CHEGA P2", "SAI"])
    ['P1']
    """
    nxt = [0]
    prv = [0]
    codigos = [""]
    na_fila = [False]

    onde = {}      
    entregues = []
    desfazer = []  

    for bruto in log:
        linha = bruto.split("#", 1)[0].strip()
        if not linha:
            continue

        cmd = SIMBOLOS.get(linha[0])
        if cmd is not None:
            arg = linha[1:].strip().upper()
        else:
            partes = linha.upper().split()
            cmd = partes[0]
            arg = partes[1] if len(partes) > 1 else ""

        if cmd == "CHEGA":
            if not arg or arg in onde:
                continue
            i = len(nxt)
            fim = prv[0]
            nxt.append(0)
            prv.append(fim)
            codigos.append(arg)
            na_fila.append(True)
            nxt[fim] = i
            prv[0] = i
            onde[arg] = i
            desfazer.append(("C", i))

        elif cmd == "SAI":
            i = nxt[0]
            if i == 0:
                continue
            nxt[prv[i]] = nxt[i]
            prv[nxt[i]] = prv[i]
            na_fila[i] = False
            entregues.append(codigos[i])
            desfazer.append(("S", i))

        elif cmd == "CANCELA":
            i = onde.get(arg)
            if i is None or not na_fila[i]:
                continue
            nxt[prv[i]] = nxt[i]
            prv[nxt[i]] = prv[i]
            na_fila[i] = False
            desfazer.append(("X", i))

        elif cmd == "DESFAZ":
            if not desfazer:
                continue
            op, i = desfazer.pop()
            if op == "C":
                nxt[prv[i]] = nxt[i]
                prv[nxt[i]] = prv[i]
                na_fila[i] = False
                del onde[codigos[i]]
            else:
                nxt[prv[i]] = i
                prv[nxt[i]] = i
                na_fila[i] = True
                if op == "S":
                    entregues.pop()

    return entregues


if __name__ == "__main__":
    assert despachar(["CHEGA P1", "CHEGA P2", "CHEGA P3", "CANCELA P2",
                      "SAI", "DESFAZ", "DESFAZ", "SAI", "SAI"]) == ["P1", "P2"]
    assert despachar(["SAI", "DESFAZ", "CANCELA X", "chega a", "+A", ">"]) == ["A"]
    assert despachar(["+P1", "- p1", "<", ">"]) == ["P1"]
    assert despachar(["CHEGA P1", "DESFAZ", "CHEGA P1", "SAI"]) == ["P1"]
    print("ok")
