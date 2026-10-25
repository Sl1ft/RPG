from Character import Hero
import json
def save(hero: 'Hero',saves_name:str) -> None:
    with open(f'{saves_name}.json', 'w',encoding= 'utf-8') as file:
        json.dump(hero.make_dct(),file,ensure_ascii=False,indent=3)
