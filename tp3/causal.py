"""Expériences causales : on ne change qu'UN facteur à la fois. Écrit results/causal.csv."""
import csv, subprocess, sys
from pathlib import Path
from jinja2 import Template

reps = int(sys.argv[1]) if len(sys.argv) > 1 else 1000000
seeds = [1, 2, 3, 4, 5]
template = Template(Path("templates/assoc.c.jinja").read_text())
Path("build").mkdir(exist_ok=True)
Path("results").mkdir(exist_ok=True)
ADD = ("(x + y) + z", "x + (y + z)")

def build_c(name, ctype, flags):
    base = f"build/causal_{name}"
    Path(base + ".c").write_text(template.render(ctype=ctype, lhs=ADD[0], rhs=ADD[1]))
    subprocess.run(["gcc", *flags, "-o", base, base + ".c"], check=True)
    return [base]

def run(exe, seed, low, high):
    args = [f"--repetitions={reps}", f"--seed={seed}", f"--low={low}", f"--high={high}"]
    return float(subprocess.run(exe + args, capture_output=True, text=True, check=True).stdout)

rows = []
def record(experiment, variant, exe, low, high):
    for s in seeds:
        rows.append({"experiment": experiment, "variant": variant, "seed": s,
                     "percentage": run(exe, s, low, high)})
    print(experiment, variant, "ok")

# 1. Option de compilation : seule l'option -ffast-math change
for name, flags in [("-O2", ["-O2"]), ("-O2 -ffast-math", ["-O2", "-ffast-math"])]:
    record("compiler flag (C, float, [0,1])", name, build_c("flag" + str(len(rows)), "float", flags), 0, 1)

# 2. Générateur : seule la fabrication du nombre aléatoire change (Python)
for cstyle, name in [(0, "random() natif"), (1, "entier/(2^31-1) comme rand()/RAND_MAX")]:
    exe = [sys.executable, "assoc_py.py", f"--cstyle={cstyle}"]
    record("generator (Python, [0,1])", name, exe, 0, 1)

# 3. Type : seul float/double change, sur un intervalle énorme
for ctype in ["float", "double"]:
    record("type (C, [-1e15,1e15])", ctype, build_c("type_" + ctype, ctype, ["-O2"]), "-1e15", "1e15")

# 4. Intervalle : seul le signe des nombres change
for name, lo, hi in [("[0,1]", 0, 1), ("[-1,1]", -1, 1)]:
    record("interval (C, float)", name, build_c("iv" + str(len(rows)), "float", ["-O2"]), lo, hi)

with open("results/causal.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["experiment", "variant", "seed", "percentage"])
    w.writeheader(); w.writerows(rows)
print("écrit results/causal.csv", len(rows), "lignes")

