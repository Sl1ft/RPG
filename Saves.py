from selectors import SelectSelector
from xmlrpc.client import FastMarshaller

from Character import Hero
from Items import Sword, HealPotion,Bow,Hammer
import json
SAVES_FILE = 'Saves.json'
MAX_SAVES = 3

items_dict = {'sword': Sword, 'heal_potion': HealPotion, 'bow': Bow, 'hammer': Hammer}

def write_saves(dct:dict,path:str = SAVES_FILE) -> None:
    with open(path,'w', encoding='utf-8') as file:
        json.dump({"Saves": dct},file, ensure_ascii=False ,indent=3)

def save(hero: 'Hero',saves_name:str,path: str= SAVES_FILE) -> None:
    dct = load_saves(path)
    is_new = True
    if saves_name in dct:
        is_new = False
    dct[saves_name] = hero.make_dct()
    write_saves(dct,path)
    if is_new:
        print('Успешно сохранено')
    else:
        print('Сохранение перезаписано')

def delete_save(name:str,path: str= SAVES_FILE) -> None:
    dct = load_saves(path)
    dct.pop(name)
    write_saves(dct,path)



def load_saves(path: str= SAVES_FILE) -> dict:
    try:
        with open(path,'r',encoding='utf-8') as file:
            return json.load(file).get('Saves', {})
    except json.decoder.JSONDecodeError:
        return {}
    except FileNotFoundError:
        return {}

def load_hero(saves_name:str,path: str= SAVES_FILE) -> Hero:
    info = load_saves(path)[saves_name]
    hero = Hero(info['name'])
    hero.max_hp = info['max_hp']
    hero.hp = info['hp']
    hero.level = info['level']
    hero.exp = info['exp']
    hero.exp_to_next_lvl= info['exp_to_next_lvl']
    hero.inventory = [items_dict[i]() for i in info['inventory']]
    hero.is_equipped = items_dict[info['is_equipped']]() if info['is_equipped'] else None
    hero.damage = info['damage']
    hero.gold = info['gold']
    return hero
