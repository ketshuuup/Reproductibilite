import argparse, json, random

p = argparse.ArgumentParser()
p.add_argument("--repetitions", type=int, default=1000000)
p.add_argument("--seed", type=int, default=42)
p.add_argument("--low", type=float, default=-1e15)
p.add_argument("--high", type=float, default=1e15)
p.add_argument("--cstyle", type=int, default=0, choices=[0, 1])
a = p.parse_args()

rng = random.Random(a.seed)
M = 2**31 - 1

def draw():
    if a.cstyle == 1:
        u = rng.randrange(M + 1) / M          # comme rand()/RAND_MAX en C
    else:
        u = rng.random()                      # générateur natif de Python
    return a.low + (a.high - a.low) * u       # même formule que uniform()

holds = 0
for _ in range(a.repetitions):
    x = draw()
    y = draw()
    z = draw()
    if (x + y) + z == x + (y + z):
        holds += 1

print(json.dumps({"program": "P2_py_gemini", "repetitions": a.repetitions,
                  "seed": a.seed, "low": a.low, "high": a.high, "cstyle": a.cstyle,
                  "percentage": round(100 * holds / a.repetitions, 4)}))
