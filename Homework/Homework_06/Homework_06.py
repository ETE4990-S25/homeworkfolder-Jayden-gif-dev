from functools import reduce

# List of heroes and their scores
heroes = [
    ("Barbarian", 88),
    ("Sorceress", 76),
    ("Necromancer", 95),
    ("Paladin", 60),
    ("Amazon", 45),
    ("Druid", 82),
    ("Assassin", 91)
]

# Determine if a hero wins or loses
def battle_result(score):
    return "Victory" if score >= 50 else "Defeat"

# Total score of all heroes
total_score = sum(score for _, score in heroes)

# Sort heroes by score, highest first
ranked = sorted(heroes, key=lambda x: x[1], reverse=True)

# Filter heroes who won
victorious = [hero for hero in heroes if hero[1] >= 50]

# Grading scale using thresholds
grade_thresholds = {
    "S": 90,
    "A": 80,
    "B": 70,
    "C": 50,
    "F": 0
}

def get_grade(score):
    for grade, threshold in grade_thresholds.items():
        if score >= threshold:
            return grade

graded = [(name, score, get_grade(score)) for name, score in heroes]

# Find the hero with the highest score
top_hero = max(heroes, key=lambda x: x[1])

# Display results
print("\nDiablo 2 PvP Ranking System\n")
print("Total PvP Score:", total_score)

print("\nRanked Heroes:")
for i, (name, score) in enumerate(ranked, start=1):
    print(f"{i}. {name} - {score} points")

print("\nVictorious Heroes (score ≥ 50):")
for name, score in victorious:
    print(f"{name} - {score}")

print("\nHero Grades:")
for name, score, g in graded:
    print(f"{name} - {score} points - Grade: {g}")

print("\nTop Hero:", top_hero[0], "with", top_hero[1], "points")

print("\nBattle Results:")
for name, score in heroes:
    print(f"{name}: {battle_result(score)}")
