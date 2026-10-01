"""Recomputes the food-costing math in a Pop-up Ops output and checks it.

Usage: python3 tests/check_costing.py demo/output.md --guests 20 --price 65
Reads the costing table (Dish | batch cost | cost per plate), redoes every number,
and compares it with what the agent wrote.
"""
import argparse
import re

ap = argparse.ArgumentParser()
ap.add_argument("file")
ap.add_argument("--guests", type=int, required=True)
ap.add_argument("--price", type=float, required=True)
a = ap.parse_args()
text = open(a.file, encoding="utf-8").read()
checks = []


def check(name, ok, detail=""):
    checks.append((name, ok, detail))


def money(s):
    return float(s.replace("$", "").replace(",", "").replace("*", ""))


costing = text[text.find("## Food costing"):]
rows = re.findall(r"^\| (?!Dish|\*\*Total)([^|]+)\| (\$[\d.,]+) \| (\$[\d.,]+) \|", costing, re.M)
check("Costing table found", len(rows) >= 3, f"{len(rows)} dishes")
total = 0.0
for dish, batch, plate in rows:
    b, p = money(batch), money(plate)
    total += b
    check(f"{dish.strip()}: per plate = batch ÷ {a.guests}", abs(b / a.guests - p) < 0.005, f"{b}/{a.guests}={b/a.guests:.2f}, wrote {p:.2f}")
m = re.search(r"\*\*Total\*\* \| \*\*(\$[\d.,]+)\*\* \| \*\*(\$[\d.,]+)\*\*", costing)
check("Total row present", bool(m))
if m:
    check("Total batch cost adds up", abs(money(m.group(1)) - total) < 0.005, f"sum {total:.2f}, wrote {m.group(1)}")
    check("Total per plate correct", abs(money(m.group(2)) - total / a.guests) < 0.005, f"{total/a.guests:.2f}")
per_plate = total / a.guests
pct = per_plate / a.price * 100
check("Food cost % stated correctly", f"{pct:.1f}%" in costing, f"{pct:.1f}%")
buf = per_plate * 1.10
check("10% buffer per plate correct", f"${buf:.2f}" in costing, f"${buf:.2f}")
check("Buffer food cost % correct", f"{buf / a.price * 100:.1f}%" in costing, f"{buf/a.price*100:.1f}%")
for base in (per_plate, buf):
    for t in (0.32, 0.28):
        v = base / t
        check(f"Suggested price {base:.2f} ÷ {t} = ${v:.2f}", f"${v:.2f}" in costing)
check("Prices labeled as estimates", "ESTIMATES" in costing)
check("Allergen key present", "G gluten" in text and "D dairy" in text)
check("Food-safety points present", "Food-safety" in text)

passed = sum(ok for _, ok, _ in checks)
for name, ok, detail in checks:
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))
print(f"\n{passed}/{len(checks)} checks passed")
raise SystemExit(0 if passed == len(checks) else 1)
