# TP1 — Reproductibilité

Deux petits programmes C qui illustrent les problèmes de l'arithmétique flottante.
Chaque programme écrit sa réponse dans un fichier texte.

## Prérequis

- `gcc` (testé avec GCC 13.3.0, Ubuntu 24.04)
- `make` (optionnel)
- la bibliothèque mathématique (`-lm`)

## Exécution

Avec make :

```bash
make run
```

Ou à la main :

```bash
gcc -O0 -Wall -o associativity associativity.c
gcc -O0 -Wall -o banking banking.c -lm
./associativity
./banking
```

Nettoyer : `make clean`.

## Résultats attendus

| Fichier | Contenu attendu |
|---|---|
| `answer_associativity.txt` | `746552` |
| `answer_banking.txt` | `-4396803930182068517325088235103664583272782888960.000000` |

(Obtenus sur Linux x86-64, GCC 13.3.0, `-O0`.)

### « Même résultat » : définition

- **exo1** : le programme utilise une graine fixe (`SEED = 42`) et un nombre
  d'essais fixe (`1000000`). Le résultat doit être **exactement identique** (`746552`)
  sur une même plateforme (même compilateur, même `libc`). La fonction `rand()`
  dépend de l'implémentation de la `libc` : avec une autre `libc` (macOS, Windows/MSVC, musl),
  la valeur peut différer. Dans ce cas, l'ordre de grandeur attendu est environ 75 % (≈ 0,75 × 10⁶).
- **exo2** : calcul déterministe, la valeur doit être identique à celle ci-dessus.
  Une légère différence sur les derniers chiffres peut venir d'un autre compilateur
  ou d'options d'optimisation (`-ffast-math`, `-O3`, FMA...) ; le signe négatif et
  l'ordre de grandeur (~ −4,4 × 10⁴⁸) doivent rester les mêmes.

## Explications

### 1. Associativité des flottants

En mathématiques, `(x+y)+z = x+(y+z)`. En `float` (32 bits), chaque addition arrondit
le résultat, donc l'ordre des opérations compte. Le programme tire 3 nombres
aléatoires dans [0,1] et compte combien de fois l'égalité reste vraie : environ 75 % des
cas ici, donc **environ 25 % des cas violent l'associativité**.

Notes :
- La graine fixe rend l'expérience reproductible. L'original utilisait `srand(time(NULL))`,
  qui donne un résultat différent à chaque exécution.
- La boucle d'origine allait de 1 à 1000001 (soit 1 000 001 essais) ; elle a été
  ramenée à exactement 1 000 000.

### 2. Le calcul « bancaire »

Le programme calcule la suite

```
u_0 = e - 1
u_i = i * u_{i-1} - 1      pour i = 1..50
```

Mathématiquement, `u_n = n! * (e - sum_{k=0..n} 1/k!)`... et cette suite tend vers **0**
(elle vaut environ `1/(n+1)`). Mais à chaque étape l'erreur d'arrondi initiale
(≈ 10⁻¹⁶ sur `e - 1`) est **multipliée par i**, donc après 50 itérations elle est amplifiée
d'un facteur proche de `50!` (≈ 3 × 10⁶⁴). Le résultat final n'a plus aucun rapport
avec la valeur exacte : c'est un exemple d'algorithme **numériquement instable**.
Passer en `float` ou en `long double` ne change que le moment où le résultat diverge.

## Fichiers

```
exo1.c   # problème 1
exo2.c         # problème 2
Makefile          # compilation et exécution
README.md         # ce fichier
```

