import argparse, random

p = argparse.ArgumentParser()
p.add_argument("--repetitions", type=int, default=1000)
p.add_argument("--seed", type=int, default=1)
p.add_argument("--low", type=float, default=0.0)
p.add_argument("--high", type=float, default=1.0)
p.add_argument("--cstyle", type=int, default=0)
p.add_argument("--property", default="AssocAdd")
a = p.parse_args()

PROPS = {
    "AssocAdd": lambda x, y, z: (x + y) + z == x + (y + z),
    "AssocMul": lambda x, y, z: (x * y) * z == x * (y * z),
    "Distrib":  lambda x, y, z: x * (y + z) == x * y + x * z,
    "Inverse":  lambda x, y, z: x * (1 / x) == 1,
}
check = PROPS[a.property]
rng = random.Random(a.seed)
M = 2**31 - 1

def draw():
    u = rng.randrange(M + 1) / M if a.cstyle == 1 else rng.random()
    return a.low + (a.high - a.low) * u

holds = 0
for _ in range(a.repetitions):
    x, y, z = draw(), draw(), draw()
    try:
        if check(x, y, z):
            holds += 1
    except ZeroDivisionError:      # x == 0 dans 1/x : la propriété n'est pas vérifiée
        pass
print(f"{100 * holds / a.repetitions:.4f}")
