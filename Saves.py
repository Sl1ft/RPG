from Character import Hero
import json
def save(hero: 'Hero',saves_name:str) -> None:
    with open(f'{saves_name}.json', 'w',encoding= 'utf-8') as file:
        json.dump(hero.make_dct(),file,ensure_ascii=False,indent=3)

def load_saves(file: str) -> dict:
    try:
        with open(file,'r',encoding='utf-8') as fil:
            return json.load(fil)
    except json.decoder.JSONDecodeError:
        print('Ошибка внутри файла с загрузкой')
    except FileNotFoundError:
        return {}

print(load_saves('sex.json'))

def load_hero(file: str) -> Hero:
    info = load_saves(file)
    hero = Hero('Пепа')
    hero.name = info['name']
    hero.max_hp = info['max_hp']
    hero.hp = info['hp']
    hero.level = info['level']
    hero.exp = info['exp']
    hero.exp_to_next_lvl= info['exp_to_next_lvl']
    hero.damage = info['damage']
    return hero
