from random import randint,choice,choices
from Character import INVENTORY_LIMIT, Hero, NotEnoughGold, InventoryFullError, ItemNotFoundError
from combat import fight
from enum import Enum
from Shop import Shop, OutOfStockError


class Events(Enum):
    MONSTER = "Монстр"
    TREASURE = "Сокровище"
    UNKNOWN = "Неизвестность"
    TRAP = "Ловушка"
    SHOP = "Торговец"

def chance(some_list):
    return choices(some_list, weights=[i.weight for i in some_list], k=1)[0]

ROOM_EVENTS = [i for i in Events if i != Events.TRAP]

def open_treasure(hero: 'Hero',item_list: list) -> None:
    treasure = choices(['item','small_gold','big_gold'], weights= [40,50,10], k=1)[0]
    if treasure == 'item':
        hero.take_item(chance(item_list))
    elif treasure == 'small_gold':
        hero.gain_gold(randint(150,300))
    elif treasure == 'big_gold':
        hero.gain_gold(randint(600,800))

def open_shop(hero: 'Hero') -> None:
    shop = Shop()
    chose = ['Купить','Продать','Выйти из магазина']
    while True:
        for i,move in enumerate(chose,start=1):
            print(f'{i}: {move}')
        try:
            user_input = int(input())
        except ValueError:
            print('Введите число!')
            continue
        if 0 < user_input <= len(chose):
            if user_input == 1:
                while True:
                    shop.buy_menu()
                    print(f'{len(shop.shop_dict)+1}. Выйти')
                    print(f'У вас {hero.gold}')
                    try:
                        user_item = int(input())
                    except ValueError:
                        print('Введите число')
                        continue
                    if 0 < user_item <= len(shop.shop_dict)+1:
                        if user_item == len(shop.shop_dict)+1:
                            break
                        item = shop.choose_buy(user_item)
                        try:
                            buy_item(hero,shop,item)
                        except OutOfStockError:
                            print('Предмет закончился')
                        except NotEnoughGold:
                            print('У вас недостаточно золота')
                        except InventoryFullError:
                            print('Ваш рюкзак полон')
                        else:
                            print(f'Вы купили {item.name}')
                    else:
                        print('Введите число из выше перечисленных')
            elif user_input == 2:
                while True:
                    a = hero.sell_menu()
                    if a is not None:
                        try:
                            hero.sell_item(a)
                        except ItemNotFoundError:
                            print('Выбранного предмета нету в инвентаре')
                            continue
                    else:
                        break
            elif user_input == 3:
                return None
        else:
            print('Выберите вариант из предложенных!')

def buy_item(hero: 'Hero', shop: 'Shop', item: 'Item') -> None:
    shop.item_sell(item)
    try:
        hero.spend_gold(item.price)
    except NotEnoughGold:
        shop.shop_dict[item] += 1
        raise
    try:
        hero.input_item(item)
    except InventoryFullError:
        hero.gold += item.price
        shop.shop_dict[item] += 1
        raise

def room(hero: 'Hero', monsters_list: list,items_list:list):
    a = randint(1,3)
    if a == 1:
        print(f'Перед вами {a} комната')
    else:
        print(f'Перед вами {a} комнаты')

    directions = ['Прямо', 'Слева', 'Справа']
    choose = []
    current_events ={}
    for i in range(1,a+1):

        direction = choice(directions)
        choose.append(direction)
        current_events.setdefault(direction, choice(ROOM_EVENTS))
        directions.remove(direction)
        print(f'{direction} от вас находится {current_events[direction].value}')
    print('\nКуда вы собираетесь пойти?')
    while True:
        for i,j in enumerate(choose,start= 1):
            print(f'{i}: {j}')

        try:
            user_input = int(input())
            if user_input in range(1,a+1):
                if current_events[choose[user_input-1]] == Events.MONSTER:
                    chosen_monstr = chance(monsters_list)
                    fight(hero,chosen_monstr)
                    break
                elif current_events[choose[user_input-1]] == Events.TREASURE:
                    open_treasure(hero, items_list)
                    break
                elif current_events[choose[user_input-1]] == Events.SHOP:
                    open_shop(hero)
                    break
                elif current_events[choose[user_input-1]] == Events.UNKNOWN:
                    chosen_event = choices([e for e in Events if e != Events.UNKNOWN], weights=[60,50,30,5], k=1)[0]
                    print(f'В комнате за слоем тумана, оказывается {chosen_event.value}')
                    if chosen_event == Events.MONSTER:
                        fight(hero,chance(monsters_list))
                        break
                    elif chosen_event == Events.TREASURE:
                        open_treasure(hero,items_list)
                        break
                    elif chosen_event == Events.TRAP:
                        trap_damage = randint(10,50)
                        print(f'Вы попались в ловушку и вам нанесло {trap_damage} урона')
                        hero.hp -= trap_damage
                        break
                    elif chosen_event == Events.SHOP:
                        print(f'Вас встречает мужчина, который представился торговцем')
                        open_shop(hero)
                        break
            else:
                print('Введите вариант из списка')
        except(ValueError,IndexError):
            print('\nВведити вариант из выше перечисленных!\n')

