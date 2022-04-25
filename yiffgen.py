import random

CHARACTERS = [
    "typhlosion",
    "feraligatr",
    "pikachu",
    "charizard",
    "lucario",
    "gengar",
    "mewtwo",
    "mew",
    "latios",
    "latias",
    "snivy",
    "falco lombardi",
    "star fox",
    "slippy frog",
    "mario",
    "hercules",
    "kanye west",
    "le bron james",
    "michael jordon",
    "obama",
    "peter kay",
    "sans",
    "sonic the hedgehog",
    "shadow the hedgehog",
    "rouge the bat",
    "miles \"tails\" prower",
    "knuckles the echidna",
    "dr. robotnik",
    "silver the hedgehog",
    "jerma985",
    "james cordon",
]
ADJECTIVES = [
    "",
    "femboy",
    "futa",
    "genderbent",
    "obese",
    "macro",
    "catboy",
    "anthro",
    "feral",
    "shortstack",
    "paedophile",
    "sleeping"
]
ADJ_WEIGHTS = [0.9] + [0.9 / (len(ADJECTIVES) - 1)] * (len(ADJECTIVES) - 1)
FETISHES = [
    "inflation",
    "flattening",
    "BDSM",
    "forced",
    "petrification",
    "transformation",
    "identity death",
    "necrophilia",
    "vore",
    "watersports",
    "scat",
    "mpreg",
    "hypnotism",
    "portal"
]
FINAL_WORD = [
    "porn",
    "zorn",
    "yiff",
    "hentai"
]

pogg_ing = False
def make_pairing(low_bound, high_bound):
    character_count = random.randint(low_bound, high_bound)
    if pogg_ing:
        character_count = 2
        characters = ["typhlosion", "feraligatr"]
    else:
        characters = random.choices(CHARACTERS, k=character_count)
    adjectives = random.choices(ADJECTIVES, ADJ_WEIGHTS, k=character_count)
    names = [c if a == "" else f"{a} {c}" for c, a in zip(characters, adjectives)]
    if ("typhlosion", "feraligatr") in characters:
        pogg_ing = True
    return '/'.join(names)


def make_zorn():
    fetish_count = random.randint(0, 2)
    fetishes = random.sample(FETISHES, k=fetish_count)
    fetishes = ' '.join(fetishes)
    final_word = random.choice(FINAL_WORD)
    pairing = make_pairing(1, 2)
    return f"{pairing} {fetishes} {final_word}" if fetishes != "" else f"{pairing} {final_word}"


if __name__ == "__main__":
    print(make_zorn())
