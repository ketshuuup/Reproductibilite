import csv, itertools, json, subprocess, sys
from collections import defaultdict

subprocess.run(["gcc", "-O2", "-o", "assoc_p1", "assoc_p1.c"], check=True)
subprocess.run(["gcc", "-O2", "-o", "assoc_p3", "assoc_p3.c"], check=True)

programs = [["./assoc_p1"], [sys.executable, "assoc_p2.py"], ["./assoc_p3"]]
repetitions = [1000, 100000, 1000000]
seeds = [1, 2, 3]
intervals = [(0, 1), (-1000, 1000), (-1e15, 1e15)]

rows = []
for prog, r, s, (lo, hi) in itertools.product(programs, repetitions, seeds, intervals):
    args = [f"--repetitions={r}", f"--seed={s}", f"--low={lo:g}", f"--high={hi:g}"]
    out = subprocess.run(prog + args, capture_output=True, text=True, check=True).stdout
    rows.append(json.loads(out))

with open("results_cli.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["program", "repetitions", "seed", "low", "high", "percentage"])
    w.writeheader()
    w.writerows(rows)

groups = defaultdict(dict)
for row in rows:
    groups[(row["repetitions"], row["seed"], row["low"], row["high"])][row["program"]] = row["percentage"]
print(f"{'reps':>8} {'seed':>4} {'low':>8} {'high':>8} | {'P1_C_tp1':>9} {'P2_py':>9} {'P3_C':>9}")
for (r, s, lo, hi), d in groups.items():
    print(f"{r:>8} {s:>4} {lo:>8g} {hi:>8g} | {d['P1_C_tp1']:>9} {d['P2_py_gemini']:>9} {d['P3_C_gemini']:>9}")
