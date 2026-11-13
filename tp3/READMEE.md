# Reproductibilité – labs 1 à 3

Question étudiée : **combien de fois `(x+y)+z == x+(y+z)` ?** (et d'autres propriétés arithmétiques), puis pourquoi la réponse varie d'un programme et d'un environnement à l'autre.

Dépôt : https://github.com/ketshuuup/Reproductibilite

## 1. Architecture du dépôt

| Chemin | Contenu |
|---|---|
| `tp1/` | Lab 1 : programmes C d'origine (associativité, banking) |
| `tp2/` | Lab 2 : Docker, GitHub Actions, programmes générés par un LLM (`tp2/llm/`) |
| `tp3/fm/experiment.uvl` | Modèle de variabilité (UVL) : 4000 configurations |
| `tp3/configs/` | `p1/p2/p3.csvconf` (mes trois programmes comme configurations) et `sample.csv` (échantillon) |
| `tp3/sample.py` | Script d'échantillonnage du cours (flamapy) |
| `tp3/templates/assoc.c.jinja` | Template C : type et propriété sont des trous |
| `tp3/assoc_py.py` | Programme Python configurable en ligne de commande |
| `tp3/run_sample.py` | Dérive, compile et exécute chaque configuration ; écrit un CSV |
| `tp3/causal.py` | Expériences causales (un seul facteur change) → `results/causal.csv` |
| `tp3/results/` | `results_ci*.csv` (GitHub Actions), `causal.csv`, `results_colab.csv` (exécution complémentaire sur Google Colab) |
| `tp3/analysis.ipynb` | Notebook d'analyse (lit les CSV, ne produit pas de données) |
| `tp3/matrice.md` | Matrice de comparaison des trois programmes et liste des facteurs |
| `tp3/part3/`, `tp3/part33/` | Expériences des sections 3.2 (CLI) et 3.3 (templates) |
| `.github/workflows/tp3.yml` | Workflow : échantillonne, exécute, enregistre le CSV |

## 2. Reproduire les résultats

Prérequis : Linux, `gcc`, Python ≥ 3.11.

```bash
git clone https://github.com/ketshuuup/Reproductibilite.git
cd Reproductibilite
python3 -m venv .venv && source .venv/bin/activate
pip install -r tp3/requirements.txt pandas matplotlib scikit-learn jupyterlab
cd tp3
```

**Échantillon** (mêmes commande et graine → même fichier, vérifié par `diff` et par le job `sample` du workflow) :

```bash
python sample.py fm/experiment.uvl --size 100 --seed 1 --include configs/p*.csvconf -o configs/sample.csv
```

103 configurations : mes 3 programmes + 100 tirées au hasard parmi 4000 (2,5 % de l'espace).

**Exécution locale** (5 exécutions par configuration) : `python run_sample.py --runs 5` → `results/results_<machine>.csv`.

**Exécution automatique** : le workflow `tp3.yml` se déclenche à chaque push dans `tp3/`. Il échantillonne, puis exécute l'échantillon dans une matrice de 4 jobs (**Python 3.10 / 3.14 × gcc 12 / 14**), fusionne les CSV dans `results/results_ci.csv` et les commite. Chaque exécution laisse aussi `results_ci_attemptN.csv`, ce qui permet de comparer deux exécutions du même commit.

**Expériences causales** : `python causal.py 1000000` → `results/causal.csv`.

**Notebook** : `jupyter nbconvert --to notebook --execute --inplace analysis.ipynb` (équivalent de *Restart Kernel and Run All*).

Chaque ligne des CSV de résultats contient les facteurs, la graine réellement utilisée (`seed_used`), la machine, le système, la version de Python et celle de gcc.

## 3. Ce qui varie : les facteurs

Facteurs du modèle : langage (C, Python), type (`float`, `double`), générateur (`rand()`, `random()`, entier divisé par 2³¹-1), intervalle des tirages, nombre de répétitions, graine, propriété testée, option d'optimisation (`-O0`, `-O2`, `-O2 -ffast-math`). Facteurs d'environnement (matrice du workflow) : version de gcc et de Python.

**L'architecture CPU (x86_64 / ARM) a été identifiée mais volontairement retirée du modèle : elle n'a pas été testée**, on ne peut donc rien en conclure.

## 4. Principaux résultats

Expériences contrôlées (un seul facteur change), 1 000 000 de répétitions, graine fixée, mesurées pendant le lab :

| Facteur qui change | Valeur A | Valeur B |
|---|---|---|
| Option `-ffast-math` (C, `float`, [0, 1]) | 74,59 % | **100 %** |
| Signe des nombres : [0, 1] / [-1, 1] (C, `float`) | 74,6 % | 93,0 % |
| Générateur (Python, [0, 1]) : `random()` / entier÷(2³¹-1) | 82,8 % | 74,5 % |
| Type sur [-1e15, 1e15] : `float` / `double` | ≈ 92,1 % | ≈ 93,0 % |
| Propriété (C, [0, 1]) : `x*(1/x)==1` / assoc. `+` / assoc. `*` / distributivité | 84,7 / 74,6 | 65,1 / 64,7 |

Sans effet constaté : `-O0` contre `-O2`, ordre des tirages, `float` contre `double` sur [0, 1], [-1, 1] et [-1000, 1000]. L'effet du type dépend donc de l'intervalle (interaction). L'explication par la structure binaire des valeurs de `random()` reste une **hypothèse non démontrée**. L'analyse complète (effets, arbre de décision, stabilité entre exécutions et entre environnements, recommandations) est dans `tp3/analysis.ipynb`.

**Définition de « même résultat »** : identique au chiffre près si la graine est fixée et le même environnement ; sinon compatible dans la marge statistique (≈ ±0,05 point à 10⁶ répétitions, ≈ ±1,5 point à 10³).

**Recommandations** : ne pas utiliser `-ffast-math` ; fixer la graine et la consigner ; au moins 10⁵ à 10⁶ répétitions ; documenter l'intervalle, le générateur et le type.

### Réponses des labs 1 et 2

- Lab 1, associativité : 746552 sur 1 000 000 essais, soit 74,66 % (C, `float`, `rand()/RAND_MAX`, `srand(42)`, [0, 1]).
- Lab 2, associativité (Gemini, Python) : ≈ 93 %, car l'intervalle [-1e15, 1e15] contient des nombres négatifs.
- Banking, lab 1 : -4,39e48, faux. `exp(1.0)` en `double` porte une erreur d'environ 1e-16, amplifiée par 50! ≈ 3e64. La première tentative de Gemini (`Decimal(str(math.e))`) avait le même défaut ; la version corrigée (`Decimal(1).exp()` à 100 chiffres) donne ≈ 0,0199921658 €.

## 5. Limites

- L'architecture CPU n'est pas testée ; un seul compilateur (gcc) ; un seul système d'exploitation.
- Un échantillon de 100 configurations sur 4000 ne couvre pas toutes les valeurs de tous les facteurs.
- `results_colab.csv` vient d'un autre environnement (gcc 13.3, Python 3.13) et complète les résultats du workflow sans les remplacer.

## 6. Usage de l'IA

| Outil | Utilisé pour | Ce que j'ai vérifié |
|---|---|---|
| **Gemini** (modèle et version : *à compléter, affichés dans l'interface*), via gemini.google.com | Générer les programmes du lab 2 (Python, associativité et banking) et du lab 3 (C, associativité). Prompts et réponses : `tp2/llm/`, `tp3/LLM_associativity_C.md` | J'ai exécuté chaque programme. La 1re version du banking était fausse (e tronqué) : documentée et corrigée. Le C annonçait « 75 à 85 % » sans l'avoir exécuté : non confirmé |
| **Claude** (Anthropic), via claude.ai | M'aider à comprendre l'énoncé, écrire les scripts (`run_sample.py`, `causal.py`), le workflow, le notebook et ce README ; me guider dans l'analyse | J'ai exécuté les scripts et collé les sorties réelles. Deux affirmations initiales de l'assistant ont été contredites par mes mesures et corrigées : l'ordre des tirages n'a pas d'effet, et le type `float`/`double` compte sur [-1e15, 1e15]. Le workflow n'a fonctionné qu'après correction d'un fichier mal copié |

Ce que j'ai écrit ou décidé moi-même : le choix des facteurs retenus, le retrait de l'architecture, la taille de l'échantillon, l'interprétation finale des résultats. *(À adapter à ce qui est vrai pour toi.)*
