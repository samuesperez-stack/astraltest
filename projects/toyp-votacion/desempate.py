from collections import Counter

def clave(notas):
    if not notas or any(type(n) is not int or not 1 <= n <= 10 for n in notas):
        raise ValueError('Las calificaciones deben ser enteros entre 1 y 10')
    c = Counter(notas)
    return (sum(notas), *(c[n] for n in range(10, 0, -1)))

def clasificar(candidatos):
    grupos = {}
    for candidato, notas in candidatos.items():
        grupos.setdefault(clave(notas), []).append(candidato)
    return [grupos[k] for k in sorted(grupos, reverse=True)]
