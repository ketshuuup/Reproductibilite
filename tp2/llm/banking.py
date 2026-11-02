import os
from decimal import Decimal, getcontext


def solve():
  # Définition d'une haute précision (100 décimales) pour éviter les erreurs d'arrondi
  getcontext().prec = 100

  # Calcul de e (exponentielle de 1) avec une haute précision
  e = Decimal(1).exp()

  v = e
  n = 50

  # Simulation année par année
  for year in range(1, n + 1):
    v = (v - Decimal(1)) * Decimal(year)

  # Frais de retrait final de 1 euro
  final_amount = v - Decimal(1)

  # Gestion du dossier de sortie via la variable d'environnement OUT_DIR
  out_dir = os.environ.get("OUT_DIR", ".")
  os.makedirs(out_dir, exist_ok=True)

  output_path = os.path.join(out_dir, "answer_banking_llm.txt")

  # Écriture du résultat
  with open(output_path, "w", encoding="utf-8") as f:
    f.write(f"{final_amount}\n")

  print(f"Résultat calculé et écrit dans {output_path}")


if __name__ == "__main__":
  solve()

