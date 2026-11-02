import os
import random

def test_associativity(num_tests=1000000):
    failures = 0
    successes = 0
    
    # Test avec des nombres flottants sur une large plage de magnitudes
    for _ in range(num_tests):
        x = random.uniform(-1e15, 1e15)
        y = random.uniform(-1e15, 1e15)
        z = random.uniform(-1e15, 1e15)
        
        left = (x + y) + z
        right = x + (y + z)
        
        if left == right:
            successes += 1
        else:
            failures += 1
            
    return successes, failures

def main():
    out_dir = os.environ.get("OUT_DIR", ".")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "answer_associativity_llm.txt")
    
    num_tests = 1000000
    successes, failures = test_associativity(num_tests)
    
    output = f"""Analyse de l'associativité de l'addition : (x + y) + z == x + (y + z)

1. En mathématiques théoriques (nombres réels exacts) :
L'addition est TOUJOURS associative. L'égalité est vraie dans 100 % des cas.

2. En informatique (nombres à virgule flottante IEEE 754 / type `float` de Python) :
L'addition n'est PAS toujours associative en raison des erreurs d'arrondi liées à la précision finie.

3. Résultats du test empirique sur {num_tests} échantillons aléatoires (floats Python) :
- Égalités vérifiées : {successes} ({successes/num_tests*100:.4f}%)
- Échecs (non-associativité due aux arrondis) : {failures} ({failures/num_tests*100:.4f}%)
"""
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)
    
    print(f"Résultat écrit avec succès dans {out_path}")

if __name__ == "__main__":
    main()
