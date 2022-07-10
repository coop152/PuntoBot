from requests import get
from typing import Optional, Union


# caching would probably go here
def access(base_url, name_or_id: Union[str, int]) -> Optional[dict]:
    resp = get(base_url + str(name_or_id))
    if resp.status_code != 200:  # there was an error
        return None
    return resp.json()


def pokemon(name_or_id: Union[str, int]) -> Optional[dict]:
    return access("https://pokeapi.co/api/v2/pokemon/", name_or_id)


def species(name_or_id: Union[str, int]) -> Optional[dict]:
    return access("https://pokeapi.co/api/v2/pokemon-species/", name_or_id)


def all_details(name_or_id: Union[str, int]) -> Optional[dict]:
    poke = pokemon(name_or_id)
    if poke is None:
        return None
    spec = species(name_or_id)
    if spec is None:
        return None
    en_name = [x['name'] for x in spec["names"]
               if x['language']['name'] == "en"][0]  # fucking lmao, nice api nerd
    desc = [x for x in spec['flavor_text_entries']
            if x['language']['name'] == "en"][0]['flavor_text']
    sprite_url = poke['sprites']['other']['official-artwork']['front_default']
    return {
        "name": en_name,
        "pokedex": desc,
        "sprite": sprite_url
    }
