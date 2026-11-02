import csv, itertools, subprocess
from pathlib import Path
from jinja2 import Template

template = Template(Path("assoc.c.jinja").read_text())
properties = {
    "assoc_add": ("(x + y) + z", "x + (y + z)"),
    "assoc_mul": ("(x * y) * z", "x * (y * z)"),
    "distrib":   ("x * (y + z)", "x * y + x * z"),
    "inverse":   ("x * (1 / x)", "1"),
}
types = ["float", "double"]

Path("generated").mkdir(exist_ok=True)
rows = []
for (name, (lhs, rhs)), t in itertools.product(properties.items(), types):
    base = f"generated/{name}_{t}"
    Path(base + ".c").write_text(template.render(type=t, lhs=lhs, rhs=rhs))
    subprocess.run(["gcc", "-O2", "-o", base, base + ".c"], check=True)
    out = subprocess.run([base], capture_output=True, text=True, check=True).stdout
    rows.append({"property": name, "type": t, "percentage": float(out)})
    print(f"{name:10} {t:7} {out.strip()}")

with open("results_template.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["property", "type", "percentage"])
    w.writeheader()
    w.writerows(rows)
