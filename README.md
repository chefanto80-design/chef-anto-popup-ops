# Chef Anto Pop-up Ops 🍲

**Operations for Chef Anto's Balkan pop-ups, Baba by Chef Anto (Tuesdays) and Dream House by Chef Anto (Wednesdays): menus, prep timelines, shopping lists, food costing and guest messages.**
Part of the [Chef Anto AI Agency](https://github.com/chefanto80-design/chef-anto-agent). Built by Chef Anto (Antoanela Alexander), Miami.

## What the agent produces
| Output | Details |
|---|---|
| Menu | Gustări · Ciorbe · De la Casă · Dulciuri, allergens marked (G, D, N, E, F, S, V, VG), trilingual RO/EN/ES on request |
| Prep timeline | T-7, T-3, T-2, T-1, day-of hour by hour, service, close-down |
| Shopping list | Scaled to guest count + 10% buffer, grouped by store section |
| Costing | Cost per plate, food cost %, suggested seat price at 28–32% food cost, **all math shown** |
| Guest messages | Confirmation, dietary question, 24-hour reminder, thank-you (drafts only) |

It never books, buys, pays or sends. Chef Anto approves everything.

## Files
| Path | What it is |
|---|---|
| [`skill/SKILL.md`](skill/SKILL.md) | The agent's full instructions (Claude skill) |
| [`demo/output.md`](demo/output.md) | Real demo: Baba menu + costing, verbatim |
| [`tests/check_costing.py`](tests/check_costing.py) | Re-does every number in the costing table and compares |

## How to use
**Claude app:** zip the `skill` folder renamed to `chef-anto-popup-ops`, upload it in Claude's Settings → Skills, then ask:
> Use chef-anto-popup-ops. Baba Tuesday, 20 guests, $65 a seat, family-style. Menu and costing.

**Claude Code:** `mkdir -p ~/.claude/skills/chef-anto-popup-ops && cp skill/SKILL.md ~/.claude/skills/chef-anto-popup-ops/`

## Real demo
Run on **2026-10-01 (UTC)** in Claude (Cowork), model `claude-opus-5-5`, by invoking the `chef-anto-popup-ops` skill.

**Input (exact):**
```
Demo order: Baba by Chef Anto, Tuesday pop-up, 20 guests, $65 per seat, family-style service.
Give me the menu (with allergens) and the food costing table with the math. Ingredient prices
are estimates; label them as such.
```

**Output** ([full, verbatim](demo/output.md)):
- Menu: zacuscă + bread, tzatziki, ciorbă de perișoare, sarmale with mămăligă, papanași, each with allergens
- Costing (**estimated** prices): $266 total → **$13.30 per plate → 20.5% food cost** at $65; with a 10% buffer **$14.63 → 22.5%**
- Suggested price range at 28–32%: $41.56–$47.50 (or $45.72–$52.25 with buffer), so $65 leaves room for drinks, labor and venue
- Food-safety points: cooling, hot holding, allergen cross-contact

## Test results (only tests actually run)
| # | Test | Result |
|---|---|---|
| 1 | Live run of the skill on the demo input | ✅ Menu + costing produced, saved verbatim |
| 2 | `python3 tests/check_costing.py demo/output.md --guests 20 --price 65` | ✅ **19/19 passed**: every per-plate number, the total, food cost %, 10% buffer and all 4 suggested prices recomputed and matched |
| 3 | Checker on a costing table with a deliberate math error | ✅ Caught it: **4/17 passed** |

**Not tested yet:** ingredient prices are estimates, not supplier quotes; the menu has not been cooked for guests; the prep timeline, shopping list and guest messages were not part of this demo.

## Run the tests
```bash
python3 tests/check_costing.py demo/output.md --guests 20 --price 65
```

---
Chef Anto 🌿🤓❤️
