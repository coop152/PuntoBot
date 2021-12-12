import random

CHARACTERS = [
    "typhlosion",
    "pikachu",
    "charizard",
    ""
    "rouge the bat",
    "falco",
]
ADJECTIVES = [
    "",
    "femboy",
    "futa",
    "genderbent",
    "obese",
]
ADJ_WEIGHTS = [0.9] + [0.9 / (len(ADJECTIVES) - 1)] * (len(ADJECTIVES) - 1)
FETISHES = [
    "inflation",
    "flattening",
    "BDSM",
    "forced",
    "petrification",
    "transformation",
]
FINAL_WORD = [
    "porn",
    "zorn",
    "yiff",
    "hentai",
]


def make_pairing():
    character_count = random.randint(1, 2)
    characters = random.choices(CHARACTERS, k=character_count)
    adjectives = random.choices(ADJECTIVES, ADJ_WEIGHTS, k=character_count)
    names = [c if a == "" else f"{a} {c}" for c, a in zip(characters, adjectives)]
    return '/'.join(names)

def make_zorn():
    fetish_count = random.randint(0, 2)
    fetishes = random.sample(FETISHES, k=fetish_count)
    fetishes = ' '.join(fetishes)
    final_word = random.choice(FINAL_WORD)
    pairing = make_pairing()
    return f"{pairing} {fetishes} {final_word}"