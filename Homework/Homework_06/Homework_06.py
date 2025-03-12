from functools import reduce

diablo_heroes = [
    ("Barbarian", 88),
    ("Sorceress", 76),
    ("Necromancer", 95),
    ("Paladin", 60),
    ("Amazon", 45),
    ("Druid", 82),
    ("Assassin", 91)
]

battle_result = lambda score: "Victory" if score >= 50 else "Defeat"
total_battle_score = reduce(lambda x, y: x + y[1], diablo_heroes, 0)
ranked_heroes = sorted(diablo_heroes, key=lambda x: x[1], reverse=True)
victorious_heroes = list(filter(lambda x: x[1] >= 50, diablo_heroes))

graded_heroes = list(map(lambda x: (x[0], x[1], 
    "S" if x[1] >= 90 else 
    "A" if x[1] >= 80 else 
    "B" if x[1] >= 70 else 
    "C" if x[1] >= 50 else 
    "F"), diablo_heroes))

ultimate_champion = reduce(lambda x, y: x if x[1] > y[1] else y, diablo_heroes)
hero_ranks = list(enumerate(ranked_heroes, start=1))
battle_outcomes = list(zip([h[0] for h in diablo_heroes], map(lambda x: battle_result(x[1]), diablo_heroes)))

print("\n🔥 **Diablo 2 PvP Ranking System** 🔥\n")
print("💀 Total PvP Score:", total_battle_score)

print("\n🏆 **Ranked Heroes (by PvP Score):**")
for rank, (name, score) in hero_ranks:
    print(f"#{rank} - {name}: {score} points")

print("\n⚔️ **Victorious Heroes (Score ≥ 50):**")
print(victorious_heroes)

print("\n📜 **Hero Power Tiers:**")
for hero in graded_heroes:
    print(hero)

print("\n👑 **Ultimate Champion:**", ultimate_champion)

print("\n⚔️ **Battle Outcomes:**")
for name, outcome in battle_outcomes:
    print(f"{name}: {outcome}")
