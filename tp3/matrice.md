# TP3 – Part 1 : matrice de comparaison et facteurs de variabilité

Question étudiée : combien de fois `(x+y)+z == x+(y+z)` ?

## 1. Les trois programmes

| Programme | Langage | Répétitions | Type | Générateur | Graine | Intervalle | Sortie | Résultat |
|---|---|---|---|---|---|---|---|---|
| **P1** : le mien (TP1) | C | 1 000 000 | `float` | `rand()` (libc) | `srand(42)` | [0, 1] (`rand()/RAND_MAX`) | un compte brut | 746552, soit 74,6552 % |
| **P2** : Gemini (TP2, version A) | Python 3.11 | 1 000 000 | `float` (64 bits) | `random` (Mersenne Twister) | aucune | `uniform(-1e15, 1e15)` | pourcentage | 93,04 % |
| **P2'** : Gemini (TP2, version B) | Python 3 | 1 000 000 | `float` (64 bits) | `random` (Mersenne Twister) | `seed(42)` | `uniform(-1000, 1000)` | pourcentage | non exécuté |
| **P3** : Gemini (TP3, nouveau) | C | 10 000 000 | `float` | `rand()` (libc) | `time(NULL)` | [-1000, 1000] (`rand()/RAND_MAX*2000-1000`) | pourcentage | à compléter : ______ % |

Remarques :

- Mon programme TP1 écrit un **nombre** (746552) et non un pourcentage, alors que l'énoncé demande un pourcentage.
- P3 est dans le même langage et le même type que P1 : les écarts viennent donc des choix de code.
- P3 annonce « 75 % à 85 % » sans l'avoir exécuté : affirmation à vérifier.

### Banking

| Programme | Langage | Type | Valeur de e | Résultat |
|---|---|---|---|---|
| Le mien (TP1) | C | `double` | `exp(1.0)` | -4,39e48 (faux : bruit d'arrondi) |
| Gemini, 1re tentative | Python | `Decimal` | `Decimal(str(math.e))` (~16 chiffres) | bruit amplifié par 50! |
| Gemini, version corrigée | Python | `Decimal`, 100 chiffres | `Decimal(1).exp()` | 0,0199921658366679... |

L'erreur initiale de ~1e-16 sur e est multipliée par 50! ≈ 3e64, ce qui donne une erreur de ~1e48 : seule une valeur de e à plus de ~70 chiffres donne un résultat fiable.

## 2. Ce que P3 apprend que P1 et P2 n'apprennent pas

P1 et P2 diffèrent par plusieurs choses à la fois (langage, type, intervalle, graine, générateur) : impossible d'isoler la cause d'un écart. P3 a le même langage et le même type que P1 : seuls changent le nombre de répétitions, la graine, l'intervalle et la façon de normaliser `rand()`. Cela permet d'attribuer les écarts à ces choix de programmation, et non au langage. P3 révèle aussi de nouveaux facteurs : un intervalle symétrique autour de 0 (des nombres de signes opposés s'annulent) et la taille de l'échantillon.

## 3. Liste des facteurs de variabilité (à compléter)

| # | Facteur | Valeurs observées ou possibles |
|---|---|---|
| 1 | Nombre de répétitions | 100 à 10 000 000 |
| 2 | Graine | fixe (42), `time(NULL)`, aucune |
| 3 | Générateur aléatoire | `rand()`, Mersenne Twister, autres |
| 4 | Implémentation de `rand()` / valeur de `RAND_MAX` | glibc 2³¹-1, MSVC 32767 |
| 5 | Type des nombres | `float` (32 bits), `double` (64 bits) |
| 6 | Intervalle / distribution | [0,1], [-1000,1000], [-1e15,1e15], normale... |
| 7 | Normalisation de `rand()` | `/RAND_MAX`, `(float)RAND_MAX` = 2³¹ arrondi |
| 8 | Ordre des tirages | y, x, z (P1) ou x, y, z |
| 9 | Propriété testée | assoc. de `+`, assoc. de `*`, distributivité, `x*(1/x)==1` |
| 10 | Langage | C, Python |
| 11 | Optimisations du compilateur | `-O0`, `-O2`, `-ffast-math` |
| 12 | Modèle d'évaluation flottant (SSE, x87) | selon cible |
| 13 | FMA (multiplication-addition fusionnée) | selon compilateur et CPU |
| 14 | Version du compilateur ou de l'interpréteur | gcc 12 / 15, Python 3.10 / 3.14 |
| 15 | Bibliothèque mathématique (`exp`) | version de la libm |
| 16 | Architecture CPU | x86_64, ARM |
| 17 | Format de sortie | compte, pourcentage, `%d`, `%f`, `%.2f` |
| 18 | Précision de e (banking) | `double`, `Decimal` 16 ou 100 chiffres |

Cette liste n'est jamais terminée : chaque expérience du TP3 pourra y ajouter un facteur.

## 4. Expériences de la Part 1 (à compléter après exécution)

| Expérience | Commande | Résultat |
|---|---|---|
| P1 en `-O0` | `gcc -O0 assoc_tp1.c` | ______ |
| P1 en `-O2` | `gcc -O2 assoc_tp1.c` | ______ |
| P1 en `-O2 -ffast-math` | `gcc -O2 -ffast-math assoc_tp1.c` | ______ |
| P1 avec `double` | `sed 's/float/double/g'` | ______ |
| P1 avec intervalle [-1000, 1000] | voir `assoc_tp1_sym.c` | ______ |
| P3, 3 exécutions | `./gemini_assoc` | ______ / ______ / ______ |

## 5. Déclaration d'usage de l'IA

- Outil : Gemini (modèle et version : ______), via gemini.google.com.
- Utilisé pour : générer les programmes P2, P2' et P3 (prompts et réponses complètes dans `tp2/llm/` et `tp3/LLM_associativity_C.md`).
- Vérifié : exécution des programmes dans Docker ; correction du banking après identification du bruit d'arrondi sur e.
