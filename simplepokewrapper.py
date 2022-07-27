from requests import get
from typing import Union
import psycopg2
from json import loads


class PokeWrapper():

    def __init__(self, connect_url) -> None:
        self.conn = psycopg2.connect(connect_url, sslmode='require')

    def query_cache(self, request_url: str) -> Union[str, None]:
        cur = self.conn.cursor()
        cur.execute("SELECT data FROM cache WHERE url=%s", (request_url,))
        row = cur.fetchone()
        if row is None:  # nothing in cache
            return None
        else:  # cache hit!
            return row[0]  # and theres only one thing in the row

    def cache_response(self, request_url: str, response: str) -> None:
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO cache VALUES (%s, %s)",
                        (request_url, response))
            self.conn.commit()

    def access(self, base_url: str, name_or_id: Union[str, int]) -> Union[dict, None]:
        req_url = base_url + str(name_or_id)
        cached = self.query_cache(req_url)
        if cached is not None:  # cache hit!
            return loads(cached)
        else:
            resp = get(req_url)
            if resp.status_code != 200:  # there was an error
                return None
            self.cache_response(req_url, resp.text)
            return resp.json()

    def pokemon(self, name_or_id: Union[str, int]) -> Union[dict, None]:
        return self.access("https://pokeapi.co/api/v2/pokemon/", name_or_id)

    def species(self, name_or_id: Union[str, int]) -> Union[dict, None]:
        return self.access("https://pokeapi.co/api/v2/pokemon-species/", name_or_id)

    def all_details(self, name_or_id: Union[str, int]) -> Union[dict, None]:
        poke = self.pokemon(name_or_id)
        if poke is None:
            return None
        spec = self.species(name_or_id)
        if spec is None:
            return None
        en_name = [x['name'] for x in spec["names"]
                   if x['language']['name'] == "en"][0]  # fucking lmao, nice api nerd
        desc = [x for x in spec['flavor_text_entries']
                if x['language']['name'] == "en"][0]['flavor_text']
        sprite_url = poke['sprites']['other']['official-artwork']['front_default']
        return {
            "id": spec['id'],
            "name": en_name,
            "pokedex": desc,
            "sprite": sprite_url
        }
