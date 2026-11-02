 Écris un programme en python qui répond à ce problème :


The banking problem: do the same."My banker proposed this investment to me: you give me e ≈ 2.71828… The following year,

I take 1 euro as a fee and multiply by 1. The next year, I take 1 euro as a fee and

multiply by 2. The next year, I take 1 euro as a fee and multiply by 3. […] After n years,

I take 1 euro as a fee and multiply by n. To retrieve my money, there is a 1 euro fee.

In 50 years, for my retirement, how much money will I have?"

Write a program that answers this question, write down your choices, and check whether your

result is reproducible.


Contraintes :

    Le programme doit s'exécuter sans interaction, dans un conteneur Docker.
    Il écrit son résultat dans le fichier answer_associativity_llm.txt, 

dans le dossier donné par la variable d'environnement OUT_DIR

(par défaut le dossier courant).

    Donne-moi aussi le Dockerfile et un script run.sh pour le lancer.
    Explique brièvement tes choix (nombre de répétitions, type des nombres, 

générateur aléatoire).

Voici une solution complète en Python, accompagnée de son Dockerfile et d'un script run.sh, répondant à toutes vos contraintes.
1. Le programme Python (solution.py)

Ce script modélise année par année l'investissement proposé. Le module decimal est utilisé avec une haute précision pour éviter les erreurs d'arrondi inhérentes aux nombres flottants (float) standard lors des multiplications successives par des grands nombres.
Python

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

  output_path = os.path.join(out_dir, "answer_associativity_llm.txt")

  # Écriture du résultat
  with open(output_path, "w", encoding="utf-8") as f:
    f.write(f"{final_amount}\n")

  print(f"Résultat calculé et écrit dans {output_path}")


if __name__ == "__main__":
  solve()

2. Le Dockerfile
Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY solution.py .

CMD ["python", "solution.py"]

3. Le script de lancement (run.sh)

Ce script construit l'image Docker et exécute le conteneur en montant le dossier courant pour récupérer directement le fichier de sortie.
Bash

#!/bin/bash
set -e

# Construction de l'image Docker
docker build -t banking-problem .

# Exécution du conteneur en liant le dossier courant à /output
docker run --rm -v "$(pwd)":/output -e OUT_DIR="/output" banking-problem

(N'oubliez pas de rendre le script exécutable avec chmod +x run.sh avant de le lancer).
4. Explication des choix

    Nombre de répétitions (n=50) : Défini par l'énoncé du problème pour représenter la durée de l'investissement jusqu'à la retraite.

    Type des nombres (Decimal vs float) : L'utilisation de float standard en Python provoque des pertes de précision significatives sur 50 itérations en raison de la croissance exponentielle des facteurs de multiplication (le terme final implique 50!≈3.04×1064). Le module decimal avec 100 chiffres de précision garantit un résultat exact et sans dérive numérique.

    Générateur aléatoire : Aucun générateur aléatoire n'est utilisé, car le problème est entièrement déterministe. Le calcul est par conséquent strictement reproductible à chaque exécution.


