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

# ---------------- Gramática ----------------
gramatica = {
    "<E>": ["<E> OR <T>", "<E> XOR <T>", "<T>"],
    "<T>": ["<T> AND <F>", "<F>"],
    "<F>": ["NOT <F>", "(<E>)", "<num>"],
    "<num>": ["A", "B", "C"]
}