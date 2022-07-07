from typing import Union
import pokebase

# note: gets individual forms, not species. e.g. "lycanroc" doesnt work, "lycanroc-midday"


def get_deets(name_or_id: Union[str, int]) -> dict:
    pokemon = pokebase.APIResource("pokemon", name_or_id)
    return {
        "name": pokemon.name,
        "desc": [x for x in pokemon.species.flavor_text_entries if x.language.name == "en"][0].flavor_text,
        "sprite": pokemon.sprites.other.__getattribute__("official-artwork").front_default
    }
