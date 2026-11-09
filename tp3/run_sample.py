import argparse, csv, platform, random, subprocess, sys
from pathlib import Path
from jinja2 import Template

ap = argparse.ArgumentParser()
ap.add_argument("--sample", default="configs/sample.csv")
ap.add_argument("--runs", type=int, default=5)
ap.add_argument("--only", nargs="*", default=None, help="config_id à exécuter")
a = ap.parse_args()

ARCH = {"x86_64": "X86_64", "aarch64": "Arm64", "arm64": "Arm64"}
machine = platform.machine()
my_arch = ARCH.get(machine, machine)

INTERVALS = {"Int_0_1": (0, 1), "Int_0_1000": (0, 1000), "Int_m1_1": (-1, 1),
             "Int_m1000_1000": (-1000, 1000), "Int_m1e15_1e15": (-1e15, 1e15)}
PROPERTIES = {"AssocAdd": ("(x + y) + z", "x + (y + z)"),
              "AssocMul": ("(x * y) * z", "x * (y * z)"),
              "Distrib":  ("x * (y + z)", "x * y + x * z"),
              "Inverse":  ("x * (1 / x)", "1")}
OPT = {"O0": ["-O0"], "O2": ["-O2"], "O2FastMath": ["-O2", "-ffast-math"]}

template = Template(Path("templates/assoc.c.jinja").read_text())
Path("build").mkdir(exist_ok=True)
Path("results").mkdir(exist_ok=True)
gcc_version = subprocess.run(["gcc", "-dumpfullversion"], capture_output=True, text=True).stdout.strip()

def build_c(ctype, prop, opt):
    name = f"build/{prop}_{ctype}_{opt}"
    lhs, rhs = PROPERTIES[prop]
    Path(name + ".c").write_text(template.render(ctype=ctype, lhs=lhs, rhs=rhs))
    subprocess.run(["gcc", *OPT[opt], "-o", name, name + ".c"], check=True)
    return name

out_path = Path(f"results/results_{machine}.csv")
rows = []
with open(a.sample) as f:
    configs = list(csv.DictReader(f))

for c in configs:
    if a.only and c["config_id"] not in a.only:
        continue
    low, high = INTERVALS[c["Interval"]]
    reps = int(c["Repetitions"].removeprefix("Rep"))
    prop = c["Property"]
    if c["Language"] == "LangC":
        ctype = "float" if c["NumType"] == "Float32" else "double"
        exe = [build_c(ctype, prop, c["Optimization"])]
    else:
        exe = [sys.executable, "assoc_py.py", f"--property={prop}",
               f"--cstyle={1 if c['Generator'] == 'GenPyCStyle' else 0}"]
    for run in range(1, a.runs + 1):
        if c["Seed"] == "SeedNotFixed":
            seed = random.SystemRandom().randrange(1, 2**31)
        else:
            seed = int(c["Seed"].removeprefix("Seed"))
        args = [f"--repetitions={reps}", f"--seed={seed}", f"--low={low:g}", f"--high={high:g}"]
        out = subprocess.run(exe + args, capture_output=True, text=True, check=True).stdout
        rows.append({**c, "run": run, "seed_used": seed, "repetitions_n": reps,
                     "low": low, "high": high, "percentage": float(out),
                     "machine": machine, "os": platform.platform(),
                     "python": platform.python_version(), "gcc": gcc_version})
    print(f"{c['config_id']}: {a.runs} exécutions, dernier résultat {rows[-1]['percentage']}")

with out_path.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f"écrit : {out_path} ({len(rows)} lignes)")
