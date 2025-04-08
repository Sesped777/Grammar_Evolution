import random
import re

# ---------------- Gramática ----------------
gramatica = {
    "<E>": ["<E> OR <T>", "<E> XOR <T>", "<T>"],
    "<T>": ["<T> AND <F>", "<F>"],
    "<F>": ["NOT <F>", "(<E>)", "<num>"],
    "<num>": ["A", "B", "C"]
}

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

# ---------------- Fitness ----------------
tabla_verdad_sum= [
    {"A": False, "B": False, "C": False, "target": False},
    {"A": False, "B": False, "C": True,  "target": True},
    {"A": False, "B": True,  "C": False, "target": True},
    {"A": False, "B": True,  "C": True,  "target": False},
    {"A": True,  "B": False, "C": False, "target": True},
    {"A": True,  "B": False, "C": True,  "target": False},
    {"A": True,  "B": True,  "C": False, "target": False},
    {"A": True,  "B": True,  "C": True,  "target": True},
]

tabla_verdad_Prueba = [
    {"A": False, "B": False, "C": False, "target": False},
    {"A": False, "B": False, "C": True,  "target": True},
    {"A": False, "B": True,  "C": False, "target": True},
    {"A": False, "B": True,  "C": True,  "target": False},
    {"A": True,  "B": False, "C": False, "target": True},
    {"A": True,  "B": False, "C": True,  "target": False},
    {"A": True,  "B": True,  "C": False, "target": False},
    {"A": True,  "B": True,  "C": True,  "target": True},
]
tabla_verdad_carry = [
    {"A": False, "B": False, "C": False, "target": False},
    {"A": False, "B": False, "C": True,  "target": False},
    {"A": False, "B": True,  "C": False, "target": False},
    {"A": False, "B": True,  "C": True,  "target": True},
    {"A": True,  "B": False, "C": False, "target": False},
    {"A": True,  "B": False, "C": True,  "target": True},
    {"A": True,  "B": True,  "C": False, "target": True},
    {"A": True,  "B": True,  "C": True,  "target": True},   
]

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


def Selecion_Torneo_dual(population, k=3):
    competitors = random.sample(population, k)
    return max(competitors, key=lambda ind: ind["fitness_total"])


def fitness_dual(genotipo, gramatica):
    expr_sum = decodificacion(genotipo, gramatica)
    expr_carry = expr_sum  # misma expresión, se evalúa en ambos contextos

    score_sum = 0
    score_carry = 0

    for row_sum, row_carry in zip(tabla_verdad_sum, tabla_verdad_carry):
        inputs = {k: row_sum[k] for k in ["A", "B", "C"]}

        out_sum = evaluar_expresion(expr_sum, inputs)
        out_carry = evaluar_expresion(expr_carry, inputs)

        if out_sum is not None and out_sum == row_sum["target"]:
            score_sum += 1
        if out_carry is not None and out_carry == row_carry["target"]:
            score_carry += 1

    return (score_sum, score_carry), expr_sum  # usamos la misma expresión para ambos

