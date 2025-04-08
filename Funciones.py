import random
import re

from Const import(gramatica)


# ---------------- Decodificación ----------------
def decodificacion(genotipo, gramatica, simbolo_inicial="<E>"):
    fenotipo = simbolo_inicial
    codon_index = 0
    max_codons = len(genotipo)
    while any(simbolo in fenotipo for simbolo in gramatica):
        replaced = False
        for simbolo in gramatica:
            while simbolo in fenotipo:
                if codon_index >= max_codons:
                    return fenotipo
                opciones = gramatica[simbolo]
                eleccion = genotipo[codon_index] % len(opciones)
                produccion = opciones[eleccion]
                fenotipo = fenotipo.replace(simbolo, produccion, 1)
                codon_index += 1
                replaced = True
        if not replaced:
            break
    return fenotipo

# ---------------- Evaluación lógica ----------------
def evaluar_expresion(expr, variables):
    if any(nt in expr for nt in ["<E>", "<T>", "<F>", "<num>"]):
        return None
    for var, val in variables.items():
        expr = re.sub(rf'\b{var}\b', str(val), expr)
    expr = re.sub(r'\bAND\b', ' and ', expr)
    expr = re.sub(r'\bOR\b', ' or ', expr)
    expr = re.sub(r'\bXOR\b', ' ^ ', expr)
    expr = re.sub(r'\bNOT\b', ' not ', expr)
    expr = " ".join(expr.split())
    try:
        return eval(expr)
    except:
        return None


def fitness(genotipo, gramatica,tabla):
    expr = decodificacion(genotipo, gramatica)
    score = 0
    for row in tabla:
        inputs = {k: row[k] for k in ["A", "B", "C"]}
        resultado = evaluar_expresion(expr, inputs)
        if resultado is not None and resultado == row["target"]:
            score += 1
    return score, expr

# ---------------- Operadores genéticos ----------------
def crear_individuos(length, codon_max=256):
    return [random.randint(0, codon_max - 1) for _ in range(length)]

def mutacion(individual, codon_max=256, tasa_mutacion=0.1):
    return [
        gene if random.random() > tasa_mutacion else random.randint(0, codon_max - 1)
        for gene in individual
    ]

def cruce(p1, p2):
    if len(p1) < 2:
        return p1[:], p2[:]
    point = random.randint(1, len(p1) - 1)
    return p1[:point] + p2[point:], p2[:point] + p1[point:]

def Selecion_Torneo(population, k=3):
    competitors = random.sample(population, k)
    return max(competitors, key=lambda ind: ind["fitness"])
