from Funciones import (
    fitness, crear_individuos, mutacion,
    cruce, Selecion_Torneo,
)
from Const import (gramatica, tabla_verdad_carry, tabla_verdad_Prueba, tabla_verdad_sum)

POP_SIZE = 100
GENOTYPE_LENGTH = 20
GENERATIONS = 100000

# Inicializar población
population = [crear_individuos(GENOTYPE_LENGTH) for _ in range(POP_SIZE)]

for gen in range(GENERATIONS):
    # Evaluar población
    evaluated = []
    for ind in population:
        fit, expr = fitness(ind, gramatica,tabla_verdad_Prueba)
        evaluated.append({"genotype": ind, "fitness": fit, "expr": expr})

    best = max(evaluated, key=lambda ind: ind["fitness"])
    print(f"Gen {gen:02d} | Mejor fitness: {best['fitness']} | Expr: {best['expr']} | Gen:{best['genotype']}")

    if best["fitness"] == 8:
        print(" ¡Solución perfecta encontrada!")
        break

    # Crear nueva población
    nueva_poblacion = []
    while len(nueva_poblacion) < POP_SIZE:
        p1 = Selecion_Torneo(evaluated)
        p2 = Selecion_Torneo(evaluated)
        hijo1, hijo2 = cruce(p1["genotype"], p2["genotype"])
        hijo1 = mutacion(hijo1)
        hijo2 = mutacion(hijo2)
        nueva_poblacion.append(hijo1)
        if len(nueva_poblacion) < POP_SIZE:
            nueva_poblacion.append(hijo2)
    population = nueva_poblacion


