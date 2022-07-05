import pokebase



vappo = pokebase.pokemon_species("goodra")
poke_name = vappo.name
poke_desc = vappo.flavor_text_entries[0].flavor_text
poke_desc = [x for x in vappo.flavor_text_entries if x.language.name == "en"][0].flavor_text
print()