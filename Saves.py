from selectors import SelectSelector

from Character import Hero
from Items import Sword, HealPotion,Bow,Hammer
import json
SAVES_FILE = 'Saves.json'
Max_Saves = 3

items_dict = {'sword': Sword, 'heal_potion': HealPotion, 'bow': Bow, 'hammer': Hammer}

def save(hero: 'Hero',saves_name:str) -> None:
    dct = load_saves()
    flag = True
    if saves_name in dct:
        flag= False
    dct[saves_name] = hero.make_dct()
    with open(SAVES_FILE, 'w',encoding= 'utf-8') as file:
        json.dump({"Saves": dct},file,ensure_ascii=False,indent=3)
        if flag:
            print('Успешно сохранено')
        else:
            print('Сохранение перезаписанно')

def delete_save(name:str) -> None:
    dct = load_saves()
    dct.pop(name)
    with open(SAVES_FILE,'w',encoding='utf-8') as file:
        json.dump({'Saves': dct},file,ensure_ascii=False,indent=3)



def load_saves() -> dict:
    try:
        with open(SAVES_FILE,'r',encoding='utf-8') as file:
            return json.load(file).get('Saves', {})
    except json.decoder.JSONDecodeError:
        return {}
    except FileNotFoundError:
        return {}

def load_hero(saves_name:str) -> Hero:
    info = load_saves()[saves_name]
    hero = Hero(info['name'])
    hero.max_hp = info['max_hp']
    hero.hp = info['hp']
    hero.level = info['level']
    hero.exp = info['exp']
    hero.exp_to_next_lvl= info['exp_to_next_lvl']
    hero.inventory = [items_dict[i]() for i in info['inventory']]
    hero.is_equipped = items_dict[info['is_equipped']]() if info['is_equipped'] else None
    hero.damage = info['damage']
    return hero